# TrainLoop Evals SDK

A lightweight Python SDK for collecting, submitting, and evaluating LLM responses with TrainLoop.

## Installation

```bash
pip install trainloop-evals-sdk
```

## Usage

### Data Collection

```python
from trainloop_evals import collect

# Set this up during the initialization of your application
# to collect data from all LLM calls
collect()

# Annotate llm calls with the trainloop_tag parameter
# the sdk will intelligently remove the parameter and collect information about the llm call
import openai

openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "2+2"}],
    trainloop_tag="math.addition"
)
```

## Configuration

The SDK can be configured using environment variables:
- `TRAINLOOP_DATA_FOLDER`: Directory where the registry file will be saved. If this is not set, `collect()` becomes a no-op.

## Advanced Usage

See the [documentation](https://docs.trainloop.ai/evals/sdk) for complete API reference.
