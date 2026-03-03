"""
Video generation orchestration service
"""

import os
import subprocess
import tempfile
from typing import Dict, List, Optional

import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.core.celery_app import celery_app
from app.core.storage import storage_service
from app.models.video import Video, VideoStatus
from app.services.avatar import avatar_service
from app.services.voice import voice_service

logger = get_logger(__name__)


class VideoGenerationService:
    """Orchestrate video generation process"""
    
    def __init__(self):
        self.runpod_api_key = settings.RUNPOD_API_KEY
        self.runpod_endpoint = settings.RUNPOD_SADTALKER_ENDPOINT
    
    async def generate_anime_video(
        self,
        scenes: List[Dict],
        expression_images: Dict[str, str],
        audio_paths: List[str],
        output_path: str,
    ) -> str:
        """Generate anime-style video from image sequences"""
        scene_videos = []
        
        for i, scene in enumerate(scenes):
            emotion = scene.get("emotion", "neutral")
            duration = scene.get("duration", 5)
            audio_path = audio_paths[i] if i < len(audio_paths) else None
            
            # Get expression image URL
            image_url = expression_images.get(emotion, expression_images.get("neutral"))
            
            # Download image
            image_path = f"/tmp/scene_{i}_image.png"
            await self._download_file(image_url, image_path)
            
            # Create scene video
            scene_video = f"/tmp/scene_{i}.mp4"
            await self._create_anime_scene(
                image_path=image_path,
                audio_path=audio_path,
                duration=duration,
                output_path=scene_video,
                effect=scene.get("effect", "zoom_in"),
            )
            
            scene_videos.append(scene_video)
        
        # Concatenate all scenes
        await self._concatenate_scenes(scene_videos, output_path)
        
        return output_path
    
    async def generate_realistic_video(
        self,
        face_image_url: str,
        audio_path: str,
        output_path: str,
    ) -> str:
        """Generate realistic talking head using SadTalker on RunPod"""
        
        # Upload to temp storage if needed
        face_temp = await self._ensure_url_accessible(face_image_url)
        audio_temp = await self._ensure_url_accessible(audio_path)
        
        # Submit job
        job_id = await self._submit_runpod_job(face_temp, audio_temp)
        
        # Poll for completion
        video_url = await self._poll_runpod_job(job_id)
        
        # Download result
        await self._download_file(video_url, output_path)
        
        return output_path
    
    async def _create_anime_scene(
        self,
        image_path: str,
        audio_path: Optional[str],
        duration: int,
        output_path: str,
        effect: str = "zoom_in",
    ):
        """Create single anime scene with effects"""
        
        # FFmpeg zoom/pan effects
        effects = {
            "zoom_in": "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
            "zoom_out": "zoompan=z='max(1.5-zoom*0.0015,1)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
            "pan_left": "zoompan=z=1.2:x='iw/2-(iw/zoom/2)+50*t':y='ih/2-(ih/zoom/2)'",
            "pan_right": "zoompan=z=1.2:x='iw/2-(iw/zoom/2)-50*t':y='ih/2-(ih/zoom/2)'",
            "static": "zoompan=z=1.0:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
        }
        
        vf = effects.get(effect, effects["zoom_in"])
        vf += ",fade=t=out:st=4:d=1"  # Add fade out
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", vf,
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-crf", "23",
        ]
        
        if audio_path and os.path.exists(audio_path):
            cmd.extend(["-i", audio_path, "-c:a", "aac", "-shortest"])
        else:
            cmd.extend(["-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-shortest"])
        
        cmd.append(output_path)
        
        subprocess.run(cmd, check=True, capture_output=True)
    
    async def _concatenate_scenes(self, scene_paths: List[str], output_path: str):
        """Concatenate scene videos"""
        concat_file = "/tmp/concat_list.txt"
        with open(concat_file, "w") as f:
            for path in scene_paths:
                f.write(f"file '{path}'\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path,
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
    
    async def _submit_runpod_job(self, face_image_url: str, audio_url: str) -> str:
        """Submit job to RunPod"""
        
        url = f"https://api.runpod.ai/v2/{self.runpod_endpoint}/run"
        
        payload = {
            "input": {
                "source_image": face_image_url,
                "driven_audio": audio_url,
                "preprocess": "crop",
                "still_mode": False,
                "use_enhancer": True,
                "batch_size": 1,
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.runpod_api_key}",
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()["id"]
    
    async def _poll_runpod_job(self, job_id: str, max_attempts: int = 60) -> str:
        """Poll RunPod job until complete"""
        
        url = f"https://api.runpod.ai/v2/{self.runpod_endpoint}/status/{job_id}"
        headers = {"Authorization": f"Bearer {self.runpod_api_key}"}
        
        async with httpx.AsyncClient() as client:
            for _ in range(max_attempts):
                response = await client.get(url, headers=headers, timeout=10.0)
                result = response.json()
                
                status = result.get("status")
                
                if status == "COMPLETED":
                    output = result.get("output", {})
                    if isinstance(output, dict):
                        return output.get("video_url")
                    elif isinstance(output, list):
                        return output[0]
                    raise ValueError(f"Unexpected output: {output}")
                
                elif status in ["FAILED", "CANCELLED"]:
                    raise Exception(f"Job failed: {result.get('error', 'Unknown')}")
                
                await __import__("asyncio").sleep(2)
            
            raise TimeoutError("Job polling timeout")
    
    async def _download_file(self, url: str, output_path: str):
        """Download file from URL"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
    
    async def _ensure_url_accessible(self, file_path: str) -> str:
        """Ensure file is accessible via URL"""
        if file_path.startswith("http"):
            return file_path
        
        # Upload to storage and return URL
        # TODO: Implement upload
        return file_path


class VideoQueueService:
    """Queue video generation tasks"""
    
    async def queue_video_generation(self, video_id: str, user_id: str) -> str:
        """Queue video generation Celery task"""
        
        from app.tasks.video_generation import generate_video_task
        
        # Call Celery task
        task = generate_video_task.delay(video_id=video_id, user_id=user_id)
        
        return task.id


video_generation_service = VideoGenerationService()
video_queue_service = VideoQueueService()