import pytest

from liquid_earth_sdk.modules.rest_client.rest_interface import get_dev_tokens, generate_dev_token, revoke_dev_token
import dotenv
import os
import requests

dotenv.load_dotenv()

ONLY_EXPLICIT = True


def test_token():
    # Login
    endpoint = os.getenv("LOGIN_URL")
    subscription_key = os.getenv("LOGIN_SUBSCRIPTION_KEY")
    headers = {
            "Content-Type"             : "application/x-www-form-urlencoded",
            "X-App-Version"            : "1.0.8.1",
            "Ocp-Apim-Subscription-Key": subscription_key
    }

    import time

    # Build payload with proper URL encoding
    payload = os.getenv("LOGIN_PAYLOAD")

    response = requests.post(endpoint, headers=headers, data=payload)
    result = response.json()

    # Add login token to the environment
    login_token = "Bearer " + result["access_token"]
    # user_id = os.getenv("TEST_USER_ID")
    user_id = None

    # Get dev tokens and assert there are no valid tokens
    initial_tokens = get_dev_tokens(login_token=login_token)
    initial_token_count = len(initial_tokens)

    # Generate a new dev token and assert it is valid
    token_name = f"test_token_{int(time.time())}"
    new_token = generate_dev_token(
        token_name=token_name,
        login_token=login_token
    )
    assert new_token is not None
    assert "Key" in new_token
    token_key = new_token["Key"]

    # Verify token was created
    tokens_after_creation = get_dev_tokens(login_token=login_token)
    assert len(tokens_after_creation) == initial_token_count + 1

    # Find our newly created token
    created_token = None
    for token in tokens_after_creation:
        if token.get("Key") == token_key:
            created_token = token
            break

    assert created_token is not None
    assert created_token.get("IsRevoked") is False

    # Revoke the dev token and assert it is no longer valid
    revoke_result = revoke_dev_token(
        token_id=token_key,
        login_token=login_token
    )
    assert revoke_result is not None

    # Verify token was revoked
    tokens_after_revocation = get_dev_tokens(login_token=login_token)

    # Check if the token is marked as revoked
    for token in tokens_after_revocation:
        if token.get("Key") == token_key:
            assert token.get("IsRevoked") is True, "Token should be revoked"


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_login_with_credentials():
    endpoint = os.getenv("LOGIN_URL")
    subscription_key = os.getenv("LOGIN_SUBSCRIPTION_KEY")  # Add this line
    headers = {
            "Content-Type"             : "application/x-www-form-urlencoded",
            "X-App-Version"            : "1.0.8.1",
            "Ocp-Apim-Subscription-Key": subscription_key  # Add this line
    }

    payload = os.getenv("LOGIN_PAYLOAD")

    response = requests.post(endpoint, headers=headers, data=payload)
    result = response.json()
    print(result)


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_get_user_dev_tokens():
    val = get_dev_tokens(
        login_token="Bearer " + os.getenv("TEST_LOGIN_TOKEN")
    )
    print(val)


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_generate_dev_token():
    val = generate_dev_token(
        token_name="test_token",
        login_token="Bearer " + os.getenv("TEST_LOGIN_TOKEN")
    )
    print(val)


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_revoke_dev_token():
    val = revoke_dev_token(
        token_id="le-8b4c9d33528a4e7492583871f6545ea4IAmNqhThFXeIKMQTzummp0Zdyhejwnqh1iSteK1A55I",
        login_token="unused_in_local_dev"
    )
    print(val)
