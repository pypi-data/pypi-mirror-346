"""
Authentication utility functions for the TestZeus CLI.
"""

import base64
import json
from testzeus_sdk import TestZeusClient
from typing import Dict, Any, Optional, cast


def decode_jwt_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token payload.

    Args:
        token: The JWT token

    Returns:
        Decoded payload as a dictionary, or None if decoding fails
    """
    try:
        # For JWT tokens
        token_parts = token.split(".")
        if len(token_parts) == 3:  # Standard JWT format
            # Decode the payload (middle part)
            payload = token_parts[1]
            # Add padding if needed
            padding = "=" * (4 - len(payload) % 4)
            payload += padding
            # Decode from base64
            decoded = base64.b64decode(payload.replace("-", "+").replace("_", "/"))
            return cast(Dict[str, Any], json.loads(decoded))
    except Exception:
        pass

    return None


def initialize_client_with_token(client: TestZeusClient, token: str) -> None:
    """
    Initialize a TestZeusClient with a token, properly setting up the auth store model.

    Args:
        client: The TestZeusClient instance
        token: JWT token
    """
    # Set the token
    client.token = token
    client._authenticated = True

    # Extract token data
    claims = decode_jwt_payload(token)
    tenant_id = None

    if claims:
        # Check for tenant ID in various possible locations within the token
        if "tenant" in claims:
            tenant_id = claims["tenant"]
        elif "record" in claims and "tenant" in claims["record"]:
            tenant_id = claims["record"]["tenant"]
        elif "collectionId" in claims:
            # Use collection ID as a fallback
            tenant_id = claims["collectionId"]

    # If no tenant ID found in token, use the default
    if not tenant_id:
        tenant_id = "pbc_138639755"  # Default tenant ID for TestZeus

    # Save the token to the auth store - don't try to set the model property directly
    # as it's read-only. Instead, just save the token and let PocketBase handle it.
    client.pb.auth_store.save(token, None)

    # Add tenant ID directly to the client for easy access
    # This is the important part - ensure the tenant ID is accessible
    setattr(client, "_tenant_id", tenant_id)


def extract_tenant_from_token(token: str) -> str:
    """
    Extract tenant ID from a JWT token.

    Args:
        token: The JWT token

    Returns:
        Tenant ID or default ID if not found
    """
    claims = decode_jwt_payload(token)

    if claims:
        # Check for tenant ID in various possible locations
        if "tenant" in claims:
            return str(claims["tenant"])
        elif "record" in claims and "tenant" in claims["record"]:
            return str(claims["record"]["tenant"])
        elif "collectionId" in claims:
            return str(claims["collectionId"])

    # Default tenant ID for TestZeus
    return "pbc_138639755"
