import json
import os
import sys

import requests


BASE = os.environ.get("MINIMAX_TTS_BASE_URL", "https://api.minimaxi.com")
KEY = os.environ["MINIMAX_API_KEY"]


def upload_audio(path: str) -> str:
    url = BASE.rstrip("/") + "/v1/files/upload"
    with open(path, "rb") as fh:
        files = {"file": (os.path.basename(path), fh, "audio/mpeg")}
        data = {"purpose": "voice_clone"}
        headers = {"Authorization": "Bearer " + KEY}
        resp = requests.post(url, files=files, data=data, headers=headers, timeout=240)
    try:
        payload = resp.json()
    except Exception:
        print("UPLOAD_HTTP", resp.status_code, resp.text, file=sys.stderr)
        raise SystemExit(2)
    file_id = (payload.get("file") or {}).get("file_id") or payload.get("file_id")
    if not file_id:
        print("UPLOAD_NO_FILE_ID", json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(3)
    print("UPLOADED", file_id)
    return file_id


def clone_voice(file_id: str, voice_id: str) -> str:
    url = BASE.rstrip("/") + "/v1/voice_clone"
    headers = {"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}
    body = {"file_id": file_id, "voice_id": voice_id}
    resp = requests.post(url, headers=headers, json=body, timeout=240)
    try:
        payload = resp.json()
    except Exception:
        print("CLONE_HTTP", resp.status_code, resp.text, file=sys.stderr)
        raise SystemExit(4)
    code = (payload.get("base_resp") or {}).get("status_code")
    if code not in (0, None):
        msg = (payload.get("base_resp") or {}).get("status_msg", "unknown")
        print("CLONE_ERR", code, msg, json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(5)
    print("CLONED", voice_id)
    return voice_id


def main() -> None:
    audio_path, voice_id = sys.argv[1], sys.argv[2]
    file_id = upload_audio(audio_path)
    clone_voice(file_id, voice_id)
    print(json.dumps({"voice_id": voice_id, "file_id": file_id}, ensure_ascii=False))


if __name__ == "__main__":
    main()
