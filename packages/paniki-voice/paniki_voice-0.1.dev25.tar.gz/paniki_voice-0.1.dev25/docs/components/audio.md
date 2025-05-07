# Audio Components

## Overview

Paniki provides comprehensive audio processing capabilities through various components:

- Voice Activity Detection (VAD)
- Audio Filters
- Audio Mixers
- Audio Resamplers
- Turn Management

## Voice Activity Detection (VAD)

### Silero VAD

```python
from paniki.audio.vad.silero import SileroVADAnalyzer

vad = SileroVADAnalyzer()
```

The Silero VAD provides robust voice activity detection using the Silero model.

## Audio Filters

### Available Filters

1. Koala Filter
```python
from paniki.audio.filters.koala_filter import KoalaFilter

filter = KoalaFilter()
```

2. Krisp Filter
```python
from paniki.audio.filters.krisp_filter import KrispFilter

filter = KrispFilter()
```

3. NoiseReduce Filter
```python
from paniki.audio.filters.noisereduce_filter import NoiseReduceFilter

filter = NoiseReduceFilter()
```

## Audio Mixers

### SoundFile Mixer

```python
from paniki.audio.mixers.soundfile_mixer import SoundFileMixer

mixer = SoundFileMixer()
```

## Audio Resamplers

### Available Resamplers

1. Resampy Resampler
```python
from paniki.audio.resamplers.resampy_resampler import ResampyResampler

resampler = ResampyResampler()
```

2. SoXR Resampler
```python
from paniki.audio.resamplers.soxr_resampler import SoxrResampler

resampler = SoxrResampler()
```

## Turn Management

### Smart Turn Analysis

```python
from paniki.audio.turn.smart_turn import LocalCoreMLSmartTurn

turn_analyzer = LocalCoreMLSmartTurn()
```

Available implementations:
- Local CoreML Smart Turn
- FAL Smart Turn
- HTTP Smart Turn