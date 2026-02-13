#!/usr/bin/env python3
"""Run a single image through the local moodboard generate endpoint.

Usage:
  python backend/scripts/run_generate_once.py --image backend/images/example.jpg \
      --endpoint http://localhost:8002/api/v1/moodboard/generate/ \
      --outdir backend/results

Sends multipart field 'file' with the image, polls job status, fetches the
final result, and writes:
  - generate_response_<basename>.json (initial POST body or raw text)
  - generate_result_<basename>.json (final result JSON, if completed)
  - generate_response_<basename>.html (simple HTML with anchors when available)
"""

import argparse
import os
import sys
import time
import mimetypes
import json
import requests


def save_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--image', required=True, help='Path to a single image file')
    p.add_argument('--endpoint', default='http://localhost:8002/api/v1/moodboard/generate/', help='Generate endpoint URL')
    p.add_argument('--outdir', default='backend/results', help='Directory to save outputs')
    p.add_argument('--timeout', type=int, default=120, help='Request timeout in seconds')
    p.add_argument('--pinterest-consent', action='store_true', help='Send pinterest_consent=true form field')
    args = p.parse_args()

    image_path = args.image
    endpoint = args.endpoint
    outdir = args.outdir
    timeout = args.timeout

    if not os.path.isfile(image_path):
        print(f"Error: image file not found: {image_path}")
        sys.exit(2)

    os.makedirs(outdir, exist_ok=True)

    basename = os.path.basename(image_path)
    mime, _ = mimetypes.guess_type(image_path)
    mime = mime or 'application/octet-stream'

    print(f"Uploading: {image_path} → {endpoint}")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (basename, f, mime)}
            data = {'pinterest_consent': 'true'} if args.pinterest_consent else None
            r = requests.post(endpoint, files=files, data=data, timeout=timeout)
        print(f"POST HTTP {r.status_code}")
    except Exception as ex:
        print(f"POST error: {ex}")
        sys.exit(1)

    initial_json_path = os.path.join(outdir, f"generate_response_{basename}.json")
    try:
        try:
            body = r.json()
        except Exception:
            body = {'raw': r.text}
        save_json(initial_json_path, body)
        print(f"Saved initial JSON: {initial_json_path}")
    except Exception as ex:
        print(f"Failed to save initial JSON: {ex}")
        body = None

    # If job id is present, poll for completion and fetch result
    final_result = None
    if isinstance(body, dict) and 'job_id' in body and r.status_code in (200, 201, 202):
        job_id = body['job_id']
        # Derive moodboard base from the generate endpoint
        # Example: http://host/api/v1/moodboard/generate -> http://host/api/v1/moodboard
        ep = endpoint.rstrip('/')
        moodboard_base = ep.rsplit('/generate', 1)[0]
        status_url = f"{moodboard_base}/status/{job_id}"
        result_url = f"{moodboard_base}/result/{job_id}"
        print(f"Polling job: {job_id}")
        elapsed = 0.0
        poll_interval = 1.0
        while elapsed < timeout:
            try:
                s = requests.get(status_url, timeout=10)
                if s.status_code == 200:
                    st = s.json()
                    state = (st.get('status') or '').lower()
                    print(f"  status={state} progress={st.get('progress')} elapsed={elapsed:.0f}s")
                    if state == 'completed':
                        res = requests.get(result_url, timeout=20)
                        if res.status_code == 200:
                            try:
                                final_result = res.json()
                            except Exception:
                                print("  result JSON parse failed")
                        break
                    if state == 'failed':
                        print(f"  Job failed: {st.get('error_message')}")
                        break
                else:
                    print(f"  status HTTP {s.status_code}")
            except Exception as ex:
                print(f"  status poll error: {ex}")
            time.sleep(poll_interval)
            elapsed += poll_interval
    else:
        print("No job_id in initial response or POST failed; skipping poll.")

    # Save final result JSON and a simple HTML if we have images
    if final_result:
        res_json_out = os.path.join(outdir, f"generate_result_{basename}.json")
        try:
            save_json(res_json_out, final_result)
            print(f"Saved result JSON: {res_json_out}")
        except Exception as ex:
            print(f"Failed to save result JSON: {ex}")

        imgs = final_result.get('images', []) if isinstance(final_result, dict) else []
        html_lines = ["<html><head><meta charset=\"utf-8\"><title>Moodboard Result</title></head><body>"]
        html_lines.append(f"<h1>Result for {basename}</h1>")
        for img in imgs:
            link = img.get('pinterest_url') or img.get('source_url') or img.get('url') or '#'
            url_for_img = img.get('url') or link
            photographer = img.get('photographer') or ''
            html_lines.append(f'<div style=\"margin:12px\"><a href=\"{link}\" target=\"_blank\" rel=\"noopener noreferrer\"><img src=\"{url_for_img}\" style=\"max-width:300px\"></a><div>{photographer}</div></div>')
        html_lines.append("</body></html>")
        html_out = os.path.join(outdir, f"generate_response_{basename}.html")
        try:
            with open(html_out, 'w', encoding='utf-8') as hf:
                hf.write('\n'.join(html_lines))
            print(f"Saved result HTML: {html_out}")
            if imgs:
                links_found = any(img.get('source_url') or img.get('pinterest_url') for img in imgs)
                print(f"Links present in images: {links_found}")
            else:
                print("No images in final result")
        except Exception as ex:
            print(f"Failed to save HTML: {ex}")
    else:
        print("No final result available; inspect the initial JSON for job_id and errors.")


if __name__ == '__main__':
    main()
