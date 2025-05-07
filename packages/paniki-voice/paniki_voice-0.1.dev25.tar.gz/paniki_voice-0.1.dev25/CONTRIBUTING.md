# Contributing to Paniki

Thank you for your interest in contributing to Paniki! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a healthy and inclusive community.

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/paniki.git
cd paniki
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings in Google style
- Keep functions and methods focused and concise
- Use meaningful variable and function names

### Testing

1. Write tests for new features:
```python
import pytest
from paniki.your_module import YourFeature

def test_your_feature():
    feature = YourFeature()
    result = feature.do_something()
    assert result == expected_result
```

2. Run tests:
```bash
pytest
```

3. Check code coverage:
```bash
pytest --cov=paniki tests/
```

### Documentation

1. Update relevant documentation in the `docs/` directory
2. Include docstrings for new classes and functions
3. Add examples for new features
4. Update the changelog

## Pull Request Process

1. Update your fork:
```bash
git remote add upstream https://github.com/anak10thn/paniki.git
git fetch upstream
git rebase upstream/main
```

2. Commit your changes:
```bash
git add .
git commit -m "feat: add your feature description"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request:
   - Use a clear and descriptive title
   - Describe the changes in detail
   - Reference any related issues
   - Update documentation if needed

### Commit Message Guidelines

Follow the Conventional Commits specification:

- feat: A new feature
- fix: A bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- test: Adding or updating tests
- chore: Maintenance tasks

Example:
```
feat(audio): add noise reduction filter

- Add NoiseReduceFilter class
- Implement Spectral Gating algorithm
- Add unit tests
- Update documentation
```

## Development Setup

### Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -e ".[dev,test,docs]"
```

### Running Tests

1. Unit tests:
```bash
pytest tests/unit/
```

2. Integration tests:
```bash
pytest tests/integration/
```

3. With coverage:
```bash
pytest --cov=paniki --cov-report=html tests/
```

### Building Documentation

1. Install documentation dependencies:
```bash
pip install -e ".[docs]"
```

2. Build documentation:
```bash
cd docs
make html
```

## Project Structure

```
paniki/
├── docs/              # Documentation
├── examples/          # Example applications
├── libs/              # Core library code
│   └── paniki/
│       ├── audio/    # Audio processing
│       ├── pipeline/ # Pipeline system
│       └── services/ # Service integrations
├── tests/            # Test suite
└── tools/            # Development tools
```

## Adding New Features

### New Components

1. Create a new component:
```python
from paniki.processors.frame_processor import FrameProcessor

class YourComponent(FrameProcessor):
    """Your component description."""
    
    def __init__(self, config):
        self.config = config
        
    async def process_frame(self, frame):
        # Implementation
```

2. Add tests:
```python
def test_your_component():
    component = YourComponent(config)
    result = await component.process_frame(frame)
    assert result.is_valid()
```

### New Services

1. Create a service class:
```python
from paniki.services.ai_service import AIService

class YourService(AIService):
    """Your service description."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    async def process_frame(self, frame):
        # Implementation
```

2. Add configuration:
```python
from dataclasses import dataclass

@dataclass
class YourServiceConfig:
    """Configuration for your service."""
    api_key: str
    endpoint: str
    timeout: float = 30.0
```

## Release Process

1. Update version:
   - Update version in pyproject.toml
   - Update CHANGELOG.md

2. Create release branch:
```bash
git checkout -b release/v1.0.0
```

3. Run tests and checks:
```bash
pytest
ruff check .
mypy .
```

4. Create release commit:
```bash
git commit -m "release: v1.0.0"
```

5. Create tag:
```bash
git tag -a v1.0.0 -m "Version 1.0.0"
```

6. Push release:
```bash
git push origin release/v1.0.0 --tags
```

## Getting Help

- Create an issue for bugs or feature requests
- Join our community discussions
- Check the documentation
- Contact the maintainers

## License

By contributing to Paniki, you agree that your contributions will be licensed under the MIT License.