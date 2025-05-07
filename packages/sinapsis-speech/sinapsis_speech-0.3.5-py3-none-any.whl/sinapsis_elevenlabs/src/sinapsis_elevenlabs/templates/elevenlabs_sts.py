# -*- coding: utf-8 -*-
"""Speech-To-Speech template for ElevenLabs"""

from typing import Callable, Iterator, Literal

from sinapsis_core.data_containers.data_packet import AudioPacket

from sinapsis_elevenlabs.helpers.voice_utils import create_voice_settings, get_voice_id
from sinapsis_elevenlabs.templates.elevenlabs_base import ElevenLabsBase


class ElevenLabsSTS(ElevenLabsBase):
    """Template to interact with ElevenLabs speech-to-speech API."""

    PACKET_TYPE_NAME: str = "audios"

    class AttributesBaseModel(ElevenLabsBase.AttributesBaseModel):
        """Attributes specific to ElevenLabs STS API interaction.

        This class overrides the base attributes of `ElevenLabsBase` to define
        default models specific to the ElevenLabs STS system.
        """

        model: Literal["eleven_english_sts_v2", "eleven_multilingual_sts_v2"] = "eleven_multilingual_sts_v2"

    def synthesize_speech(self, input_data: list[AudioPacket]) -> Iterator[bytes]:
        """
        Sends an audio input to the ElevenLabs API for speech-to-speech synthesis.

        This method processes the provided audio input using the specified voice, model,
        and settings to generate a new audio response.
        """

        try:
            method: Callable[..., Iterator[bytes]] = (
                self.client.speech_to_speech.convert_as_stream
                if self.attributes.stream
                else self.client.speech_to_speech.convert
            )
            return method(
                audio=input_data[0].content,
                voice_id=get_voice_id(self.client, voice=self.attributes.voice),
                model_id=self.attributes.model,
                voice_settings=create_voice_settings(self.attributes.voice_settings),
                output_format=self.attributes.output_format,
                optimize_streaming_latency=str(self.attributes.streaming_latency),
            )
        except ValueError as e:
            self.logger.error(f"Value error synthesizing speech: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Type error in input data or parameters: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Missing key in input data or settings: {e}")
            raise
