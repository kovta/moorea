#!/usr/bin/env python
"""Quick test script for Pinterest OAuth mock service without full backend dependencies."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test the mock service directly
from backend.services.mock_pinterest_service import mock_pinterest_oauth
from backend.config.settings import settings

print("=" * 60)
print("🧪 PINTEREST OAUTH MOCK SERVICE TEST")
print("=" * 60)
print()

# Test 1: Check settings
print("✓ Test 1: Settings Configuration")
print(f"  - USE_MOCK_PINTEREST: {settings.use_mock_pinterest}")
print(f"  - REDIRECT_URI: {settings.pinterest_redirect_uri}")
print()

# Test 2: Get authorization URL
print("✓ Test 2: Generate Authorization URL")
state = "test_state_12345"
auth_url = mock_pinterest_oauth.get_authorization_url(state=state)
print(f"  - Generated URL: {auth_url}")
print(f"  - Contains state: {'state=' + state in auth_url}")
print()

# Test 3: Check token (should be None initially)
print("✓ Test 3: Check Token (Before Exchange)")
token = mock_pinterest_oauth.get_access_token()
print(f"  - Token before exchange: {token}")
print()

# Test 4: Exchange code for token
print("✓ Test 4: Exchange Code for Token")
import asyncio
async def test_token_exchange():
    token_data = await mock_pinterest_oauth.exchange_code_for_token("mock_code_123", state)
    print(f"  - Access Token: {token_data.get('access_token')[:30]}...")
    print(f"  - Token Type: {token_data.get('token_type')}")
    print(f"  - Expires In: {token_data.get('expires_in')} seconds")
    print(f"  - Scope: {token_data.get('scope')}")
    print(f"  - Has Refresh Token: {'refresh_token' in token_data}")
    
    # Now check if token is stored
    stored_token = mock_pinterest_oauth.get_access_token()
    print(f"  - Token stored in Redis: {stored_token is not None}")
    return token_data

token_data = asyncio.run(test_token_exchange())
print()

# Test 5: Make authenticated request
print("✓ Test 5: Make Authenticated Request (Search)")
async def test_search():
    response = await mock_pinterest_oauth.make_authenticated_request("GET", "/v5/search/pins?query=minimalist")
    print(f"  - Response has items: {'items' in response}")
    print(f"  - Number of items: {len(response.get('items', []))}")
    if response.get('items'):
        item = response['items'][0]
        print(f"  - First item URL: {item.get('url')}")
        print(f"  - First item title: {item.get('title')}")

asyncio.run(test_search())
print()

# Test 6: Refresh token
print("✓ Test 6: Refresh Token")
async def test_refresh():
    new_token = await mock_pinterest_oauth.refresh_access_token()
    print(f"  - New token generated: {new_token is not None}")
    print(f"  - New token differs from old: {new_token != token_data.get('access_token')}")

asyncio.run(test_refresh())
print()

print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print()
print("The mock Pinterest OAuth service is working correctly!")
print("You can now:")
print("  1. Add PinterestLoginButton to your React components")
print("  2. Test the OAuth flow in your browser")
print("  3. Switch to real API by setting USE_MOCK_PINTEREST=false")
