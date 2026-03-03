"""
Avatar generation service using Segmind API
"""

import os
from typing import Dict, List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import get_logger
from app.models.avatar import CharacterType

logger = get_logger(__name__)


# Segmind configurations
SEGMIND_CONFIGS = {
    CharacterType.ANIME: {
        "url": "https://api.segmind.com/v1/sdxl-anime",
        "prompt": "{description}, {expression} expression, anime style, high quality, detailed, masterpiece",
        "negative": "realistic, 3d, photo, photograph, ugly, deformed, blurry, low quality",
        "width": 512,
        "height": 512,
        "scheduler": "dpmpp_2m",
        "steps": 25,
        "scale": 7.5,
    },
    CharacterType.REALISTIC: {
        "url": "https://api.segmind.com/v1/tiny-sd-portrait",
        "prompt": "{description}, {expression} expression, photorealistic, 8k uhd, detailed skin, professional photography, studio lighting",
        "negative": "anime, cartoon, illustration, drawing, 3d render, ugly, deformed, blurry",
        "width": 512,
        "height": 512,
        "scheduler": "dpmpp_2m",
        "steps": 30,
        "scale": 7.5,
    },
}


EXPRESSION_MODIFIERS = {
    "happy": "smiling, joyful, cheerful, bright eyes",
    "sad": "crying, tears, sorrowful, downcast eyes",
    "angry": "furious, rage, intense stare, clenched jaw",
    "surprised": "shocked, wide eyes, open mouth, amazed",
    "neutral": "calm expression, relaxed, looking at camera",
}


class AvatarService:
    """Service for generating avatar images"""
    
    def __init__(self):
        self.api_key = settings.SEGMIND_API_KEY
        self.client = httpx.AsyncClient(timeout=60.0)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_expression(
        self,
        character_type: CharacterType,
        description: str,
        expression: str,
        seed: Optional[int] = None,
    ) -> str:
        """Generate a single expression image"""
        config = SEGMIND_CONFIGS[character_type]
        
        # Build prompt
        expression_modifier = EXPRESSION_MODIFIERS.get(expression, "")
        prompt = config["prompt"].format(
            description=description,
            expression=expression_modifier
        )
        
        payload = {
            "prompt": prompt,
            "negative_prompt": config["negative"],
            "width": config["width"],
            "height": config["height"],
            "samples": 1,
            "scheduler": config["scheduler"],
            "num_inference_steps": config["steps"],
            "guidance_scale": config["scale"],
        }
        
        if seed:
            payload["seed"] = seed
        
        headers = {"x-api-key": self.api_key}
        
        response = await self.client.post(
            config["url"],
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        
        result = response.json()
        
        if "image_url" in result:
            return result["image_url"]
        elif "images" in result and len(result["images"]) > 0:
            return result["images"][0]
        else:
            raise ValueError(f"Unexpected response: {result}")
    
    async def generate_avatar_set(
        self,
        character_type: CharacterType,
        description: str,
        expressions: Optional[List[str]] = None,
        base_seed: Optional[int] = None,
    ) -> Dict[str, str]:
        """Generate complete avatar with multiple expressions"""
        if expressions is None:
            expressions = ["happy", "sad", "angry", "surprised", "neutral"]
        
        expression_urls = {}
        
        for i, expression in enumerate(expressions):
            seed = (base_seed + i) if base_seed else None
            
            try:
                url = await self.generate_expression(
                    character_type=character_type,
                    description=description,
                    expression=expression,
                    seed=seed,
                )
                expression_urls[expression] = url
                logger.info(f"Generated {expression} expression")
            except Exception as e:
                logger.error(f"Failed to generate {expression}: {e}")
                raise
        
        return expression_urls
    
    async def close(self):
        await self.client.aclose()


avatar_service = AvatarService()