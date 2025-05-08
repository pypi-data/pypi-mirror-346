import os
import pytest
import json
from src.api_clients import call_openai_api, call_google_api, call_anthropic_api

# Test constants
# System prompt designed to elicit a specific, simple JSON response.
TEST_SYSTEM_PROMPT = (
    "You are a test assistant. "
    "Your sole task is to output the following JSON object and nothing else: "
    '{"connectivity_test": "success"}'
)
TEST_USER_PROMPT = "Please provide the JSON output as instructed."
TEST_TEMPERATURE = 0.1  # Low temperature for deterministic-like responses
EXPECTED_JSON_SUCCESS = {"connectivity_test": "success"}

# Model names for testing - choose cost-effective and commonly available models
OPENAI_TEST_MODEL = "gpt-3.5-turbo"
GOOGLE_TEST_MODEL = "gemini-1.5-pro"  # Updated to use officially supported model
ANTHROPIC_TEST_MODEL = "claude-3-haiku-20240307"

# --- OpenAI Tests ---
def test_openai_api_connectivity():
    """Tests basic connectivity and JSON response from the OpenAI API.
    Assumes OPENAI_API_KEY environment variable is set."""
    response_str = call_openai_api(
        OPENAI_TEST_MODEL,
        TEST_SYSTEM_PROMPT,
        TEST_USER_PROMPT,
        TEST_TEMPERATURE
    )

    assert response_str is not None, "OpenAI API returned None, indicating an error during the call."
    try:
        response_json = json.loads(response_str)
    except json.JSONDecodeError:
        pytest.fail(f"OpenAI API response was not valid JSON. Response: {response_str}")

    assert response_json == EXPECTED_JSON_SUCCESS, \
        f"OpenAI API response JSON did not match expected. Got: {response_json}, Expected: {EXPECTED_JSON_SUCCESS}"

# --- Google Tests ---
def test_google_api_connectivity():
    """Tests basic connectivity and JSON response from the Google Gemini API.
    Assumes GOOGLE_API_KEY environment variable is set."""
    response_str = call_google_api(
        GOOGLE_TEST_MODEL,
        TEST_SYSTEM_PROMPT,
        TEST_USER_PROMPT,
        TEST_TEMPERATURE
    )

    assert response_str is not None, "Google API call returned None (unexpected for this function)."
    try:
        response_json = json.loads(response_str)
    except json.JSONDecodeError:
        pytest.fail(f"Google API response was not valid JSON. Response: {response_str}")

    # The call_google_api function returns a JSON with an "error" key on failure.
    if "error" in response_json:
        pytest.fail(f"Google API call resulted in an error: {response_json['error']}")

    assert response_json == EXPECTED_JSON_SUCCESS, \
        f"Google API response JSON did not match expected. Got: {response_json}, Expected: {EXPECTED_JSON_SUCCESS}"

# --- Anthropic Tests ---
def test_anthropic_api_connectivity():
    """Tests basic connectivity and JSON response from the Anthropic API.
    Assumes ANTHROPIC_API_KEY environment variable is set."""
    response_str = call_anthropic_api(
        ANTHROPIC_TEST_MODEL,
        TEST_SYSTEM_PROMPT,
        TEST_USER_PROMPT,
        TEST_TEMPERATURE
    )

    assert response_str is not None, "Anthropic API call returned None (unexpected for this function)."
    try:
        response_json = json.loads(response_str)
    except json.JSONDecodeError:
        pytest.fail(f"Anthropic API response was not valid JSON. Response: {response_str}")

    # The call_anthropic_api function returns a JSON with an "error" key on failure.
    if "error" in response_json:
        pytest.fail(f"Anthropic API call resulted in an error: {response_json['error']}")

    assert response_json == EXPECTED_JSON_SUCCESS, \
        f"Anthropic API response JSON did not match expected. Got: {response_json}, Expected: {EXPECTED_JSON_SUCCESS}" 