# -*- coding: utf-8 -*-
"""Text-To-Speech template for ElevenLabs"""

from elevenlabs import Voice
from sinapsis_core.data_containers.data_packet import AudioPacket, DataContainer

from sinapsis_elevenlabs.templates.elevenlabs_tts import ElevenLabsTTS


class ElevenLabsVoiceClone(ElevenLabsTTS):
    """Template to clone a voice using ElevenLabs API."""

    class AttributesBaseModel(ElevenLabsTTS.AttributesBaseModel):
        """Attributes specific to the ElevenLabsVoiceClone class."""

        name: str | None = None
        description: str | None = None

    def clone_voice(self, input_data: list[AudioPacket]) -> Voice:
        """Clones a voice using the provided audio files."""
        files = [f.content for f in input_data]
        try:
            add_voice_response = self.client.voices.add(
                name=self.attributes.name,
                description=self.attributes.description,
                files=files,
            )
            cloned_voice = self.client.voices.get(add_voice_response.voice_id)
            self.logger.info(f"Voice cloned successfully: {cloned_voice.name}")
            return cloned_voice
        except ValueError as e:
            self.logger.error(f"Value error in input data or parameters: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Type error with input data or files: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Missing expected key in API response: {e}")
            raise

    def execute(self, container: DataContainer) -> DataContainer:
        """Executes the voice cloning process and generates the speech output."""
        audios = getattr(container, "audios", None)
        if not audios:
            self.logger.debug("No audios provided to clone voice")
            return container
        self.attributes.voice = self.clone_voice(audios)

        container = super().execute(container)

        return container
