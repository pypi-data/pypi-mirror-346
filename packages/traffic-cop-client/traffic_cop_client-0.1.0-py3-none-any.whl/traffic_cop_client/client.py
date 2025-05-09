"""Traffic Cop client for Python."""

import hashlib
import json
import logging
import os
import time
from enum import Enum
from typing import Dict, Optional, Union, Any
from uuid import uuid4

# Set environment variable to use native DNS resolver if not already set
if "GRPC_DNS_RESOLVER" not in os.environ:
    os.environ["GRPC_DNS_RESOLVER"] = "native"

import httpx

logger = logging.getLogger(__name__)


class ExecutionMode(str, Enum):
    """Execution mode for the Traffic Cop API."""

    ADVISE = "advise"  # Client executes LLM calls
    PROXY = "proxy"    # Traffic Cop executes LLM calls


class TrafficCopError(Exception):
    """Base exception for all Traffic Cop client errors."""
    pass


class TrafficCopConnectionError(TrafficCopError):
    """Exception raised for connection errors when communicating with the Traffic Cop API."""
    pass


class TrafficCopAPIError(TrafficCopError):
    """Exception raised for API errors returned by the Traffic Cop API."""

    def __init__(self, status_code: int, detail: str, *args: Any):
        self.status_code = status_code
        self.detail = detail
        message = f"API error (status code {status_code}): {detail}"
        super().__init__(message, *args)


