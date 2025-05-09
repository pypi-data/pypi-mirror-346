"""Tests for the TrafficCopClient class."""

import json
import unittest
from unittest import mock
from uuid import UUID

import httpx
import pytest

from traffic_cop_client import (
    TrafficCopClient,
    TrafficCopError,
    TrafficCopConnectionError,
    TrafficCopAPIError,
)


class TestTrafficCopClient(unittest.TestCase):
    """Test cases for the TrafficCopClient class."""

    def test_init_with_valid_params(self):
        """Test initialization with valid parameters."""
        client = TrafficCopClient(
            api_key="test-api-key",
            base_url="https://example.com",
            timeout=30,
        )
        self.assertEqual(client.api_key, "test-api-key")
        self.assertEqual(client.base_url, "https://example.com")
        self.assertEqual(client.timeout, 30)
        self.assertEqual(
            client.headers,
            {
                "Authorization": "Bearer test-api-key",
                "Content-Type": "application/json",
            },
        )

    def test_init_with_trailing_slash_in_base_url(self):
        """Test initialization with trailing slash in base_url."""
        client = TrafficCopClient(
            api_key="test-api-key",
            base_url="https://example.com/",
        )
        self.assertEqual(client.base_url, "https://example.com")

    def test_init_with_invalid_api_key(self):
        """Test initialization with invalid API key."""
        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key="")
        self.assertEqual(str(cm.exception), "API key must be a non-empty string")

        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key=None)
        self.assertEqual(str(cm.exception), "API key must be a non-empty string")

        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key=123)
        self.assertEqual(str(cm.exception), "API key must be a non-empty string")

    def test_init_with_invalid_base_url(self):
        """Test initialization with invalid base URL."""
        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key="test-api-key", base_url="")
        self.assertEqual(str(cm.exception), "Base URL must be a non-empty string")

        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key="test-api-key", base_url=None)
        self.assertEqual(str(cm.exception), "Base URL must be a non-empty string")

        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key="test-api-key", base_url=123)
        self.assertEqual(str(cm.exception), "Base URL must be a non-empty string")

    def test_init_with_invalid_timeout(self):
        """Test initialization with invalid timeout."""
        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key="test-api-key", timeout=0)
        self.assertEqual(str(cm.exception), "Timeout must be a positive integer")

        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key="test-api-key", timeout=-1)
        self.assertEqual(str(cm.exception), "Timeout must be a positive integer")

        with self.assertRaises(ValueError) as cm:
            TrafficCopClient(api_key="test-api-key", timeout="60")
        self.assertEqual(str(cm.exception), "Timeout must be a positive integer")


class TestRouteSync(unittest.TestCase):
    """Test cases for the route_sync method."""

    def setUp(self):
        """Set up the test client."""
        self.client = TrafficCopClient(api_key="test-api-key")

    def test_route_sync_with_valid_params(self):
        """Test route_sync with valid parameters."""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "request_id": "123e4567-e89b-12d3-a456-426614174000",
            "draft_response": {
                "content": "Paris is the capital of France.",
                "model_id": "gpt-3.5-turbo",
                "tokens_used": 15,
                "latency_ms": 250,
                "confidence": 0.92,
                "metadata": {"provider": "openai"},
            },
            "verify_response": None,
            "final_response": "Paris is the capital of France.",
            "verification_used": False,
            "estimated_cost_saved": 0.000123,
            "threshold_used": 0.7,
        }

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            response = self.client.route_sync(
                prompt="What is the capital of France?",
                draft_model_id="gpt-3.5-turbo",
                verify_model_id="gpt-4",
            )

        self.assertEqual(response["final_response"], "Paris is the capital of France.")
        self.assertEqual(response["verification_used"], False)
        self.assertEqual(response["estimated_cost_saved"], 0.000123)

    def test_route_sync_with_invalid_prompt(self):
        """Test route_sync with invalid prompt."""
        with self.assertRaises(ValueError) as cm:
            self.client.route_sync(
                prompt="",
                draft_model_id="gpt-3.5-turbo",
                verify_model_id="gpt-4",
            )
        self.assertEqual(str(cm.exception), "Prompt must be a non-empty string")

        with self.assertRaises(ValueError) as cm:
            self.client.route_sync(
                prompt=None,
                draft_model_id="gpt-3.5-turbo",
                verify_model_id="gpt-4",
            )
        self.assertEqual(str(cm.exception), "Prompt must be a non-empty string")

        with self.assertRaises(ValueError) as cm:
            self.client.route_sync(
                prompt=123,
                draft_model_id="gpt-3.5-turbo",
                verify_model_id="gpt-4",
            )
        self.assertEqual(str(cm.exception), "Prompt must be a non-empty string")

    def test_route_sync_with_api_error(self):
        """Test route_sync with API error."""
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Invalid request"}
        mock_response.text = '{"detail": "Invalid request"}'

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            with self.assertRaises(TrafficCopAPIError) as cm:
                self.client.route_sync(
                    prompt="What is the capital of France?",
                    draft_model_id="gpt-3.5-turbo",
                    verify_model_id="gpt-4",
                )

        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(cm.exception.detail, "Invalid request")

    def test_route_sync_with_connection_error(self):
        """Test route_sync with connection error."""
        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = httpx.RequestError("Connection error")
            with self.assertRaises(TrafficCopConnectionError) as cm:
                self.client.route_sync(
                    prompt="What is the capital of France?",
                    draft_model_id="gpt-3.5-turbo",
                    verify_model_id="gpt-4",
                )

        self.assertIn("Connection error", str(cm.exception))

    def test_route_sync_with_timeout_error(self):
        """Test route_sync with timeout error."""
        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = httpx.TimeoutException("Timeout")
            with self.assertRaises(TrafficCopConnectionError) as cm:
                self.client.route_sync(
                    prompt="What is the capital of France?",
                    draft_model_id="gpt-3.5-turbo",
                    verify_model_id="gpt-4",
                )

        self.assertIn("Timeout", str(cm.exception))


@pytest.mark.asyncio
async def test_route_async():
    """Test the async route method."""
    client = TrafficCopClient(api_key="test-api-key")

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "request_id": "123e4567-e89b-12d3-a456-426614174000",
        "draft_response": {
            "content": "Paris is the capital of France.",
            "model_id": "gpt-3.5-turbo",
            "tokens_used": 15,
            "latency_ms": 250,
            "confidence": 0.92,
            "metadata": {"provider": "openai"},
        },
        "verify_response": None,
        "final_response": "Paris is the capital of France.",
        "verification_used": False,
        "estimated_cost_saved": 0.000123,
        "threshold_used": 0.7,
    }

    with mock.patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        response = await client.route(
            prompt="What is the capital of France?",
            draft_model_id="gpt-3.5-turbo",
            verify_model_id="gpt-4",
        )

    assert response["final_response"] == "Paris is the capital of France."
    assert response["verification_used"] is False
    assert response["estimated_cost_saved"] == 0.000123
