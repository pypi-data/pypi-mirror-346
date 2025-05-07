# Paniki

Paniki is an open-source framework for building voice and multimodal assistants. It provides a flexible and extensible architecture for creating AI-powered voice applications with support for various speech-to-text, text-to-speech, and AI model integrations.

## Features

- WebRTC support for real-time audio/video processing
- Integration with multiple AI providers (OpenAI, Anthropic, Google, Azure, etc.)
- Modular architecture for easy extension and customization
- Support for various speech-to-text and text-to-speech services
- Built-in audio processing capabilities
- Cross-platform compatibility

## Installation

```bash
pip install paniki-voice
```

For additional features, you can install optional dependencies:

```bash
# For OpenAI integration
pip install "paniki-voice[openai]"

# For Google Cloud services
pip install "paniki-voice[google]"

# For local audio processing
pip install "paniki-voice[local]"
```

## Quick Start

```python
# Example code coming soon
```

## Optional Dependencies

Paniki supports various optional dependencies for different use cases:

- `[anthropic]` - Anthropic Claude integration
- `[assemblyai]` - AssemblyAI speech recognition
- `[aws]` - Amazon Web Services integration
- `[azure]` - Microsoft Azure Cognitive Services
- `[google]` - Google Cloud services
- `[openai]` - OpenAI integration
- `[local]` - Local audio processing capabilities
- And many more...

Check `pyproject.toml` for the complete list of optional dependencies.

## Documentation

Detailed documentation is available in the [docs](./docs) directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024 Paniki Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.