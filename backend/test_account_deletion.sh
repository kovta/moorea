#!/bin/bash
# Script to test account deletion endpoint

echo "================================================"
echo "Moorea Account Deletion Test Script"
echo "================================================"
echo ""

# Check if backend is running
echo "1. Checking if backend is running..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend is not running at http://localhost:8000"
    echo "Please start the backend first:"
    echo "  cd /Users/tamas-pal.kovacs/dev/match/project-mood-2/backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload"
    exit 1
fi
echo "✅ Backend is running"
echo ""

# Step 1: Register a test user
echo "2. Creating test user..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_delete_user",
    "email": "test_delete@example.com",
    "password": "TestPassword123!"
  }')

echo "Registration response: $REGISTER_RESPONSE"
echo ""

# Step 2: Login to get token
echo "3. Logging in to get authentication token..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test_delete_user&password=TestPassword123!")

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Failed to get authentication token"
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi

echo "✅ Got authentication token: ${TOKEN:0:20}..."
echo ""

# Step 3: Export data first (optional but recommended)
echo "4. Exporting user data (optional)..."
curl -s -X GET http://localhost:8000/api/v1/auth/export-data \
  -H "Authorization: Bearer $TOKEN" \
  -o test_user_export.json

if [ -f test_user_export.json ]; then
    echo "✅ Data exported to test_user_export.json"
else
    echo "⚠️  Data export failed, but continuing..."
fi
echo ""

# Step 4: Delete the account
echo "5. Deleting account..."
DELETE_RESPONSE=$(curl -s -X DELETE http://localhost:8000/api/v1/auth/delete-account \
  -H "Authorization: Bearer $TOKEN")

echo "Deletion response: $DELETE_RESPONSE"
echo ""

# Step 5: Try to access the account (should fail)
echo "6. Verifying account is deleted..."
VERIFY_RESPONSE=$(curl -s -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN")

if echo "$VERIFY_RESPONSE" | grep -q "Could not validate credentials"; then
    echo "✅ Account successfully deleted! Token is invalid."
else
    echo "❌ Account may not be deleted. Response: $VERIFY_RESPONSE"
fi
echo ""

# Step 6: Try to login (should fail)
echo "7. Trying to login with deleted account..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test_delete_user&password=TestPassword123!")

if echo "$LOGIN_RESPONSE" | grep -q "Incorrect username or password"; then
    echo "✅ Login failed as expected! Account is gone."
else
    echo "❌ Login succeeded? Something went wrong. Response: $LOGIN_RESPONSE"
fi
echo ""

echo "================================================"
echo "Test Complete!"
echo "================================================"
echo ""
echo "Summary:"
echo "  - Test user created: test_delete_user"
echo "  - Data exported: test_user_export.json"
echo "  - Account deleted via DELETE /api/v1/auth/delete-account"
echo "  - Verification: Token invalid, login fails"
echo ""
echo "Check test_user_export.json to see the exported data structure"
