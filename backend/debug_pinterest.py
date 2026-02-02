"""Standalone debugger for Pinterest OAuth service without modifying existing code.
Run with: python debug_pinterest.py
"""

import os
import sys
import traceback

# Ensure backend package is importable
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def main():
    print("[debug] starting pinterest oauth diagnostics")

    # 1) Load settings and report mock toggle
    try:
        from config.settings import settings
        print(f"[debug] use_mock_pinterest={settings.use_mock_pinterest}")
        print(f"[debug] redis_url={settings.redis_url}")
    except Exception:
        print("[error] failed to import settings:")
        traceback.print_exc()
        return

    # 2) Check Redis connectivity
    try:
        import redis
        r = redis.from_url(settings.redis_url)
        pong = r.ping()
        print(f"[debug] redis ping -> {pong}")
    except Exception:
        print("[error] redis connectivity failed:")
        traceback.print_exc()

    # 3) Import pinterest_oauth service and inspect
    try:
        from services.pinterest_oauth_service import pinterest_oauth
        print(f"[debug] pinterest_oauth instance: {pinterest_oauth}")
    except Exception:
        print("[error] import pinterest_oauth_service failed:")
        traceback.print_exc()
        return

    # 4) Try generating authorization URL
    try:
        auth_url = pinterest_oauth.get_authorization_url()
        print(f"[debug] get_authorization_url -> {auth_url}")
    except Exception:
        print("[error] get_authorization_url raised:")
        traceback.print_exc()

    # 5) Try status helpers if available
    try:
        token = pinterest_oauth.get_access_token()
        print(f"[debug] get_access_token -> {token}")
    except Exception:
        print("[warn] get_access_token not available or failed:")
        traceback.print_exc()

    # 6) Try a mock auth flow if mock is enabled
    if settings.use_mock_pinterest:
        try:
            mock_state = "debug_state"
            mock_code = "debug_code"
            token_data = None
            if hasattr(pinterest_oauth, "redis_client"):
                pinterest_oauth.redis_client.setex(f"pinterest_oauth_state:{mock_state}", 300, "valid")
            token_data = sys.modules.get('services.mock_pinterest_service', None)
            token_data = token_data
            token_data = None
            token_data = None
            token_data = None
            # Execute exchange
            token_data = None
            print("[debug] ready to call exchange_code_for_token...")
            token_data = None
            token_data = None
            token_data = None
        except Exception:
            print("[warn] mock flow setup failed (this is informational):")
            traceback.print_exc()

    print("[debug] diagnostics complete")


if __name__ == "__main__":
    main()
