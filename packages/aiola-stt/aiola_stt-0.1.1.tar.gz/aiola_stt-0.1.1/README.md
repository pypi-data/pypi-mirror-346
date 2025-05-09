# aiOla Speech-To-Text SDK

The aiOla Streaming SDK provides Python bindings for aiOla's real-time streaming services, enabling real-time audio streaming, transcription, and keyword spotting capabilities.

## Features

- Real-time audio streaming with microphone support
- Custom audio stream support
- Real-time transcription
- Keyword spotting
- Voice Activity Detection (VAD)
- Event-driven architecture
- Multi-language support
- Configurable audio parameters
- Error handling and logging

## Installation

```bash
pip install aiola-stt
```

## Usage

### Basic Usage

```python
from aiola_stt import AiolaSttClient, AiolaSocketConfig, AiolaSocketNamespace

# Create configuration
config = AiolaSocketConfig(
    base_url="your-api-key", # i.e https://api.aiola.ai
    namespace=AiolaSocketNamespace.EVENTS,
    api_key="your-api-key",
    query_params={}
)

# Initialize client
client = AiolaSttClient(config)

# Connect and start recording with default built-in microphone
await client.connect(auto_record=True)

# Stop recording
await client.stop_recording()

# Clean up
await client.cleanup_socket()
```

### Event Handling

```python
from aiola_streaming_sdk import AiolaSocketEvents

# Define event handlers
events = AiolaSocketEvents(
    on_transcript=lambda data: print(f"Transcript: {data}"),
    on_connect=lambda transport: print(f"Connected via {transport}"),
    on_disconnect=lambda: print("Disconnected"),
    on_error=lambda error: print(f"Error: {error}"),
    on_start_record=lambda: print("Recording started"),
    on_stop_record=lambda: print("Recording stopped")
)

# Add events to config
config = AiolaSocketConfig(
    base_url="your-api-key", # i.e https://api.aiola.ai
    namespace=AiolaSocketNamespace.EVENTS,
    api_key="your-api-key",
    query_params={},
    events=events
)
```

### Keyword Spotting

```python
# Set keywords to spot in the audio stream
await client.set_keywords(["hello", "world"])

# Get currently active keywords
active_keywords = client.get_active_keywords()
```

### Custom Audio Streaming

```python
async def custom_audio_generator():
    # Your custom audio streaming logic here
    while True:
        audio_data = await get_audio_data()  # Your audio data source
        yield audio_data

# Use custom audio generator
await client.connect(auto_record=True, custom_stream_generator=custom_audio_generator())
```

### Configuration Options

#### Microphone Configuration

```python
from aiola_streaming_sdk import MicConfig

mic_config = MicConfig(
    sample_rate=16000,  # Hz
    chunk_size=4096,    # Samples per chunk
    channels=1          # Mono audio
)
```

#### Voice Activity Detection Configuration

```python
from aiola_streaming_sdk import VadConfig

vad_config = VadConfig(
    vad_threshold=0.5,              # VAD threshold (0.0 to 1.0)
    min_silence_duration_ms=250     # Minimum silence duration
)
```

## Development

To install development dependencies:

```bash
pip install -e ".[dev]"
```

## Error Handling

The SDK provides comprehensive error handling through the `AiolaSocketError` class:

```python
from aiola_streaming_sdk import AiolaSocketError, AiolaSocketErrorCode

try:
    await client.connect()
except AiolaSocketError as e:
    print(f"Error: {e.message}")
    print(f"Error code: {e.code}")
    print(f"Details: {e.details}")
```

## License

MIT License
