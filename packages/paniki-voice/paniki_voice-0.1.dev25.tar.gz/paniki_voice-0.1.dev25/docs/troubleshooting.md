# Troubleshooting Guide

## Common Issues and Solutions

### Audio Issues

#### No Audio Input

**Symptoms:**
- No audio being captured
- VAD not detecting voice

**Solutions:**
1. Check device permissions:
```python
import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
```

2. Verify VAD configuration:
```python
from paniki.audio.vad.silero import SileroVADAnalyzer

vad = SileroVADAnalyzer()
vad.set_threshold(0.5)  # Adjust sensitivity
```

#### Audio Quality Issues

**Symptoms:**
- Poor audio quality
- Noise in audio

**Solutions:**
1. Apply noise reduction:
```python
from paniki.audio.filters.noisereduce_filter import NoiseReduceFilter

filter = NoiseReduceFilter(
    prop_decrease=0.95,
    n_fft=1024
)
```

2. Adjust resampling:
```python
from paniki.audio.resamplers.soxr_resampler import SoxrResampler

resampler = SoxrResampler(
    quality="high",
    num_channels=1
)
```

### WebRTC Issues

#### Connection Failures

**Symptoms:**
- Failed to establish WebRTC connection
- ICE connection errors

**Solutions:**
1. Check STUN/TURN configuration:
```python
webrtc_config = {
    "iceServers": [
        {"urls": "stun:stun.l.google.com:19302"},
        {
            "urls": "turn:your-turn-server",
            "username": "username",
            "credential": "password"
        }
    ]
}
```

2. Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Media Stream Issues

**Symptoms:**
- No media stream
- Stream interruptions

**Solutions:**
1. Check media constraints:
```python
media_constraints = {
    "audio": {
        "echoCancellation": True,
        "noiseSuppression": True,
        "autoGainControl": True
    }
}
```

### AI Service Issues

#### API Rate Limits

**Symptoms:**
- Service requests failing
- Rate limit errors

**Solutions:**
1. Implement rate limiting:
```python
from paniki.utils.network import RateLimiter

rate_limiter = RateLimiter(
    max_requests=60,
    time_window=60  # seconds
)
```

2. Use multiple API keys:
```python
api_keys = [key1, key2, key3]
current_key_index = 0

def get_next_api_key():
    global current_key_index
    key = api_keys[current_key_index]
    current_key_index = (current_key_index + 1) % len(api_keys)
    return key
```

#### Response Timeouts

**Symptoms:**
- Long response times
- Request timeouts

**Solutions:**
1. Configure timeouts:
```python
from paniki.services.openai import OpenAILLMService

llm = OpenAILLMService(
    api_key="your-key",
    timeout=30,  # seconds
    max_retries=3
)
```

### Pipeline Issues

#### Memory Leaks

**Symptoms:**
- Increasing memory usage
- Performance degradation

**Solutions:**
1. Implement cleanup:
```python
async def cleanup_resources():
    await transport.close()
    await pipeline.cleanup()
    gc.collect()
```

2. Monitor memory usage:
```python
from paniki.metrics import MemoryMetrics

metrics = MemoryMetrics()
pipeline.add_observer(metrics)
```

#### Pipeline Deadlocks

**Symptoms:**
- Pipeline hanging
- Tasks not completing

**Solutions:**
1. Add timeouts:
```python
from paniki.pipeline.task import PipelineTask, PipelineParams

task = PipelineTask(
    pipeline,
    params=PipelineParams(
        max_idle_time=30.0,
        max_response_time=10.0
    ),
)
```

2. Implement health checks:
```python
async def check_pipeline_health():
    if not pipeline.is_healthy():
        await pipeline.restart()
```

## Debugging Tools

### Logging

```python
from loguru import logger

logger.add(
    "debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 MB"
)
```

### Metrics Collection

```python
from paniki.metrics import PipelineMetrics
from prometheus_client import start_http_server

metrics = PipelineMetrics()
start_http_server(8000)
```

### Performance Profiling

```python
import cProfile
import pstats

def profile_pipeline():
    profiler = cProfile.Profile()
    profiler.enable()
    # Run pipeline
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
```

## Support Resources

- GitHub Issues: [Paniki Issues](https://github.com/anak10thn/paniki/issues)
- Documentation: [Paniki Docs](https://github.com/anak10thn/paniki/docs)
- Community Support: [Discord Server](https://discord.gg/paniki)