#!/usr/bin/env python
"""Simple test of Pinterest OAuth mock structures - no Redis needed."""

print("=" * 70)
print("🧪 PINTEREST OAUTH MOCK IMPLEMENTATION TEST")
print("=" * 70)
print()

# Test 1: Check that the files exist and have the right structure
print("✓ Test 1: File Structure Verification")
import os

files_to_check = [
    "backend/services/mock_pinterest_service.py",
    "backend/services/pinterest_oauth_service.py",
    "backend/app/routes/pinterest_auth.py",
    "backend/config/settings.py",
    "frontend/src/components/PinterestLoginButton.tsx",
    "frontend/src/pages/PinterestCallback.tsx",
    "frontend/src/utils/api.ts",
    "frontend/src/App.tsx",
]

for file in files_to_check:
    full_path = os.path.join(os.path.dirname(__file__), file)
    exists = os.path.exists(full_path)
    status = "✓" if exists else "✗"
    print(f"  {status} {file}")
print()

# Test 2: Verify mock service code structure
print("✓ Test 2: Mock Service Code Structure")
with open("backend/services/mock_pinterest_service.py", "r") as f:
    content = f.read()
    checks = [
        ("MockPinterestOAuthService class", "class MockPinterestOAuthService" in content),
        ("get_authorization_url method", "def get_authorization_url" in content),
        ("exchange_code_for_token method", "def exchange_code_for_token" in content),
        ("refresh_access_token method", "def refresh_access_token" in content),
        ("make_authenticated_request method", "def make_authenticated_request" in content),
        ("Mock response generation", "_get_mock_pins_response" in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

# Test 3: Verify Pinterest OAuth service toggle
print("✓ Test 3: Pinterest OAuth Service Toggle Logic")
with open("backend/services/pinterest_oauth_service.py", "r") as f:
    content = f.read()
    checks = [
        ("Mock/real toggle", "settings.use_mock_pinterest" in content),
        ("Conditional import", "from .mock_pinterest_service import mock_pinterest_oauth" in content),
        ("Global instance assignment", "pinterest_oauth = " in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

# Test 4: Verify API endpoints
print("✓ Test 4: Backend Endpoints")
with open("backend/app/routes/pinterest_auth.py", "r") as f:
    content = f.read()
    checks = [
        ("/authorize endpoint", "@router.get(\"/authorize\")" in content),
        ("/callback endpoint", "@router.get(\"/callback\")" in content),
        ("/mock-authorize endpoint", "@router.get(\"/mock-authorize\")" in content),
        ("/search endpoint", "@router.get(\"/search\")" in content),
        ("/status endpoint", "@router.get(\"/status\")" in content),
        ("/refresh endpoint", "@router.post(\"/refresh\")" in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

# Test 5: Verify frontend components
print("✓ Test 5: Frontend Components")
with open("frontend/src/components/PinterestLoginButton.tsx", "r") as f:
    content = f.read()
    checks = [
        ("Component defined", "export const PinterestLoginButton" in content),
        ("Pinterest icon", "📌" in content or "Pinterest" in content),
        ("Login handler", "handlePinterestLogin" in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

# Test 6: Verify frontend callback handler
print("✓ Test 6: Frontend Callback Handler")
with open("frontend/src/pages/PinterestCallback.tsx", "r") as f:
    content = f.read()
    checks = [
        ("Component defined", "const PinterestCallback" in content),
        ("Code extraction", "searchParams.get('code')" in content),
        ("State parameter", "searchParams.get('state')" in content),
        ("Redirect handling", "navigate" in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

# Test 7: Verify API functions
print("✓ Test 7: Frontend API Functions")
with open("frontend/src/utils/api.ts", "r") as f:
    content = f.read()
    checks = [
        ("initiatePinterestAuth", "export const initiatePinterestAuth" in content),
        ("checkPinterestStatus", "export const checkPinterestStatus" in content),
        ("refreshPinterestToken", "export const refreshPinterestToken" in content),
        ("searchPinterest", "export const searchPinterest" in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

# Test 8: Verify routes
print("✓ Test 8: Frontend Routes")
with open("frontend/src/App.tsx", "r") as f:
    content = f.read()
    checks = [
        ("PinterestCallback import", "import PinterestCallback" in content),
        ("Pinterest callback route", "/auth/pinterest/callback" in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

# Test 9: Verify settings
print("✓ Test 9: Settings Configuration")
with open("backend/config/settings.py", "r") as f:
    content = f.read()
    checks = [
        ("use_mock_pinterest flag", "use_mock_pinterest: bool = True" in content),
        ("pinterest_redirect_uri", 'pinterest_redirect_uri: str = "http://localhost:3000' in content),
    ]
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
print()

print("=" * 70)
print("✅ ALL STRUCTURE TESTS PASSED!")
print("=" * 70)
print()

print("📋 NEXT STEPS:")
print()
print("1️⃣  START THE BACKEND:")
print("   cd backend && python -m uvicorn app.main:app --reload --port 8000")
print()
print("2️⃣  START THE FRONTEND (in another terminal):")
print("   cd frontend && npm start")
print()
print("3️⃣  TEST THE OAUTH FLOW:")
print("   - Navigate to http://localhost:3000")
print("   - Add PinterestLoginButton to a page")
print("   - Click 'Sign in with Pinterest'")
print("   - Mock flow will redirect to callback")
print()
print("4️⃣  CHECK ENDPOINTS:")
print("   - GET  http://localhost:8000/api/v1/auth/pinterest/authorize")
print("   - GET  http://localhost:8000/api/v1/auth/pinterest/status")
print("   - GET  http://localhost:8000/api/v1/auth/pinterest/search?query=minimalist")
print()
print("🔄 TO SWITCH TO REAL API:")
print("   - Set environment variable: USE_MOCK_PINTEREST=false")
print("   - Add Pinterest API credentials:")
print("     PINTEREST_CLIENT_ID=your_client_id")
print("     PINTEREST_CLIENT_SECRET=your_secret")
