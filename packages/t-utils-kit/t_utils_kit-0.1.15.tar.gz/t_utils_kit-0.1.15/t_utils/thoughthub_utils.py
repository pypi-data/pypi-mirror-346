"""This module contains utility functions for the ThoughtHub project."""

from dataclasses import dataclass
from enum import Enum
import requests
import time
from pathlib import Path
import os

# Global variables to store token and timestamp
_cached_token = None
_token_timestamp = None


def get_stytch_token(client_id: str, client_secret: str, project_id: str) -> str:
    """Get a Stytch access token for the ThoughtHub project.

    Args:
        client_id (str): The Stytch client ID.
        client_secret (str): The Stytch client secret.
        project_id (str): The Stytch project ID.

    Returns:
        str: The Stytch access token.
    """
    global _cached_token, _token_timestamp

    # Check if token exists and is valid (less than 30 minutes old)
    current_time = time.time()
    if _cached_token and _token_timestamp and (current_time - _token_timestamp < 1800):
        print("Using cached token...")
        return _cached_token

    print("No valid token in memory, requesting new token...")

    # Validate required environment variables
    missing_vars = []
    if not client_id:
        missing_vars.append("STYTCH_CLIENT_ID")
    if not client_secret:
        missing_vars.append("STYTCH_CLIENT_SECRET")
    if not project_id:
        missing_vars.append("STYTCH_PROJECT_ID")

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # API endpoint
    url = f"https://api.stytch.com/v1/public/{project_id}/oauth2/token"

    # Request headers
    headers = {"Content-Type": "application/json"}

    # Request payload
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Get the access token
        access_token = response.json()["access_token"]

        # Update global variables
        _cached_token = access_token
        _token_timestamp = time.time()

        return access_token

    except requests.exceptions.RequestException as e:
        error_message = f"Error making request: {e}"
        if hasattr(e, "response") and hasattr(e.response, "text"):
            error_message += f"\nResponse text: {e.response.text}"
        raise RuntimeError(error_message)


class DocumentParserEndpoint(Enum):
    """Enum for the document parser endpoint."""

    PATIENT_INFORMATION_V1 = "v1/patient-information"
    SUBSCRIBER_INFORMATION_V1 = "v1/subscriber-information"
    MEDICAL_EVALUATION_V1 = "v1/medical-evaluation"
    EOB_V1 = "v1/eob"
    DIAGNOSIS_REPORT_V1 = "v1/diagnosis-report"
    APPROVED_AUTHORIZATION_V1 = "v1/approved-authorization"
    TREATMENT_PLAN_V1 = "v1/treatment-plan"


@dataclass
class StytchCredentials:
    """Class for storing Stytch credentials."""

    client_id: str
    client_secret: str
    project_id: str


def parse_document(
    endpoint: DocumentParserEndpoint,
    file_path: str,
    credentials: StytchCredentials,
    development_mode: bool = True,
) -> dict:
    """Post documents to the document parser endpoint.

    Args:
        endpoint (DocumentParserEndpoint): The endpoint to post the document to.
        file_path (str): The path to the file to upload.
        development_mode (bool, optional): Whether to use development mode. Defaults to True.
        client_id (str, optional): The Stytch client ID. Defaults to None.
        client_secret (str, optional): The Stytch client secret. Defaults to None.
        project_id (str, optional): The Stytch project ID. Defaults to None.

    Returns:
        dict: The JSON response from the API.
    """
    if not development_mode:
        raise Exception("not supported in production")

    # Get authentication token
    token = get_stytch_token(credentials.client_id, credentials.client_secret, credentials.project_id)

    # Determine the base URL based on development mode
    base_url = "https://documents-parser-thoughthub-services.api.thoughthub.thoughtful-dev.ai"

    # Construct full URL
    url = f"{base_url}/{endpoint.value}"

    # Prepare headers with authentication
    headers = {"Authorization": f"Bearer {token}"}

    # Read file content
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Prepare the file for upload
    files = {
        "file": (
            Path(file_path).name,
            file_content,
            "application/octet-stream",
        )
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # Raise an exception for bad status codes

        return response.json()

    except requests.exceptions.RequestException as e:
        error_message = f"Error uploading document: {e}"
        if hasattr(e, "response") and hasattr(e.response, "text"):
            error_message += f"\nResponse text: {e.response.text}"
        raise RuntimeError(error_message)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    client_id = os.getenv("STYTCH_CLIENT_ID")
    client_secret = os.getenv("STYTCH_CLIENT_SECRET")
    project_id = os.getenv("STYTCH_PROJECT_ID")
    test_document_path = os.getenv("TEST_DOCUMENT_PATH")

    if not client_id or not client_secret or not project_id or not test_document_path:
        raise ValueError("Missing required environment variables")

    credentials = StytchCredentials(client_id, client_secret, project_id)

    response = parse_document(
        DocumentParserEndpoint.PATIENT_INFORMATION_V1,
        test_document_path,
        credentials,
        development_mode=True,
    )

    print(response)
