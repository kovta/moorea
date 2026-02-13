#!/usr/bin/env python3
"""Batch-upload images to the local moodboard generate endpoint.

Usage:
    python backend/scripts/batch_generate.py --folder backend/images --endpoint http://localhost:8002/api/v1/moodboard/generate/ --outdir backend/results

The script posts each image file in --folder (non-recursive by default) as multipart form `image`.
It saves the HTML response for each image as `generate_response_<basename>.html` in --outdir.
"""

import argparse
import os
import sys
import mimetypes
import time
import requests


def iter_images(folder, recursive=False):
    exts = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    if recursive:
        for root, _, files in os.walk(folder):
            for fn in files:
                if os.path.splitext(fn.lower())[1] in exts:
                    yield os.path.join(root, fn)
    else:
        for fn in sorted(os.listdir(folder) if os.path.isdir(folder) else []):
            if os.path.splitext(fn.lower())[1] in exts:
                yield os.path.join(folder, fn)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--folder', required=True, help='Folder containing image files')
    p.add_argument('--endpoint', default='http://localhost:8002/api/v1/moodboard/generate/', help='Generate endpoint URL')
    p.add_argument('--outdir', default='backend/results', help='Directory to save generated JSON/HTML')
    p.add_argument('--recursive', action='store_true', help='Search recursively')
    p.add_argument('--timeout', type=int, default=120, help='Request timeout in seconds')
    args = p.parse_args()

    folder = args.folder
    endpoint = args.endpoint
    outdir = args.outdir
    timeout = args.timeout

    if not os.path.isdir(folder):
        print(f"Error: folder does not exist: {folder}")
        sys.exit(2)

    ensure_dir(outdir)

    images = list(iter_images(folder, args.recursive))
    if not images:
        print(f"No images found in: {folder}")
        return

    print(f"Found {len(images)} images. Posting to {endpoint}")

    for idx, img_path in enumerate(images, start=1):
        basename = os.path.basename(img_path)
        out_file = os.path.join(outdir, f"generate_response_{basename}.html")
        print(f"[{idx}/{len(images)}] {basename} -> {out_file}")

        mime, _ = mimetypes.guess_type(img_path)
        mime = mime or 'application/octet-stream'

        try:
            with open(img_path, 'rb') as f:
                # FastAPI endpoint expects the UploadFile field name 'file'
                files = {'file': (basename, f, mime)}
                r = requests.post(endpoint, files=files, timeout=timeout)

            print(f"  HTTP {r.status_code}")

            # If the API returned a job id, poll for completion and fetch result
            try:
                body = r.json()
            except Exception:
                body = None

            if r.status_code in (200, 201, 202) and body and 'job_id' in body:
                job_id = body['job_id']
                # Derive moodboard base from the generate endpoint
                ep = endpoint.rstrip('/')
                moodboard_base = ep.rsplit('/generate', 1)[0]
                status_url = f"{moodboard_base}/status/{job_id}"
                result_url = f"{moodboard_base}/result/{job_id}"

                # Poll for completion
                print(f"  Job queued: {job_id}. Polling for completion...")
                poll_timeout = timeout
                poll_interval = 1.0
                elapsed = 0.0
                final_result = None
                while elapsed < poll_timeout:
                    try:
                        s = requests.get(status_url, timeout=10)
                        if s.status_code == 200:
                            status_json = s.json()
                            state = status_json.get('status')
                            print(f"    status={state} progress={status_json.get('progress')}")
                            if state and state.lower() == 'completed':
                                # fetch result
                                res = requests.get(result_url, timeout=20)
                                if res.status_code == 200:
                                    final_result = res.json()
                                break
                            if state and state.lower() == 'failed':
                                print(f"    Job failed: {status_json.get('error_message')}")
                                break
                        else:
                            print(f"    status check HTTP {s.status_code}")
                    except Exception as ex:
                        print(f"    status poll error: {ex}")
                    time.sleep(poll_interval)
                    elapsed += poll_interval

                # Save the API response body for debugging
                json_out = os.path.join(outdir, f"generate_response_{basename}.json")
                try:
                    with open(json_out, 'w', encoding='utf-8') as jf:
                        import json
                        json.dump(body, jf, indent=2)
                except Exception:
                    pass

                if final_result:
                    # Save result JSON
                    res_json_out = os.path.join(outdir, f"generate_result_{basename}.json")
                    with open(res_json_out, 'w', encoding='utf-8') as rf:
                        import json
                        json.dump(final_result, rf, indent=2)

                    # Build a simple HTML that links images to source_url/url
                    imgs = final_result.get('images', [])
                    html_lines = ["<html><head><meta charset=\"utf-8\"><title>Moodboard Result</title></head><body>"]
                    html_lines.append(f"<h1>Result for {basename}</h1>")
                    for img in imgs:
                        link = img.get('pinterest_url') or img.get('source_url') or img.get('url')
                        url_for_img = img.get('url') or link
                        photographer = img.get('photographer') or ''
                        html_lines.append(f'<div style=\"margin:12px\"><a href=\"{link}\" target=\"_blank\" rel=\"noopener noreferrer\"><img src=\"{url_for_img}\" style=\"max-width:300px\"></a><div>{photographer}</div></div>')
                    html_lines.append("</body></html>")

                    html_out = os.path.join(outdir, f"generate_response_{basename}.html")
                    with open(html_out, 'w', encoding='utf-8') as hf:
                        hf.write('\n'.join(html_lines))

                    print(f"  Saved result JSON to: {res_json_out}")
                    print(f"  Saved result HTML to: {html_out}")
                    if imgs:
                        links_found = any(img.get('source_url') or img.get('pinterest_url') for img in imgs)
                        print(f"  Links present in images: {links_found}")
                    else:
                        print("  No images in final result")
                else:
                    print("  No final result available yet; check job status later.")

            else:
                # Save raw response body (non-JSON) for inspection
                with open(out_file, 'wb') as fo:
                    fo.write(r.content)
                # Also save a JSON file capturing the raw text for debugging
                json_out = os.path.join(outdir, f"generate_response_{basename}.json")
                try:
                    with open(json_out, 'w', encoding='utf-8') as jf:
                        import json
                        # Attempt to parse JSON; if it fails, store as raw text
                        try:
                            jf.write(json.dumps(r.json(), indent=2))
                        except Exception:
                            jf.write(json.dumps({"raw": r.text}, indent=2))
                    print(f"  Saved initial JSON to: {json_out}")
                except Exception as ex:
                    print(f"  Failed to save initial JSON: {ex}")
                if b'href=\"http' in r.content:
                    print("  hrefs found in response")
                else:
                    print("  no hrefs found in response")

        except Exception as e:
            print(f"  ERROR for {basename}: {e}")
