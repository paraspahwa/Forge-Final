"""
Voice generation service using Edge TTS (free)
"""

import os
from typing import Optional

import edge_tts

from app.core.logging import get_logger

logger = get_logger(__name__)


# Voice mappings
VOICE_PRESETS = {
    "anime": {
        "female": "en-US-AnaNeural",      # Young, anime-like
        "male": "en-US-BrandonNeural",    # Young male
    },
    "realistic": {
        "female": "en-US-AriaNeural",     # Natural female
        "male": "en-US-GuyNeural",        # Natural male
        "narrator": "en-US-JennyNeural",  # Professional narrator
    },
}


class VoiceService:
    """Generate voice using Edge TTS (completely free)"""
    
    async def generate(
        self,
        text: str,
        character_type: str = "anime",
        gender: str = "female",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Generate voice audio file
        
        Returns:
            Path to generated audio file
        """
        # Select voice
        voice = VOICE_PRESETS.get(character_type, VOICE_PRESETS["realistic"]).get(
            gender, VOICE_PRESETS["realistic"]["female"]
        )
        
        # Generate
        communicate = edge_tts.Communicate(text, voice)
        
        if output_path is None:
            output_path = f"/tmp/voice_{hash(text)}.mp3"
        
        await communicate.save(output_path)
        
        logger.info(f"Generated voice: {output_path} ({len(text)} chars)")
        
        return output_path
    
    async def get_voices(self) -> list:
        """Get list of available voices"""
        voices = await edge_tts.list_voices()
        return [
            {
                "name": v["Name"],
                "gender": v["Gender"],
                "locale": v["Locale"],
            }
            for v in voices
        ]


voice_service = VoiceService()