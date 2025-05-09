"""
Configuration classes for the aiOla streaming service.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Literal, TypedDict, Callable

class AiolaSocketNamespace(str, Enum):
    """Enumeration of available Socket.IO namespaces for the aiOla streaming service."""
    EVENTS = "/events"

@dataclass
class MicConfig:
    """Configuration for the microphone input."""
    sample_rate: int = 16000
    chunk_size: int = 4096
    channels: int = 1

@dataclass
class VadConfig:
    """Configuration for voice activity detection."""
    vad_threshold: float = 0.5
    min_silence_duration_ms: int = 250

class AiolaSocketEvents(TypedDict, total=False):
    """Events for the aiOla streaming service."""
    on_transcript: Callable[[Dict], None]
    on_events: Callable[[Dict], None]
    on_connect: Callable[[Literal["polling", "websocket"]], None]
    on_disconnect: Callable[[], None]
    on_start_record: Callable[[], None]
    on_stop_record: Callable[[], None]
    on_keyword_set: Callable[[List[str]], None]
    on_error: Callable[["AiolaSocketError"], None]

@dataclass
class AiolaSocketConfig:
    """Configuration for the aiOla streaming service."""
    base_url: str
    api_key: str
    query_params: Dict[str, str]
    namespace: Optional[AiolaSocketNamespace] = None
    mic_config: Optional[MicConfig] = None
    vad_config: Optional[VadConfig] = None
    events: Optional[AiolaSocketEvents] = None
    transports: Literal["polling", "websocket", "all"] = "all" 