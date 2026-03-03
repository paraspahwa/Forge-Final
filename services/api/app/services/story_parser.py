"""
Story parsing service using Lepton AI (Llama)
"""

from typing import List, Optional

import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.video import Scene

logger = get_logger(__name__)


class StoryParserService:
    """Parse stories into structured scenes"""
    
    def __init__(self):
        self.api_key = settings.LEPTON_API_KEY
        self.base_url = "https://api.lepton.ai/models/llama3-1-8b/completion"
    
    async def parse_story(
        self,
        story_text: str,
        character_type: str,
        num_scenes: int = 5,
    ) -> List[Scene]:
        """Parse story into scenes using LLM"""
        
        style_guide = {
            "anime": "Anime-style scenes with emotional expressions and dynamic action",
            "realistic": "Realistic scenes with natural human emotions and subtle movements",
        }
        
        prompt = f"""Parse this story into {num_scenes} scenes for a {character_type} video.

Story: {story_text}

Style: {style_guide.get(character_type, "Standard")}

Return ONLY a JSON array with this exact format:
[
  {{
    "scene_number": 1,
    "description": "Visual description of what's happening",
    "dialogue": "Spoken lines (optional)",
    "emotion": "happy|sad|angry|surprised|neutral",
    "duration": 5,
    "background_prompt": "Description of background setting"
  }}
]

Make scenes engaging and visually descriptive. Keep dialogue natural. Vary emotions across scenes."""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.7,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=30.0,
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("text", "")
            
            # Extract JSON from response
            import json
            import re
            
            # Find JSON array in response
            json_match = re.search(r'\[.*\]', generated_text, re.DOTALL)
            if json_match:
                scenes_data = json.loads(json_match.group())
                scenes = [Scene(**scene) for scene in scenes_data]
                return scenes
            else:
                raise ValueError("Could not parse scenes from LLM response")
    
    async def generate_title(self, story_text: str) -> Optional[str]:
        """Generate a title for the story"""
        
        prompt = f"""Create a short, catchy title (5 words or less) for this story:

{story_text[:500]}

Title:"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": 50,
            "temperature": 0.7,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            
            result = response.json()
            title = result.get("text", "").strip().strip('"\'')
            return title if title else None


story_parser_service = StoryParserService()