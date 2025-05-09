"""Tests for the report_execution_outcome method."""

import unittest
from unittest import mock
import httpx
import pytest

from traffic_cop_client import (
    TrafficCopClient,
    TrafficCopError,
    TrafficCopConnectionError,
    TrafficCopAPIError,
)


class TestReportExecutionOutcomeSync(unittest.TestCase):
    """Test cases for the report_execution_outcome_sync method."""

    def setUp(self):
        """Set up the test client."""
        self.client = TrafficCopClient(api_key="test-api-key")
        self.valid_params = {
            "traffic_cop_request_id": "test-traffic-cop-request-id",
            "user_id": "test-user-id",
            "actual_draft_model_used": "gpt-3.5-turbo",
            "draft_token_count": 100,
            "draft_latency_ms": 250,
            "was_verification_performed": False,
            "final_response": "Paris is the capital of France.",
        }
        self.valid_params_with_verification = {
            "traffic_cop_request_id": "test-traffic-cop-request-id",
            "user_id": "test-user-id",
            "actual_draft_model_used": "gpt-3.5-turbo",
            "draft_token_count": 100,
            "draft_latency_ms": 250,
            "was_verification_performed": True,
            "final_response": "Paris is the capital of France.",
            "actual_verify_model_used": "gpt-4",
            "verify_token_count": 150,
            "verify_latency_ms": 500,
        }

    def test_report_execution_outcome_sync_with_valid_params(self):
        """Test report_execution_outcome_sync with valid parameters."""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "traffic_cop_request_id": "test-traffic-cop-request-id",
            "message": "Execution outcome successfully reported",
        }

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            response = self.client.report_execution_outcome_sync(**self.valid_params)

        self.assertEqual(response["success"], True)
        self.assertEqual(response["traffic_cop_request_id"], "test-traffic-cop-request-id")
        self.assertEqual(response["message"], "Execution outcome successfully reported")

    def test_report_execution_outcome_sync_with_verification(self):
        """Test report_execution_outcome_sync with verification performed."""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "traffic_cop_request_id": "test-traffic-cop-request-id",
            "message": "Execution outcome successfully reported",
        }

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            response = self.client.report_execution_outcome_sync(**self.valid_params_with_verification)

        self.assertEqual(response["success"], True)
        self.assertEqual(response["traffic_cop_request_id"], "test-traffic-cop-request-id")
        self.assertEqual(response["message"], "Execution outcome successfully reported")

    def test_report_execution_outcome_sync_with_optional_params(self):
        """Test report_execution_outcome_sync with optional parameters."""
        params = self.valid_params.copy()
        params.update({
            "quality_feedback": 0.95,
            "metadata": {"source": "test", "session_id": "test-session"},
        })

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "traffic_cop_request_id": "test-traffic-cop-request-id",
            "message": "Execution outcome successfully reported",
        }

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            response = self.client.report_execution_outcome_sync(**params)

        self.assertEqual(response["success"], True)
        self.assertEqual(response["traffic_cop_request_id"], "test-traffic-cop-request-id")
        self.assertEqual(response["message"], "Execution outcome successfully reported")

    def test_report_execution_outcome_sync_with_api_error(self):
        """Test report_execution_outcome_sync with API error."""
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Invalid request"}
        mock_response.text = '{"detail": "Invalid request"}'

        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_response
            with self.assertRaises(TrafficCopAPIError) as cm:
                self.client.report_execution_outcome_sync(**self.valid_params)

        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(cm.exception.detail, "Invalid request")

    def test_report_execution_outcome_sync_with_connection_error(self):
        """Test report_execution_outcome_sync with connection error."""
        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = httpx.RequestError("Connection error")
            with self.assertRaises(TrafficCopConnectionError) as cm:
                self.client.report_execution_outcome_sync(**self.valid_params)

        self.assertIn("Connection error", str(cm.exception))

    def test_report_execution_outcome_sync_with_timeout_error(self):
        """Test report_execution_outcome_sync with timeout error."""
        with mock.patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = httpx.TimeoutException("Timeout")
            with self.assertRaises(TrafficCopConnectionError) as cm:
                self.client.report_execution_outcome_sync(**self.valid_params)

        self.assertIn("Timeout", str(cm.exception))


@pytest.mark.asyncio
async def test_report_execution_outcome_async():
    """Test the async report_execution_outcome method."""
    client = TrafficCopClient(api_key="test-api-key")
    valid_params = {
        "traffic_cop_request_id": "test-traffic-cop-request-id",
        "user_id": "test-user-id",
        "actual_draft_model_used": "gpt-3.5-turbo",
        "draft_token_count": 100,
        "draft_latency_ms": 250,
        "was_verification_performed": False,
        "final_response": "Paris is the capital of France.",
    }

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "traffic_cop_request_id": "test-traffic-cop-request-id",
        "message": "Execution outcome successfully reported",
    }

    with mock.patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        response = await client.report_execution_outcome(**valid_params)

    assert response["success"] is True
    assert response["traffic_cop_request_id"] == "test-traffic-cop-request-id"
    assert response["message"] == "Execution outcome successfully reported"
