import json
import os
import requests

yt_api_url = os.environ.get("YT_API_URL")
channels = json.load(open("api.json"))

output_json = []
m3u_lines = ["#EXTM3U"]

for ch in channels:
    video_id = ch["id"]
    url = f"{yt_api_url}{video_id}"

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        hls_url = data.get("hlsManifestUrl")
        if hls_url:
            m3u_lines.append(f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{ch["Name"]}" tvg-logo="{ch["logo"]}",{ch["Name"]}')
            m3u_lines.append(hls_url)

            ch_out = ch.copy()
            ch_out["hlsManifestUrl"] = hls_url
            output_json.append(ch_out)
    except Exception as e:
        print(f"Failed to fetch {video_id}: {e}")

with open("yt_api.json", "w") as f:
    json.dump(output_json, f, indent=2)

with open("yt_playlist.m3u", "w") as f:
    f.write("\n".join(m3u_lines))
