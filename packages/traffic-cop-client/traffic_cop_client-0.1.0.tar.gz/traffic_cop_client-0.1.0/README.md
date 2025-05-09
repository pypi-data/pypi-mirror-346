# Traffic Cop Python Client

[![PyPI version](https://badge.fury.io/py/traffic-cop-client.svg)](https://badge.fury.io/py/traffic-cop-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client for the Traffic Cop API, an intelligent middleware for optimizing LLM API usage.

## What is Traffic Cop?

Traffic Cop is a middleware SaaS that optimizes LLM API usage by intelligently routing requests through cost-effective 'Draft' models and high-fidelity 'Verify' models. It helps you:

- **Reduce LLM API costs** by using smaller models when appropriate
- **Maintain high quality** by verifying with larger models when needed
- **Collect valuable data** on model performance and confidence
- **Optimize your LLM strategy** with data-driven insights

Traffic Cop supports two execution modes:
1. **Advise Mode** (default): Traffic Cop provides recommendations, your application executes the LLM calls
2. **Proxy Mode**: Traffic Cop executes the LLM calls on your behalf

## Installation

```bash
pip install traffic-cop-client
```

## Usage

Traffic Cop supports two execution modes:

- **Advise Mode** (default): Traffic Cop provides recommendations on whether to use a draft model or verify model, but the client executes the LLM calls.
- **Proxy Mode**: Traffic Cop executes the LLM calls on behalf of the client.

### Advise Mode (Client Executes LLM Calls)

Advise Mode is the default and recommended mode for most users. In this mode:

1. Traffic Cop provides recommendations on whether to use a draft model or verify model
2. Your application executes the LLM calls based on this advice
3. You report the outcome back to Traffic Cop to help improve future recommendations

#### Example with OpenAI

```python
import asyncio
import openai
from traffic_cop_client import TrafficCopClient, ExecutionMode

async def main():
    # Initialize clients
    traffic_cop = TrafficCopClient(api_key="your-traffic-cop-api-key")
    openai_client = openai.AsyncClient(api_key="your-openai-api-key")

    prompt = "What is the capital of France?"
    draft_model_id = "gpt-3.5-turbo"
    verify_model_id = "gpt-4"

    # Step 1: Get advice from Traffic Cop
    advice = await traffic_cop.route(
        prompt=prompt,
        draft_model_id=draft_model_id,
        verify_model_id=verify_model_id,
        execution_mode=ExecutionMode.ADVISE,  # Default, can be omitted
        user_id="user-123",  # Optional, will be generated if not provided
        metadata={  # Optional
            "source": "web-app",
            "session_id": "session-456",
        },
    )

    print(f"Decision: {advice['decision']}")
    print(f"Suggested draft model: {advice['suggested_draft_model_id']}")
    print(f"Suggested verify model: {advice['suggested_verify_model_id']}")

    # Step 2: Execute the draft model call
    start_time = asyncio.get_event_loop().time()
    draft_response = await openai_client.chat.completions.create(
        model=draft_model_id,
        messages=[{"role": "user", "content": prompt}]
    )
    draft_latency_ms = int((asyncio.get_event_loop().time() - start_time) * 1000)

    draft_content = draft_response.choices[0].message.content
    draft_token_count = draft_response.usage.total_tokens

    print(f"Draft response: {draft_content}")

    # Step 3: Decide whether to verify based on Traffic Cop's advice
    should_verify = advice['decision'] == 'verification_recommended'
    verify_content = None
    verify_token_count = None
    verify_latency_ms = None

    if should_verify:
        # Execute the verify model call
        start_time = asyncio.get_event_loop().time()
        verify_response = await openai_client.chat.completions.create(
            model=verify_model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        verify_latency_ms = int((asyncio.get_event_loop().time() - start_time) * 1000)

        verify_content = verify_response.choices[0].message.content
        verify_token_count = verify_response.usage.total_tokens

        print(f"Verify response: {verify_content}")

    # Step 4: Choose the final response
    final_content = verify_content if should_verify else draft_content

    # Step 5: Report the outcome back to Traffic Cop
    outcome = await traffic_cop.report_execution_outcome(
        traffic_cop_request_id=advice['traffic_cop_request_id'],
        user_id="user-123",  # Use the same user_id that was passed to route()
        actual_draft_model_used=draft_model_id,
        draft_token_count=draft_token_count,
        draft_latency_ms=draft_latency_ms,
        was_verification_performed=should_verify,
        final_response=final_content,
        actual_verify_model_used=verify_model_id if should_verify else None,
        verify_token_count=verify_token_count,
        verify_latency_ms=verify_latency_ms,
        quality_feedback=0.95,  # Optional feedback score (0-1)
    )

    print(f"Outcome reported: {outcome['success']}")
    print(f"Final response: {final_content}")

asyncio.run(main())
```

#### Synchronous Example

```python
from traffic_cop_client import TrafficCopClient, ExecutionMode
import openai
import time

# Initialize clients
traffic_cop = TrafficCopClient(api_key="your-traffic-cop-api-key")
openai_client = openai.Client(api_key="your-openai-api-key")

prompt = "What is the capital of France?"
draft_model_id = "gpt-3.5-turbo"
verify_model_id = "gpt-4"

# Step 1: Get advice from Traffic Cop
advice = traffic_cop.route_sync(
    prompt=prompt,
    draft_model_id=draft_model_id,
    verify_model_id=verify_model_id
)

print(f"Decision: {advice['decision']}")

# Step 2: Execute the draft model call
start_time = time.time()
draft_response = openai_client.chat.completions.create(
    model=draft_model_id,
    messages=[{"role": "user", "content": prompt}]
)
draft_latency_ms = int((time.time() - start_time) * 1000)

draft_content = draft_response.choices[0].message.content
draft_token_count = draft_response.usage.total_tokens

# Step 3: Decide whether to verify based on Traffic Cop's advice
verification_needed = advice['decision'] == 'verification_recommended'
verify_content = None
verify_token_count = None
verify_latency_ms = None

if verification_needed:
    start_time = time.time()
    verify_response = openai_client.chat.completions.create(
        model=verify_model_id,
        messages=[{"role": "user", "content": prompt}]
    )
    verify_latency_ms = int((time.time() - start_time) * 1000)

    verify_content = verify_response.choices[0].message.content
    verify_token_count = verify_response.usage.total_tokens

# Step 4: Choose the final response
final_content = verify_content if verification_needed else draft_content

# Step 5: Report the execution outcome back to Traffic Cop
traffic_cop.report_execution_outcome_sync(
    traffic_cop_request_id=advice["traffic_cop_request_id"],
    user_id="user-123",  # Use the same user_id that was passed to route() or that was auto-generated
    actual_draft_model_used=draft_model_id,
    draft_token_count=draft_token_count,
    draft_latency_ms=draft_latency_ms,
    was_verification_performed=verification_needed,
    final_response=final_content,
    actual_verify_model_used=verify_model_id if verification_needed else None,
    verify_token_count=verify_token_count,
    verify_latency_ms=verify_latency_ms
)

print(f"Final response: {final_content}")
```

### Proxy Mode (Traffic Cop Executes LLM Calls)

In Proxy Mode, Traffic Cop executes the LLM calls on your behalf. Important notes about API keys:

- **Gemini models**: Traffic Cop can use its own managed API keys for Gemini models (e.g., `gemini-pro`, `text-bison`).
- **Non-Gemini models**: You must provide your own API keys for OpenAI (e.g., `gpt-3.5-turbo`, `gpt-4`) and Anthropic (e.g., `claude-instant`, `claude-2`) models.

```python
import asyncio
from traffic_cop_client import TrafficCopClient, ExecutionMode

async def main():
    client = TrafficCopClient(api_key="your-api-key")

    # Example with OpenAI models (requires customer API key)
    response = await client.route(
        prompt="What is the capital of France?",
        draft_model_id="gpt-3.5-turbo",
        verify_model_id="gpt-4",
        execution_mode=ExecutionMode.PROXY,
        user_id="user-123",  # Optional, will be generated if not provided
        customer_api_keys={  # Required for OpenAI and Anthropic models
            "openai": "sk-your-openai-key",
        },
        metadata={  # Optional
            "source": "web-app",
            "session_id": "session-456",
        },
    )

    # Example with Gemini models (Traffic Cop's managed key can be used)
    gemini_response = await client.route(
        prompt="What is the capital of France?",
        draft_model_id="gemini-pro",
        verify_model_id="gemini-pro-1.5",
        execution_mode=ExecutionMode.PROXY,
        user_id="user-123",
        # No customer_api_keys needed for Gemini models
    )

    print(f"Final response: {response['final_response']}")
    print(f"Verification used: {response['verification_used']}")
    print(f"Estimated cost saved: ${response['estimated_cost_saved']:.6f}")

asyncio.run(main())
```

### Synchronous API

Both execution modes are also available with the synchronous API:

```python
from traffic_cop_client import TrafficCopClient, ExecutionMode

client = TrafficCopClient(api_key="your-api-key")

# Advise mode (default)
advice = client.route_sync(
    prompt="What is the capital of France?",
    draft_model_id="gpt-3.5-turbo",
    verify_model_id="gpt-4",
)

# Proxy mode
response = client.route_sync(
    prompt="What is the capital of France?",
    draft_model_id="gpt-3.5-turbo",
    verify_model_id="gpt-4",
    execution_mode=ExecutionMode.PROXY,
)
```

## Configuration

The client can be configured with the following parameters:

- `api_key`: Your Traffic Cop API key (required)
- `base_url`: The base URL for the Traffic Cop API (default: `https://traffic-cop-api-pbo3cvpjua-uc.a.run.app`)
- `timeout`: Request timeout in seconds (default: 60)

## Response Format

The response from the `route` and `route_sync` methods depends on the execution mode:

### Advise Mode Response

```python
{
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "execution_mode": "advise",
    "traffic_cop_request_id": "789a0123-b45c-67d8-e90f-123456789abc",
    "decision": "verification_recommended",  # or "draft_sufficient"
    "suggested_draft_model_id": "gpt-3.5-turbo",
    "suggested_verify_model_id": "gpt-4",
    "threshold_used": 0.7
}
```

### Proxy Mode Response

```python
{
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "execution_mode": "proxy",
    "traffic_cop_request_id": "789a0123-b45c-67d8-e90f-123456789abc",
    "draft_response": {
        "content": "Paris is the capital of France.",
        "model_id": "gpt-3.5-turbo",
        "tokens_used": 15,
        "latency_ms": 250,
        "confidence": 0.92,
        "metadata": {"provider": "openai"}
    },
    "verify_response": None,  # Present only if verification was used
    "final_response": "Paris is the capital of France.",
    "verification_used": False,
    "estimated_cost_saved": 0.000123,
    "threshold_used": 0.7
}
```

### Report Execution Outcome Response

The response from the `report_execution_outcome` and `report_execution_outcome_sync` methods:

```python
{
    "success": true,
    "traffic_cop_request_id": "789a0123-b45c-67d8-e90f-123456789abc",
    "message": "Execution outcome successfully reported"
}
```

> **Important Note on `user_id`**: When calling `report_execution_outcome`, always use the same `user_id` that was passed to the original `route()` call. This ensures consistent tracking of user interactions across the system. The `user_id` represents the end-user identifier, while `traffic_cop_request_id` is used to correlate the specific request-response pair.

## Error Handling

The client will raise specific exceptions that you can catch to handle different types of errors:

```python
from traffic_cop_client import (
    TrafficCopClient,
    TrafficCopError,
    TrafficCopConnectionError,
    TrafficCopAPIError
)

client = TrafficCopClient(api_key="your-api-key")

try:
    response = client.route_sync(
        prompt="What is the capital of France?",
        draft_model_id="gpt-3.5-turbo",
        verify_model_id="gpt-4",
    )
    print(f"Decision: {response['decision']}")

    # Execute LLM calls based on the advice...

except TrafficCopAPIError as e:
    # Handle API errors (e.g., invalid request, authentication error)
    print(f"API Error (Status {e.status_code}): {e.detail}")
except TrafficCopConnectionError as e:
    # Handle connection errors (e.g., network issues, timeouts)
    print(f"Connection Error: {str(e)}")
except TrafficCopError as e:
    # Handle other Traffic Cop errors
    print(f"Traffic Cop Error: {str(e)}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected Error: {str(e)}")
```

### Exception Types

- `TrafficCopError`: Base exception for all Traffic Cop client errors
- `TrafficCopConnectionError`: Raised for connection errors (network issues, timeouts)
- `TrafficCopAPIError`: Raised when the API returns an error response (includes status_code and detail)

## Contributing

We welcome contributions to the Traffic Cop Python SDK! Please see [CONTRIBUTING.md](https://github.com/traffic-cop/traffic-cop-python-sdk/blob/main/CONTRIBUTING.md) for details on how to contribute.

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/traffic-cop/traffic-cop-python-sdk.git
cd traffic-cop-python-sdk
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=traffic_cop_client

# Run specific test file
pytest tests/test_client.py
```

### Code Style

This project uses:
- [Black](https://black.readthedocs.io/en/stable/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [mypy](https://mypy.readthedocs.io/en/stable/) for type checking

```bash
# Format code
black traffic_cop_client tests
isort traffic_cop_client tests

# Check types
mypy traffic_cop_client
```

## Support

For support, please:
- Open an [issue](https://github.com/traffic-cop/traffic-cop-python-sdk/issues) on GitHub
- Contact us at support@trafficcop.ai
- Visit our [documentation](https://docs.trafficcop.ai)

## License

MIT

## Links

- [Traffic Cop Website](https://trafficcop.ai)
- [Documentation](https://docs.trafficcop.ai)
- [GitHub Repository](https://github.com/traffic-cop/traffic-cop-python-sdk)
