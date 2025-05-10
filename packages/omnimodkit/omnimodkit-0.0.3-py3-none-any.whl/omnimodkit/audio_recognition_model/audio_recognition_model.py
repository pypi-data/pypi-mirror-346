import io
from typing import Type
from pydantic import BaseModel
from openai import OpenAI
from openai import AsyncOpenAI

from ..base_toolkit_model import BaseToolkitModel
from ..ai_config import AudioRecognition
from ..moderation import ModerationError


class AudioRecognitionModel(BaseToolkitModel):
    model_name = "audio_recognition"

    def get_model_config(self) -> AudioRecognition:
        return self.ai_config.audio_recognition

    def run_impl(
        self,
        system_prompt: str,
        pydantic_model: Type[BaseModel],
        in_memory_audio_stream: io.BytesIO,
    ) -> BaseModel:
        default_pydantic_model = self.get_default_pydantic_model()
        if pydantic_model is not default_pydantic_model:
            raise ValueError(
                f"Image generation requires pydantic_model must be {default_pydantic_model}"
            )
        client = OpenAI(api_key=self.openai_api_key)
        in_memory_audio_stream.seek(0)
        transcript = client.audio.transcriptions.create(
            file=in_memory_audio_stream,
            model=self.get_model().name,
        )
        result = self.get_default_pydantic_model()(
            audio_description=transcript.text,
        )
        # TODO: check moderation before running the model
        if self.moderation_needed and not self.moderate_text(result.model_dump_json()):
            raise ModerationError(
                f"Audio description '{result}' was rejected by the moderation system"
            )
        return result

    async def arun_impl(
        self,
        system_prompt: str,
        pydantic_model: Type[BaseModel],
        in_memory_audio_stream: io.BytesIO,
    ) -> BaseModel:
        default_pydantic_model = self.get_default_pydantic_model()
        if pydantic_model is not default_pydantic_model:
            raise ValueError(
                f"Image generation requires pydantic_model must be {default_pydantic_model}"
            )
        client = AsyncOpenAI(api_key=self.openai_api_key)
        in_memory_audio_stream.seek(0)
        transcript = await client.audio.transcriptions.create(
            file=in_memory_audio_stream,
            model=self.get_model().name,
        )
        result = self.get_default_pydantic_model()(
            audio_description=transcript.text,
        )
        # TODO: check moderation before running the model
        if self.moderation_needed and not self.moderate_text(result.model_dump_json()):
            raise ModerationError(
                f"Audio description '{result}' was rejected by the moderation system"
            )
        return result

    def get_price(
        self,
        audio_length: int,
        *args,
        **kwargs,
    ) -> float:
        input_audio_second_price = self.get_model().rate.input_audio_second_price
        return audio_length * input_audio_second_price
