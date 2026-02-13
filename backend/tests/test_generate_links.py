import sys
import types
import os

# Insert lightweight dummy modules for services to avoid heavy imports
services_pkg = types.ModuleType("services")
sys.modules["services"] = services_pkg

for name in [
    "services.aesthetic_service",
    "services.clip_service",
    "services.moodboard_service",
    "services.unsplash_client",
    "services.pexels_client",
    "services.flickr_client",
]:
    mod = types.ModuleType(name)
    # Provide placeholder attributes that the module import expects
    base = name.split('.')[-1]
    if base == 'unsplash_client':
        setattr(mod, 'unsplash_client', object())
    if base == 'pexels_client':
        setattr(mod, 'pexels_client', object())
    if base == 'flickr_client':
        setattr(mod, 'flickr_client', object())
    if base == 'aesthetic_service':
        setattr(mod, 'aesthetic_service', object())
    if base == 'clip_service':
        setattr(mod, 'clip_service', object())
    if base == 'moodboard_service':
        setattr(mod, 'moodboard_service', object())
    sys.modules[name] = mod


def run_test():
    # Ensure backend folder is on sys.path so local module can be imported
    backend_path = os.path.join(os.getcwd(), "backend")
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    # Import the generator after stubbing services
    from generate_moodboard import generate_html_moodboard

    class FakeImage:
        def __init__(self, url, thumbnail_url, photographer, source_api, source_url=None):
            self.url = url
            self.thumbnail_url = thumbnail_url
            self.photographer = photographer
            self.source_api = source_api
            # Some clients set source_url but ImageCandidate model may not include it
            self.source_url = source_url

    img = FakeImage(
        url="https://example.com/photo.jpg",
        thumbnail_url="https://example.com/thumb.jpg",
        photographer="Jane Doe",
        source_api="pexels",
        source_url="https://pexels.com/photo/12345"
    )

    html = generate_html_moodboard(
        aesthetic_name="cottagecore",
        description="A test description",
        keywords=["flower", "vintage"],
        images=[img],
        original_image_path="/tmp/orig.jpg"
    )

    # Check for an anchor linking to image.source_url
    href = f'href="{img.source_url}"'
    if img.source_url and href in html:
        print("PASS: anchor found")
        return 0
    else:
        print("FAIL: anchor not found in generated HTML")
        # For debugging, write the html to a temp file
        out = os.path.join(os.getcwd(), "test_generate_output.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Wrote generated HTML to: {out}")
        return 2


if __name__ == '__main__':
    raise SystemExit(run_test())
