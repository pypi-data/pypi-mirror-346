"""Tests for the advise mode in the Traffic Cop client."""

import unittest
from unittest import mock
import httpx
import pytest
from uuid import uuid4

from traffic_cop_client import (
    TrafficCopClient,
    ExecutionMode,
    TrafficCopError,
    TrafficCopConnectionError,
    TrafficCopAPIError,
)


class TestAdviseMode(unittest.TestCase):
    """Test cases for the advise mode."""

    def setUp(self):
        """Set up the test client."""
        self.client = TrafficCopClient(api_key="test-api-key")
        self.prompt = "What is the capital of France?"
        self.draft_model_id = "gpt-3.5-turbo"
        self.verify_model_id = "gpt-4"
        self.user_id = "test-user-id"
        self.traffic_cop_request_id = str(uuid4())

    def test_route_sync_advise_mode(self):
        """Test route_sync with advise mode."""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "request_id": str(uuid4()),
            "execution_mode": ExecutionMode.ADVISE,
            "traffic_cop_request_id": self.traffic_cop_request_id,
            "decision": "verification_recommended",
            "suggested_draft_model_id": self.draft_model_id,
            "suggested_verify_model_id": self.verify_model_id,
            "threshold_used": 0.7,
            "draft_provider": {
                "provider": "openai",
                "api_endpoint": "https://api.openai.com/v1/chat/completions",
                "model_type": "chat",
            },
            "verify_provider": {
                "provider": "openai",
                "api_endpoint": "https://api.openai.com/v1/chat/completions",
                "model_type": "chat",
            },
            "decision_reason": "Test reason",
        }

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            response = self.client.route_sync(
                prompt=self.prompt,
                draft_model_id=self.draft_model_id,
                verify_model_id=self.verify_model_id,
                user_id=self.user_id,
                execution_mode=ExecutionMode.ADVISE,
            )

        self.assertEqual(response["execution_mode"], ExecutionMode.ADVISE)
        self.assertEqual(response["decision"], "verification_recommended")
        self.assertEqual(response["suggested_draft_model_id"], self.draft_model_id)
        self.assertEqual(response["suggested_verify_model_id"], self.verify_model_id)
        self.assertEqual(response["threshold_used"], 0.7)
        self.assertEqual(response["draft_provider"]["provider"], "openai")
        self.assertEqual(response["verify_provider"]["provider"], "openai")
        self.assertEqual(response["decision_reason"], "Test reason")

    def test_route_sync_advise_mode_draft_sufficient(self):
        """Test route_sync with advise mode and draft_sufficient decision."""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "request_id": str(uuid4()),
            "execution_mode": ExecutionMode.ADVISE,
            "traffic_cop_request_id": self.traffic_cop_request_id,
            "decision": "draft_sufficient",
            "suggested_draft_model_id": self.draft_model_id,
            "suggested_verify_model_id": self.verify_model_id,
            "threshold_used": 0.7,
            "draft_provider": {
                "provider": "openai",
                "api_endpoint": "https://api.openai.com/v1/chat/completions",
                "model_type": "chat",
            },
            "verify_provider": {
                "provider": "openai",
                "api_endpoint": "https://api.openai.com/v1/chat/completions",
                "model_type": "chat",
            },
            "decision_reason": "Test reason",
        }

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            response = self.client.route_sync(
                prompt=self.prompt,
                draft_model_id=self.draft_model_id,
                verify_model_id=self.verify_model_id,
                user_id=self.user_id,
                execution_mode=ExecutionMode.ADVISE,
            )

        self.assertEqual(response["execution_mode"], ExecutionMode.ADVISE)
        self.assertEqual(response["decision"], "draft_sufficient")
        self.assertEqual(response["suggested_draft_model_id"], self.draft_model_id)
        self.assertEqual(response["suggested_verify_model_id"], self.verify_model_id)
        self.assertEqual(response["threshold_used"], 0.7)
        self.assertEqual(response["draft_provider"]["provider"], "openai")
        self.assertEqual(response["verify_provider"]["provider"], "openai")
        self.assertEqual(response["decision_reason"], "Test reason")

    def test_default_execution_mode(self):
        """Test that the default execution mode is ADVISE."""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "request_id": str(uuid4()),
            "execution_mode": ExecutionMode.ADVISE,
            "traffic_cop_request_id": self.traffic_cop_request_id,
            "decision": "verification_recommended",
            "suggested_draft_model_id": self.draft_model_id,
            "suggested_verify_model_id": self.verify_model_id,
            "threshold_used": 0.7,
            "draft_provider": {
                "provider": "openai",
                "api_endpoint": "https://api.openai.com/v1/chat/completions",
                "model_type": "chat",
            },
            "verify_provider": {
                "provider": "openai",
                "api_endpoint": "https://api.openai.com/v1/chat/completions",
                "model_type": "chat",
            },
            "decision_reason": "Test reason",
        }

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            # Don't specify execution_mode, should default to ADVISE
            response = self.client.route_sync(
                prompt=self.prompt,
                draft_model_id=self.draft_model_id,
                verify_model_id=self.verify_model_id,
                user_id=self.user_id,
            )

        self.assertEqual(response["execution_mode"], ExecutionMode.ADVISE)


@pytest.mark.asyncio
async def test_route_async_advise_mode():
    """Test the async route method with advise mode."""
    client = TrafficCopClient(api_key="test-api-key")
    prompt = "What is the capital of France?"
    draft_model_id = "gpt-3.5-turbo"
    verify_model_id = "gpt-4"
    user_id = "test-user-id"
    traffic_cop_request_id = str(uuid4())

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "request_id": str(uuid4()),
        "execution_mode": ExecutionMode.ADVISE,
        "traffic_cop_request_id": traffic_cop_request_id,
        "decision": "verification_recommended",
        "suggested_draft_model_id": draft_model_id,
        "suggested_verify_model_id": verify_model_id,
        "threshold_used": 0.7,
        "draft_provider": {
            "provider": "openai",
            "api_endpoint": "https://api.openai.com/v1/chat/completions",
            "model_type": "chat",
        },
        "verify_provider": {
            "provider": "openai",
            "api_endpoint": "https://api.openai.com/v1/chat/completions",
            "model_type": "chat",
        },
        "decision_reason": "Test reason",
    }

    with mock.patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        response = await client.route(
            prompt=prompt,
            draft_model_id=draft_model_id,
            verify_model_id=verify_model_id,
            user_id=user_id,
            execution_mode=ExecutionMode.ADVISE,
        )

    assert response["execution_mode"] == ExecutionMode.ADVISE
    assert response["decision"] == "verification_recommended"
    assert response["suggested_draft_model_id"] == draft_model_id
    assert response["suggested_verify_model_id"] == verify_model_id
    assert response["threshold_used"] == 0.7
    assert response["draft_provider"]["provider"] == "openai"
    assert response["verify_provider"]["provider"] == "openai"
    assert response["decision_reason"] == "Test reason"
