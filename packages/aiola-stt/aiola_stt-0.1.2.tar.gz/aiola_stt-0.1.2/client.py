"""
AiolaStreamingClient - Main client for handling audio streaming and Socket.IO connections.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, AsyncGenerator
from urllib.parse import urlencode

import numpy as np
import socketio
import sounddevice as sd

from .config import (
    MicConfig,
    VadConfig,
    AiolaSocketConfig,
)
from .errors import AiolaSocketError, AiolaSocketErrorCode  


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("aiola_streaming_sdk")

class AiolaSttClient:
    """
    Client for streaming audio and handling real-time transcription.
    """

    async def connect(self, auto_record: bool = False, custom_stream_generator: Optional[AsyncGenerator[bytes, None]] = None) -> None:
        """
        Connect to the aiOla streaming service
        
        Args:
            auto_record (bool): If True, automatically start recording/streaming after connection
            custom_stream_generator: Optional async generator for custom audio streaming.
                                   If auto_record is True:
                                   - If provided: uses the custom generator for streaming
                                   - If None: uses the built-in microphone for recording
        """
        try:            
            # Only cleanup if there's an existing connection
            if self.sio and self.sio.connected:
                await self._cleanup_socket()

            # Build connection URL and parameters
            base_url = self.config.base_url
            params = {
                **self.config.query_params,
                "x-aiola-api-key": self.config.api_key,
                "vad_config": json.dumps({
                    "vad_threshold": self.config.vad_config.vad_threshold,
                    "min_silence_duration_ms": self.config.vad_config.min_silence_duration_ms
                }),
                "lang_code": "en_US",  # Default language code (using underscore instead of dash)
                "time_zone": "UTC"      # Default time zone
            }

            # Encode parameters into URL
            url = f"{base_url}/?{urlencode(params)}"

            # Configure transports
            _transports = (
                ["polling"]
                if self.config.transports == "polling"
                else (
                    ["polling", "websocket"]
                    if self.config.transports == "websocket"
                    else ["polling", "websocket"]
                )
            )

            # Connect to the server
            await self.sio.connect(
                url=url,
                headers={"Authorization": f"Bearer {self.config.api_key}"},
                transports=_transports,
                socketio_path="/api/voice-streaming/socket.io",
                namespaces=[self.config.namespace.value]
            )

            if auto_record:
                self.start_recording(custom_stream_generator)

            # If there are active keywords, resend them on reconnection
            if self.active_keywords:
                await self.set_keywords(self.active_keywords)

        except Exception as e:
            self._handle_error(
                f"Failed to connect: {str(e)}",
                AiolaSocketErrorCode.NETWORK_ERROR,
                {"original_error": str(e)}
            )
            await self._cleanup_socket()
            raise
        
    async def disconnect(self) -> None:
        """Disconnect from the server and clean up resources."""
        await self.stop_recording()
        await self._cleanup_socket()
        
    def get_active_keywords(self) -> List[str]:
        """Get the currently active keywords"""
        return self.active_keywords.copy()

    def start_recording(self, custom_stream_generator: Optional[AsyncGenerator[bytes, None]] = None) -> None:
        """
        Start recording/streaming audio.
        
        Args:
            custom_stream_generator: Optional async generator for custom audio streaming.
                                   If provided, uses the custom generator for streaming.
                                   If None, uses the built-in microphone for recording.
        """
        print("Starting recording")
        if not self.sio or not self.sio.connected:
            logger.error("Cannot start recording: Socket is not connected")
            self._handle_error(
                "Socket is not connected. Please call connect first.",
                AiolaSocketErrorCode.MIC_ERROR
            )
            return

        if self.recording_in_progress:
            logger.warning("Recording is already in progress")
            self._handle_error(
                "Recording is already in progress. Please stop the current recording first.",
                AiolaSocketErrorCode.MIC_ALREADY_IN_USE
            )
            return

        try:
            self.recording_in_progress = True
            if self.config.events.get("on_start_record"):
                self.config.events["on_start_record"]()

            # Create the appropriate streaming task
            if custom_stream_generator:
                self._streaming_task = asyncio.create_task(self._start_stream(custom_stream_generator))
            else:
                # Create microphone generator without awaiting it
                mic_generator = self._create_mic_stream_generator()
                self._streaming_task = asyncio.create_task(self._start_stream(mic_generator))

        except Exception as e:
            self.recording_in_progress = False
            self.stop_recording()
            self._handle_error(
                f"Error starting recording: {str(e)}",
                AiolaSocketErrorCode.MIC_ERROR,
                {"original_error": str(e)}
            )

    async def stop_recording(self) -> None:
        """Stop recording audio"""
        if self.is_stopping_recording:
            return

        try:
            self.is_stopping_recording = True
            if self.config.events.get("on_stop_record"):
                self.config.events["on_stop_record"]()

            if self._streaming_task:
                self._streaming_task.cancel()
                try:
                    await self._streaming_task
                except asyncio.CancelledError:
                    pass
                self._streaming_task = None

            if self.audio_stream:
                self.audio_stream.stop()
                self.audio_stream.close()
                self.audio_stream = None

        except Exception as e:
            self._handle_error(
                f"Error stopping microphone recording: {str(e)}",
                AiolaSocketErrorCode.MIC_ERROR,
                {"original_error": str(e)}
            )
        finally:
            self.recording_in_progress = False
            self.is_stopping_recording = False

    async def set_keywords(self, keywords: List[str]) -> None:
        """
        Set keywords for speech recognition.

        Args:
            keywords (List[str]): List of keywords to spot in the audio stream
        """
        if not isinstance(keywords, list):
            raise AiolaSocketError(
                "Keywords must be a valid list",
                AiolaSocketErrorCode.KEYWORDS_ERROR
            )

        # Allow empty list to clear keywords
        if not keywords:
            self.active_keywords = []
            if self.sio and self.sio.connected:
                await self.sio.emit("set_keywords", "", namespace=self.config.namespace.value)
            return

        valid_keywords = [k.strip() for k in keywords if k.strip()]

        if not valid_keywords:
            raise AiolaSocketError(
                "At least one valid keyword must be provided",
                AiolaSocketErrorCode.KEYWORDS_ERROR
            )

        self.active_keywords = valid_keywords

        if not self.sio or not self.sio.connected:
            return

        try:
            binary_data = json.dumps(valid_keywords).encode()
            await self.sio.emit("set_keywords", binary_data, namespace=self.config.namespace.value)
            if self.config.events.get("on_keyword_set"):
                self.config.events["on_keyword_set"](valid_keywords)

        except Exception as e:
            logger.error(f"Error setting keywords: {e}")
            self._handle_error(
                f"Error setting keywords: {str(e)}",
                AiolaSocketErrorCode.KEYWORDS_ERROR,
                {"original_error": str(e)}
            )
            raise
        
    def __init__(self, config: AiolaSocketConfig):
        """
        Initialize the streaming client.

        Args:
            config (AiolaSocketConfig): Configuration for the streaming client
        """
        self.config = config
        self.config.mic_config = config.mic_config or MicConfig()
        self.config.vad_config = config.vad_config or VadConfig()
        self.config.events = config.events or {}
        self.namespace = config.namespace
        
        self.sio = socketio.AsyncClient()
        self.audio_stream: Optional[sd.RawInputStream] = None
        self.recording_in_progress: bool = False
        self.is_stopping_recording: bool = False
        self.active_keywords: List[str] = []
        self._streaming_task: Optional[asyncio.Task] = None
        self._setup_event_handlers()
        
    async def _stream_audio_data(self, audio_data: bytes) -> None:
        """
        Stream custom audio data to the server.

        Args:
            audio_data (bytes): Raw audio data to stream. Should match the configured audio format
                              (sample_rate, channels, dtype as specified in mic_config)
        """
        if not self.sio or not self.sio.connected:
            logger.error("Cannot stream audio: Socket is not connected")
            self._handle_error(
                "Socket is not connected. Please call connect first.",
                AiolaSocketErrorCode.STREAMING_ERROR
            )
            return

        try:
            await self.sio.emit("binary_data", audio_data, namespace=self.config.namespace)
        except Exception as e:
            logger.error(f"Error streaming audio data: {e}")
            self._handle_error(
                f"Error streaming audio data: {str(e)}",
                AiolaSocketErrorCode.STREAMING_ERROR,
                {"original_error": str(e)}
            )

    async def _start_stream(self, stream_generator: AsyncGenerator[bytes, None]) -> None:
        """Start streaming audio from a stream generator
        
        Args:
            stream_generator: An async generator that yields audio data chunks in bytes format
        """
        chunk_count = 0
        print("Starting stream")

        try:
            async for audio_bytes in stream_generator:
                if not self.sio or not self.sio.connected:
                    break
                chunk_count += 1
                await self._stream_audio_data(audio_bytes)

        except Exception as e:
            self._handle_error(
                f"Error in audio streaming: {str(e)}",
                AiolaSocketErrorCode.STREAMING_ERROR,
                {"original_error": str(e)}
            )
        finally:
            logger.info(f"Audio streaming stopped. Total chunks sent: {chunk_count}")
            self.recording_in_progress = False
            if self.config.events.get("on_stop_record"):
                self.config.events["on_stop_record"]()
            await self.stop_recording()

    async def _create_mic_stream_generator(self) -> AsyncGenerator[bytes, None]:
        """Create an async generator that yields audio data from the microphone"""
        loop = asyncio.get_event_loop()
        queue = asyncio.Queue()

        def audio_callback(data, frames, time, status):
            """Handle audio data from the microphone"""
            if status:
                if self.config.events.get("on_error"):
                    self.config.events["on_error"]({"audio_status": status})

            if data is not None:
                loop.call_soon_threadsafe(queue.put_nowait, bytes(data))
            else:
                logger.warning("No audio data received in callback")

        # Create and start the audio stream
        self.audio_stream = sd.RawInputStream(
            samplerate=self.config.mic_config.sample_rate,
            channels=self.config.mic_config.channels,
            blocksize=self.config.mic_config.chunk_size,
            dtype=np.int16,
            callback=audio_callback
        )
        self.audio_stream.start()

        try:
            while True:
                audio_bytes = await queue.get()
                yield audio_bytes
        finally:
            if self.audio_stream:
                self.audio_stream.stop()
                self.audio_stream.close()
                self.audio_stream = None

    # Internal methods below this line
    def _setup_event_handlers(self) -> None:
        """Set up Socket.IO event handlers"""
        if not self.sio:
            return

        @self.sio.event(namespace="/events")
        async def connect():
            """Handle connection event."""
            if self.config.events.get("on_connect"):
                transport = self.sio.transport
                if transport:
                    self.config.events["on_connect"](transport)
                else:
                    self.config.events["on_connect"]("unknown")

        @self.sio.event(namespace="/events")
        async def error(error):
            """Handle error events."""
            self._handle_error(
                f"Socket error: {str(error)}",
                AiolaSocketErrorCode.GENERAL_ERROR,
                {"original_error": str(error)}
            )

        @self.sio.event(namespace="/events")
        async def connect_error(error):
            """Handle connection error events."""
            self._handle_error(
                f"Socket connection error: {str(error)}",
                AiolaSocketErrorCode.NETWORK_ERROR,
                {"original_error": str(error)}
            )

        @self.sio.event(namespace="/events")
        async def disconnect():
            """Handle disconnection event."""
            if self.config.events.get("on_disconnect"):
                self.config.events["on_disconnect"]()

        @self.sio.event(namespace="/events")
        async def transcript(data, ack=None):
            """Handle transcript events."""
            if self.config.events.get("on_transcript"):
                self.config.events["on_transcript"](data)
            if ack:
                await ack({"status": "received"})

        @self.sio.event(namespace="/events")
        async def events(data, ack=None):
            """Handle general events."""
            if self.config.events.get("on_events"):
                self.config.events["on_events"](data)
            if ack:
                await ack({"status": "received"})

    def _handle_error(
        self,
        message: str,
        code: AiolaSocketErrorCode = AiolaSocketErrorCode.GENERAL_ERROR,
        details: Optional[Dict] = None
    ) -> None:
        """Handle error by logging it and emitting the error event"""
        error = AiolaSocketError(message, code, details)
        print(f"Error: {error}")
        if self.config.events.get("on_error"):
            self.config.events["on_error"](error)
            
    async def _cleanup_socket(self) -> None:
        """Clean up socket connection and resources"""
        if self.recording_in_progress:
            await self.stop_recording()

        if self.sio:
            try:
                if self.sio.connected:
                    await self.sio.disconnect()
            except Exception:
                pass  # Ignore disconnect errors during cleanup
            finally:
                self.sio = None

        if self.config.events.get("on_disconnect"):
            self.config.events["on_disconnect"]()