class TrafficCopClient:
    """Client for interacting with the Traffic Cop API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://traffic-cop-api-pbo3cvpjua-uc.a.run.app",
        timeout: int = 60,
        verify_ssl: bool = True,
        default_execution_mode: Union[ExecutionMode, str] = ExecutionMode.ADVISE,
    ):
        """Initialize the Traffic Cop client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the Traffic Cop API
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates (default: True)
            default_execution_mode: Default execution mode to use (default: 'advise')

        Raises:
            ValueError: If api_key is empty or not a string
        """
        # Validate api_key
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key must be a non-empty string")

        # Validate base_url
        if not base_url or not isinstance(base_url, str):
            raise ValueError("Base URL must be a non-empty string")

        # Validate timeout
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("Timeout must be a positive integer")

        # Validate verify_ssl
        if not isinstance(verify_ssl, bool):
            raise ValueError("verify_ssl must be a boolean")

        # Validate default_execution_mode
        if isinstance(default_execution_mode, str):
            if default_execution_mode not in [ExecutionMode.ADVISE, ExecutionMode.PROXY]:
                raise ValueError(f"Execution mode must be either 'advise' or 'proxy', got '{default_execution_mode}'")
            self.default_execution_mode = default_execution_mode
        else:
            self.default_execution_mode = default_execution_mode.value

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Initialize provider-specific API clients to None
        # They will be lazily initialized when needed
        self._openai_client = None
        self._anthropic_client = None
        self._vertex_ai_initialized = False

    async def execute_llm_call(
        self,
        provider: str,
        model_id: str,
        prompt: str,
        api_key: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """Execute an LLM call to the specified provider.

        Args:
            provider: The provider to use (e.g., 'openai', 'anthropic', 'vertexai')
            model_id: The model ID to use
            prompt: The prompt to send
            api_key: Optional API key for the provider
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict: The response from the LLM provider including:
                - content: The generated text
                - tokens_used: Total tokens used
                - latency_ms: Time taken in milliseconds

        Raises:
            ValueError: If the provider is not supported
            TrafficCopError: If there's an error with the LLM call
        """
        start_time = time.time()

        try:
            if provider.lower() == "openai":
                response = await self._execute_openai_call(
                    model_id=model_id,
                    prompt=prompt,
                    api_key=api_key,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
            elif provider.lower() == "anthropic":
                response = await self._execute_anthropic_call(
                    model_id=model_id,
                    prompt=prompt,
                    api_key=api_key,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
            elif provider.lower() == "vertexai":
                response = await self._execute_vertexai_call(
                    model_id=model_id,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
            else:
                raise ValueError(f"Unsupported provider: {provider}")

            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000)

            # Add latency to the response
            response["latency_ms"] = latency_ms

            return response

        except Exception as e:
            logger.error(f"Error executing LLM call to {provider}: {str(e)}")
            raise TrafficCopError(f"Error executing LLM call: {str(e)}")

    def execute_llm_call_sync(
        self,
        provider: str,
        model_id: str,
        prompt: str,
        api_key: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """Synchronous version of execute_llm_call method.

        Args:
            provider: The provider to use (e.g., 'openai', 'anthropic', 'vertexai')
            model_id: The model ID to use
            prompt: The prompt to send
            api_key: Optional API key for the provider
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict: The response from the LLM provider including:
                - content: The generated text
                - tokens_used: Total tokens used
                - latency_ms: Time taken in milliseconds

        Raises:
            ValueError: If the provider is not supported
            TrafficCopError: If there's an error with the LLM call
        """
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # If no event loop is available, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            self.execute_llm_call(
                provider=provider,
                model_id=model_id,
                prompt=prompt,
                api_key=api_key,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
        )

    async def _execute_openai_call(
        self,
        model_id: str,
        prompt: str,
        api_key: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """Execute an LLM call to OpenAI.

        Args:
            model_id: The model ID to use
            prompt: The prompt to send
            api_key: Optional API key for OpenAI
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            **kwargs: Additional OpenAI-specific parameters

        Returns:
            Dict: The response from OpenAI
        """
        try:
            import openai

            # Set the API key
            if api_key:
                openai.api_key = api_key

            # Prepare the request parameters
            params = {
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
            }

            if max_tokens is not None:
                params["max_tokens"] = max_tokens

            # Add any additional parameters
            params.update(kwargs)

            # Make the API call
            response = await openai.ChatCompletion.acreate(**params)

            # Extract the relevant information
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            return {
                "content": content,
                "tokens_used": tokens_used,
                "model_id": model_id,
                "provider": "openai",
            }

        except ImportError:
            raise TrafficCopError("OpenAI package not installed. Install it with 'pip install openai'.")
        except Exception as e:
            raise TrafficCopError(f"Error calling OpenAI API: {str(e)}")

    async def _execute_anthropic_call(
        self,
        model_id: str,
        prompt: str,
        api_key: Optional[str] = None,
        max_tokens: Optional[int] = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """Execute an LLM call to Anthropic.

        Args:
            model_id: The model ID to use
            prompt: The prompt to send
            api_key: Optional API key for Anthropic
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            **kwargs: Additional Anthropic-specific parameters

        Returns:
            Dict: The response from Anthropic
        """
        try:
            import anthropic

            # Create the client
            client = anthropic.Client(api_key=api_key) if api_key else anthropic.Client()

            # Prepare the request parameters
            params = {
                "prompt": f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
                "model": model_id,
                "max_tokens_to_sample": max_tokens,
                "temperature": temperature,
            }

            # Add any additional parameters
            params.update(kwargs)

            # Make the API call
            response = client.completion(**params)

            # Extract the relevant information
            content = response.completion

            # Anthropic doesn't provide token usage, so we'll estimate it
            # This is a rough estimate and should be replaced with a proper token counter
            tokens_used = len(prompt.split()) + len(content.split())

            return {
                "content": content,
                "tokens_used": tokens_used,
                "model_id": model_id,
                "provider": "anthropic",
            }

        except ImportError:
            raise TrafficCopError("Anthropic package not installed. Install it with 'pip install anthropic'.")
        except Exception as e:
            raise TrafficCopError(f"Error calling Anthropic API: {str(e)}")

    async def _execute_vertexai_call(
        self,
        model_id: str,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """Execute an LLM call to Google Vertex AI.

        Args:
            model_id: The model ID to use
            prompt: The prompt to send
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            **kwargs: Additional Vertex AI-specific parameters

        Returns:
            Dict: The response from Vertex AI
        """
        try:
            from google.cloud import aiplatform
            from vertexai.preview.generative_models import GenerativeModel

            # Initialize Vertex AI if not already initialized
            if not self._vertex_ai_initialized:
                aiplatform.init()
                self._vertex_ai_initialized = True

            # Create the model
            model = GenerativeModel(model_id)

            # Prepare the generation config
            generation_config = {}
            if max_tokens is not None:
                generation_config["max_output_tokens"] = max_tokens
            generation_config["temperature"] = temperature

            # Add any additional parameters to the generation config
            generation_config.update(kwargs.get("generation_config", {}))

            # Make the API call
            response = model.generate_content(
                prompt,
                generation_config=generation_config,
                **{k: v for k, v in kwargs.items() if k != "generation_config"}
            )

            # Extract the relevant information
            content = response.text

            # Vertex AI doesn't provide token usage, so we'll estimate it
            # This is a rough estimate and should be replaced with a proper token counter
            tokens_used = len(prompt.split()) + len(content.split())

            return {
                "content": content,
                "tokens_used": tokens_used,
                "model_id": model_id,
                "provider": "vertexai",
            }

        except ImportError:
            raise TrafficCopError("Google Cloud AI Platform packages not installed. Install them with 'pip install google-cloud-aiplatform'.")
        except Exception as e:
            raise TrafficCopError(f"Error calling Vertex AI API: {str(e)}")

    async def execute_with_advice(
        self,
        prompt: str,
        draft_model_id: str,
        verify_model_id: str,
        user_id: Optional[str] = None,
        customer_api_keys: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """Execute LLM calls based on Traffic Cop's advice.

        This method:
        1. Gets advice from Traffic Cop on whether to use the draft or verify model
        2. Executes the appropriate LLM call(s) based on the advice
        3. Reports the execution outcome back to Traffic Cop

        Args:
            prompt: The prompt to send to the LLM
            draft_model_id: Identifier for the draft model to use
            verify_model_id: Identifier for the verify model to use
            user_id: Unique identifier for the user (default: random UUID)
            customer_api_keys: Optional API keys for the LLM providers
            metadata: Optional metadata to include with the request
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict: The final response including:
                - content: The generated text
                - verification_used: Whether verification was used
                - draft_response: The response from the draft model
                - verify_response: The response from the verify model (if used)

        Raises:
            TrafficCopError: If there's an error with the LLM calls
        """
        # Get advice from Traffic Cop
        advice = await self.route(
            prompt=prompt,
            draft_model_id=draft_model_id,
            verify_model_id=verify_model_id,
            user_id=user_id,
            execution_mode=ExecutionMode.ADVISE,
            customer_api_keys=customer_api_keys,
            metadata=metadata,
        )

        # Extract the necessary information from the advice
        traffic_cop_request_id = advice["traffic_cop_request_id"]
        decision = advice["decision"]
        draft_provider = advice["draft_provider"]
        verify_provider = advice["verify_provider"]

        # Execute the draft model call
        draft_response = await self.execute_llm_call(
            provider=draft_provider["provider"],
            model_id=draft_model_id,
            prompt=prompt,
            api_key=customer_api_keys.get(draft_provider["provider"]) if customer_api_keys else None,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )

        # Determine whether verification is needed based on the advice
        verification_needed = decision == "verification_recommended"

        verify_response = None
        if verification_needed:
            # Execute the verify model call
            verify_response = await self.execute_llm_call(
                provider=verify_provider["provider"],
                model_id=verify_model_id,
                prompt=prompt,
                api_key=customer_api_keys.get(verify_provider["provider"]) if customer_api_keys else None,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )

        # Determine the final response
        final_content = verify_response["content"] if verify_response else draft_response["content"]

        # Report the execution outcome back to Traffic Cop
        await self.report_execution_outcome(
            traffic_cop_request_id=traffic_cop_request_id,
            user_id=user_id or str(uuid4()),
            actual_draft_model_used=draft_model_id,
            draft_token_count=draft_response["tokens_used"],
            draft_latency_ms=draft_response["latency_ms"],
            was_verification_performed=verification_needed,
            final_response=final_content,
            actual_verify_model_used=verify_model_id if verification_needed else None,
            verify_token_count=verify_response["tokens_used"] if verify_response else None,
            verify_latency_ms=verify_response["latency_ms"] if verify_response else None,
            metadata=metadata,
        )

        # Return the final response
        return {
            "content": final_content,
            "verification_used": verification_needed,
            "draft_response": draft_response,
            "verify_response": verify_response,
            "traffic_cop_request_id": traffic_cop_request_id,
        }

    def execute_with_advice_sync(
        self,
        prompt: str,
        draft_model_id: str,
        verify_model_id: str,
        user_id: Optional[str] = None,
        customer_api_keys: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """Synchronous version of execute_with_advice method.

        Args:
            prompt: The prompt to send to the LLM
            draft_model_id: Identifier for the draft model to use
            verify_model_id: Identifier for the verify model to use
            user_id: Unique identifier for the user (default: random UUID)
            customer_api_keys: Optional API keys for the LLM providers
            metadata: Optional metadata to include with the request
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict: The final response including:
                - content: The generated text
                - verification_used: Whether verification was used
                - draft_response: The response from the draft model
                - verify_response: The response from the verify model (if used)

        Raises:
            TrafficCopError: If there's an error with the LLM calls
        """
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # If no event loop is available, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            self.execute_with_advice(
                prompt=prompt,
                draft_model_id=draft_model_id,
                verify_model_id=verify_model_id,
                user_id=user_id,
                customer_api_keys=customer_api_keys,
                metadata=metadata,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
        )

    async def route(
        self,
        prompt: str,
        draft_model_id: str,
        verify_model_id: str,
        user_id: Optional[str] = None,
        execution_mode: Union[ExecutionMode, str] = ExecutionMode.ADVISE,
        customer_api_keys: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """Route a prompt through the Traffic Cop API.

        Args:
            prompt: The prompt to send to the LLM
            draft_model_id: Identifier for the draft model to use
            verify_model_id: Identifier for the verify model to use
            user_id: Unique identifier for the user (default: random UUID)
            execution_mode: Execution mode - 'advise' (client executes LLM calls) or
                           'proxy' (Traffic Cop executes LLM calls). Default: 'advise'
            customer_api_keys: Optional API keys for the LLM providers
            metadata: Optional metadata to include with the request

        Returns:
            Dict: The response from the Traffic Cop API. The structure depends on the execution_mode:
                - For 'advise' mode: Contains decision, suggested models, and traffic_cop_request_id
                - For 'proxy' mode: Contains draft_response, verify_response, final_response, etc.

        Raises:
            ValueError: If required parameters are invalid
            TrafficCopConnectionError: If there's a network error
            TrafficCopAPIError: If the API returns an error response
        """
        # Validate required parameters
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")

        if not draft_model_id or not isinstance(draft_model_id, str):
            raise ValueError("Draft model ID must be a non-empty string")

        if not verify_model_id or not isinstance(verify_model_id, str):
            raise ValueError("Verify model ID must be a non-empty string")

        # Validate optional parameters
        if user_id is not None and (not isinstance(user_id, str) or not user_id):
            raise ValueError("User ID must be a non-empty string if provided")

        if customer_api_keys is not None and not isinstance(customer_api_keys, dict):
            raise ValueError("Customer API keys must be a dictionary if provided")

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary if provided")

        # Generate a user ID if not provided
        if user_id is None:
            user_id = str(uuid4())

        # Validate execution_mode
        if isinstance(execution_mode, str):
            if execution_mode not in [ExecutionMode.ADVISE, ExecutionMode.PROXY]:
                raise ValueError(f"Execution mode must be either 'advise' or 'proxy', got '{execution_mode}'")
            execution_mode_str = execution_mode
        else:
            execution_mode_str = execution_mode.value

        # Prepare the request payload
        payload = {
            "prompt": prompt,
            "user_id": user_id,
            "draft_model_id": draft_model_id,
            "verify_model_id": verify_model_id,
            "execution_mode": execution_mode_str,
        }

        if customer_api_keys:
            payload["customer_api_keys"] = customer_api_keys

        if metadata:
            payload["metadata"] = metadata

        # Make the request
        try:
            async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify_ssl) as client:
                response = await client.post(
                    f"{self.base_url}/route",
                    headers=self.headers,
                    json=payload,
                )

            # Check for API errors
            if response.status_code != 200:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and "detail" in error_data:
                        error_detail = error_data["detail"]
                except Exception:
                    error_detail = response.text

                logger.error(f"API error: {response.status_code} - {error_detail}")
                raise TrafficCopAPIError(response.status_code, error_detail)

            # Parse and return the response
            try:
                return response.json()
            except Exception as e:
                logger.error(f"Error parsing API response: {str(e)}")
                raise TrafficCopError(f"Invalid JSON response from API: {str(e)}")

        except httpx.RequestError as e:
            logger.error(f"Connection error: {str(e)}")
            raise TrafficCopConnectionError(f"Error connecting to Traffic Cop API: {str(e)}")
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {str(e)}")
            raise TrafficCopConnectionError(f"Request to Traffic Cop API timed out: {str(e)}")
        except TrafficCopError:
            # Re-raise Traffic Cop specific errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise TrafficCopError(f"Unexpected error: {str(e)}")

    def route_sync(
        self,
        prompt: str,
        draft_model_id: str,
        verify_model_id: str,
        user_id: Optional[str] = None,
        execution_mode: Union[ExecutionMode, str] = ExecutionMode.ADVISE,
        customer_api_keys: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """Synchronous version of route method.

        Args:
            prompt: The prompt to send to the LLM
            draft_model_id: Identifier for the draft model to use
            verify_model_id: Identifier for the verify model to use
            user_id: Unique identifier for the user (default: random UUID)
            execution_mode: Execution mode - 'advise' (client executes LLM calls) or
                           'proxy' (Traffic Cop executes LLM calls). Default: 'advise'
            customer_api_keys: Optional API keys for the LLM providers
            metadata: Optional metadata to include with the request

        Returns:
            Dict: The response from the Traffic Cop API. The structure depends on the execution_mode:
                - For 'advise' mode: Contains decision, suggested models, and traffic_cop_request_id
                - For 'proxy' mode: Contains draft_response, verify_response, final_response, etc.

        Raises:
            ValueError: If required parameters are invalid
            TrafficCopConnectionError: If there's a network error
            TrafficCopAPIError: If the API returns an error response
        """
        # Validate required parameters
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")

        if not draft_model_id or not isinstance(draft_model_id, str):
            raise ValueError("Draft model ID must be a non-empty string")

        if not verify_model_id or not isinstance(verify_model_id, str):
            raise ValueError("Verify model ID must be a non-empty string")

        # Validate optional parameters
        if user_id is not None and (not isinstance(user_id, str) or not user_id):
            raise ValueError("User ID must be a non-empty string if provided")

        if customer_api_keys is not None and not isinstance(customer_api_keys, dict):
            raise ValueError("Customer API keys must be a dictionary if provided")

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary if provided")

        # Generate a user ID if not provided
        if user_id is None:
            user_id = str(uuid4())

        # Validate execution_mode
        if isinstance(execution_mode, str):
            if execution_mode not in [ExecutionMode.ADVISE, ExecutionMode.PROXY]:
                raise ValueError(f"Execution mode must be either 'advise' or 'proxy', got '{execution_mode}'")
            execution_mode_str = execution_mode
        else:
            execution_mode_str = execution_mode.value

        # Prepare the request payload
        payload = {
            "prompt": prompt,
            "user_id": user_id,
            "draft_model_id": draft_model_id,
            "verify_model_id": verify_model_id,
            "execution_mode": execution_mode_str,
        }

        if customer_api_keys:
            payload["customer_api_keys"] = customer_api_keys

        if metadata:
            payload["metadata"] = metadata

        # Make the request
        try:
            with httpx.Client(timeout=self.timeout, verify=self.verify_ssl) as client:
                response = client.post(
                    f"{self.base_url}/route",
                    headers=self.headers,
                    json=payload,
                )

            # Check for API errors
            if response.status_code != 200:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and "detail" in error_data:
                        error_detail = error_data["detail"]
                except Exception:
                    error_detail = response.text

                logger.error(f"API error: {response.status_code} - {error_detail}")
                raise TrafficCopAPIError(response.status_code, error_detail)

            # Parse and return the response
            try:
                return response.json()
            except Exception as e:
                logger.error(f"Error parsing API response: {str(e)}")
                raise TrafficCopError(f"Invalid JSON response from API: {str(e)}")

        except httpx.RequestError as e:
            logger.error(f"Connection error: {str(e)}")
            raise TrafficCopConnectionError(f"Error connecting to Traffic Cop API: {str(e)}")
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {str(e)}")
            raise TrafficCopConnectionError(f"Request to Traffic Cop API timed out: {str(e)}")
        except TrafficCopError:
            # Re-raise Traffic Cop specific errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise TrafficCopError(f"Unexpected error: {str(e)}")

    async def report_execution_outcome(
        self,
        traffic_cop_request_id: str,
        user_id: str,
        actual_draft_model_used: str,
        draft_token_count: int,
        draft_latency_ms: int,
        was_verification_performed: bool,
        final_response: str,
        actual_verify_model_used: Optional[str] = None,
        verify_token_count: Optional[int] = None,
        verify_latency_ms: Optional[int] = None,
        quality_feedback: Optional[float] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """Report the outcome of a client-side execution in advise mode.

        This method should be called after executing LLM calls client-side based on
        advice received from the Traffic Cop API in 'advise' mode.

        Args:
            traffic_cop_request_id: The traffic_cop_request_id from the original advise response
            user_id: Unique identifier for the user (should match the original request)
            actual_draft_model_used: The draft model that was actually used
            draft_token_count: Number of tokens used by the draft model
            draft_latency_ms: Latency of the draft model response in ms
            was_verification_performed: Whether verification was performed
            final_response: The final response content returned to the end user
            actual_verify_model_used: The verify model that was actually used (if verification was performed)
            verify_token_count: Number of tokens used by the verify model (if verification was performed)
            verify_latency_ms: Latency of the verify model response in ms (if verification was performed)
            quality_feedback: Optional quality feedback score (0-1) provided by the client
            metadata: Optional metadata to include with the request

        Returns:
            Dict: The response from the Traffic Cop API

        Raises:
            ValueError: If required parameters are invalid
            TrafficCopConnectionError: If there's a network error
            TrafficCopAPIError: If the API returns an error response
        """
        # Validate required parameters
        if not traffic_cop_request_id or not isinstance(traffic_cop_request_id, str):
            raise ValueError("Traffic Cop request ID must be a non-empty string")

        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")

        if not actual_draft_model_used or not isinstance(actual_draft_model_used, str):
            raise ValueError("Actual draft model used must be a non-empty string")

        if not isinstance(draft_token_count, int) or draft_token_count <= 0:
            raise ValueError("Draft token count must be a positive integer")

        if not isinstance(draft_latency_ms, int) or draft_latency_ms <= 0:
            raise ValueError("Draft latency must be a positive integer")

        if not isinstance(was_verification_performed, bool):
            raise ValueError("Was verification performed must be a boolean")

        if not final_response or not isinstance(final_response, str):
            raise ValueError("Final response must be a non-empty string")

        # Validate conditional parameters
        if was_verification_performed:
            if not actual_verify_model_used or not isinstance(actual_verify_model_used, str):
                raise ValueError("Actual verify model used must be a non-empty string when verification was performed")

            if not isinstance(verify_token_count, int) or verify_token_count <= 0:
                raise ValueError("Verify token count must be a positive integer when verification was performed")

            if not isinstance(verify_latency_ms, int) or verify_latency_ms <= 0:
                raise ValueError("Verify latency must be a positive integer when verification was performed")

        # Validate optional parameters
        if quality_feedback is not None and (not isinstance(quality_feedback, float) or quality_feedback < 0 or quality_feedback > 1):
            raise ValueError("Quality feedback must be a float between 0 and 1 if provided")

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary if provided")

        # Create a hash of the final response for privacy/security
        final_outcome_hash = hashlib.sha256(final_response.encode("utf-8")).hexdigest()

        # Prepare the request payload
        payload = {
            "traffic_cop_request_id": traffic_cop_request_id,
            "user_id": user_id,
            "actual_draft_model_used": actual_draft_model_used,
            "draft_token_count": draft_token_count,
            "draft_latency_ms": draft_latency_ms,
            "was_verification_performed": was_verification_performed,
            "final_outcome_hash": final_outcome_hash,
        }

        if was_verification_performed:
            payload["actual_verify_model_used"] = actual_verify_model_used
            payload["verify_token_count"] = verify_token_count
            payload["verify_latency_ms"] = verify_latency_ms

        if quality_feedback is not None:
            payload["quality_feedback"] = quality_feedback

        if metadata:
            payload["metadata"] = metadata

        # Make the request
        try:
            async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify_ssl) as client:
                response = await client.post(
                    f"{self.base_url}/report_execution_outcome",
                    headers=self.headers,
                    json=payload,
                )

            # Check for API errors
            if response.status_code != 200:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and "detail" in error_data:
                        error_detail = error_data["detail"]
                except Exception:
                    error_detail = response.text

                logger.error(f"API error: {response.status_code} - {error_detail}")
                raise TrafficCopAPIError(response.status_code, error_detail)

            # Parse and return the response
            try:
                return response.json()
            except Exception as e:
                logger.error(f"Error parsing API response: {str(e)}")
                raise TrafficCopError(f"Invalid JSON response from API: {str(e)}")

        except httpx.RequestError as e:
            logger.error(f"Connection error: {str(e)}")
            raise TrafficCopConnectionError(f"Error connecting to Traffic Cop API: {str(e)}")
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {str(e)}")
            raise TrafficCopConnectionError(f"Request to Traffic Cop API timed out: {str(e)}")
        except TrafficCopError:
            # Re-raise Traffic Cop specific errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise TrafficCopError(f"Unexpected error: {str(e)}")

    def report_execution_outcome_sync(
        self,
        traffic_cop_request_id: str,
        user_id: str,
        actual_draft_model_used: str,
        draft_token_count: int,
        draft_latency_ms: int,
        was_verification_performed: bool,
        final_response: str,
        actual_verify_model_used: Optional[str] = None,
        verify_token_count: Optional[int] = None,
        verify_latency_ms: Optional[int] = None,
        quality_feedback: Optional[float] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """Synchronous version of report_execution_outcome method.

        This method should be called after executing LLM calls client-side based on
        advice received from the Traffic Cop API in 'advise' mode.

        Args:
            traffic_cop_request_id: The traffic_cop_request_id from the original advise response
            user_id: Unique identifier for the user (should match the original request)
            actual_draft_model_used: The draft model that was actually used
            draft_token_count: Number of tokens used by the draft model
            draft_latency_ms: Latency of the draft model response in ms
            was_verification_performed: Whether verification was performed
            final_response: The final response content returned to the end user
            actual_verify_model_used: The verify model that was actually used (if verification was performed)
            verify_token_count: Number of tokens used by the verify model (if verification was performed)
            verify_latency_ms: Latency of the verify model response in ms (if verification was performed)
            quality_feedback: Optional quality feedback score (0-1) provided by the client
            metadata: Optional metadata to include with the request

        Returns:
            Dict: The response from the Traffic Cop API

        Raises:
            ValueError: If required parameters are invalid
            TrafficCopConnectionError: If there's a network error
            TrafficCopAPIError: If the API returns an error response
        """
        # Validate required parameters
        if not traffic_cop_request_id or not isinstance(traffic_cop_request_id, str):
            raise ValueError("Traffic Cop request ID must be a non-empty string")

        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")

        if not actual_draft_model_used or not isinstance(actual_draft_model_used, str):
            raise ValueError("Actual draft model used must be a non-empty string")

        if not isinstance(draft_token_count, int) or draft_token_count <= 0:
            raise ValueError("Draft token count must be a positive integer")

        if not isinstance(draft_latency_ms, int) or draft_latency_ms <= 0:
            raise ValueError("Draft latency must be a positive integer")

        if not isinstance(was_verification_performed, bool):
            raise ValueError("Was verification performed must be a boolean")

        if not final_response or not isinstance(final_response, str):
            raise ValueError("Final response must be a non-empty string")

        # Validate conditional parameters
        if was_verification_performed:
            if not actual_verify_model_used or not isinstance(actual_verify_model_used, str):
                raise ValueError("Actual verify model used must be a non-empty string when verification was performed")

            if not isinstance(verify_token_count, int) or verify_token_count <= 0:
                raise ValueError("Verify token count must be a positive integer when verification was performed")

            if not isinstance(verify_latency_ms, int) or verify_latency_ms <= 0:
                raise ValueError("Verify latency must be a positive integer when verification was performed")

        # Validate optional parameters
        if quality_feedback is not None and (not isinstance(quality_feedback, float) or quality_feedback < 0 or quality_feedback > 1):
            raise ValueError("Quality feedback must be a float between 0 and 1 if provided")

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary if provided")

        # Create a hash of the final response for privacy/security
        final_outcome_hash = hashlib.sha256(final_response.encode("utf-8")).hexdigest()

        # Prepare the request payload
        payload = {
            "traffic_cop_request_id": traffic_cop_request_id,
            "user_id": user_id,
            "actual_draft_model_used": actual_draft_model_used,
            "draft_token_count": draft_token_count,
            "draft_latency_ms": draft_latency_ms,
            "was_verification_performed": was_verification_performed,
            "final_outcome_hash": final_outcome_hash,
        }

        if was_verification_performed:
            payload["actual_verify_model_used"] = actual_verify_model_used
            payload["verify_token_count"] = verify_token_count
            payload["verify_latency_ms"] = verify_latency_ms

        if quality_feedback is not None:
            payload["quality_feedback"] = quality_feedback

        if metadata:
            payload["metadata"] = metadata

        # Make the request
        try:
            with httpx.Client(timeout=self.timeout, verify=self.verify_ssl) as client:
                response = client.post(
                    f"{self.base_url}/report_execution_outcome",
                    headers=self.headers,
                    json=payload,
                )

            # Check for API errors
            if response.status_code != 200:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and "detail" in error_data:
                        error_detail = error_data["detail"]
                except Exception:
                    error_detail = response.text

                logger.error(f"API error: {response.status_code} - {error_detail}")
                raise TrafficCopAPIError(response.status_code, error_detail)

            # Parse and return the response
            try:
                return response.json()
            except Exception as e:
                logger.error(f"Error parsing API response: {str(e)}")
                raise TrafficCopError(f"Invalid JSON response from API: {str(e)}")

        except httpx.RequestError as e:
            logger.error(f"Connection error: {str(e)}")
            raise TrafficCopConnectionError(f"Error connecting to Traffic Cop API: {str(e)}")
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {str(e)}")
            raise TrafficCopConnectionError(f"Request to Traffic Cop API timed out: {str(e)}")
        except TrafficCopError:
            # Re-raise Traffic Cop specific errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise TrafficCopError(f"Unexpected error: {str(e)}")