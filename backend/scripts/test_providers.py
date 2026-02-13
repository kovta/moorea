#!/usr/bin/env python3
"""Quick provider test to verify keys and fetch sample candidates."""

import asyncio
import json
import sys
from pathlib import Path

# Ensure backend package is on sys.path when running from anywhere
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from config import settings
from services.unsplash_client import unsplash_client
from services.pexels_client import pexels_client
from services.flickr_client import flickr_client


async def main():
    print("Provider config:")
    print(json.dumps({
        "unsplash_configured": bool(settings.unsplash_access_key),
        "pexels_configured": bool(settings.pexels_api_key),
        "flickr_configured": bool(settings.flickr_api_key),
    }, indent=2))

    keywords = ["minimalist outfit", "vintage fashion", "cottagecore dress"]

    async def test_unsplash():
        if not settings.unsplash_access_key:
            print("Unsplash: key not configured")
            return
        print("Testing Unsplash...")
        results = []
        for kw in keywords:
            try:
                res = await unsplash_client.search_photos(kw, per_page=4)
                print(f"  {kw}: {len(res)} images")
                results.extend(res)
            except Exception as e:
                print(f"  {kw}: error {e}")
        print(f"Unsplash total: {len(results)}")
        for c in results[:3]:
            print(json.dumps(c.dict(), indent=2))

    async def test_pexels():
        if not settings.pexels_api_key:
            print("Pexels: key not configured")
            return
        print("Testing Pexels...")
        results = []
        for kw in keywords:
            try:
                res = await pexels_client.search_photos(kw, per_page=4)
                print(f"  {kw}: {len(res)} images")
                results.extend(res)
            except Exception as e:
                print(f"  {kw}: error {e}")
        print(f"Pexels total: {len(results)}")
        for c in results[:3]:
            print(json.dumps(c.dict(), indent=2))

    async def test_flickr():
        if not settings.flickr_api_key:
            print("Flickr: key not configured")
            return
        print("Testing Flickr...")
        results = []
        for kw in keywords:
            try:
                res = await flickr_client.search_photos(kw, per_page=4)
                print(f"  {kw}: {len(res)} images")
                results.extend(res)
            except Exception as e:
                print(f"  {kw}: error {e}")
        print(f"Flickr total: {len(results)}")
        for c in results[:3]:
            print(json.dumps(c.dict(), indent=2))

    await test_unsplash()
    await test_pexels()
    await test_flickr()


if __name__ == "__main__":
    asyncio.run(main())
