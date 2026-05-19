import os
import time
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gateman/sa-key.json"

try:
    print("Initializing GenAI client...")
    client = genai.Client(
        vertexai=True,
        project="jason-hsbc",
        location="us-central1"
    )

    print("Submitting video generation request to veo-3.1-generate-preview...")
    # Safe prompt, no weapons or fighting
    prompt = "A very cute little boy doing slow, graceful, and peaceful Tai Chi movements in a serene, beautiful traditional Chinese garden with blooming plum blossoms and a calm pond. High cinematic quality, 4k, peaceful atmosphere."
    
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            person_generation="ALLOW_ADULT"
        )
    )

    print(f"Operation started: {operation.name}")
    
    op = operation
    attempts = 0
    while not op.done and attempts < 60:
        print(f"Waiting 10s... (Attempt {attempts+1})")
        time.sleep(10)
        try:
            op = client.operations.get(operation=op)
        except Exception as poll_e:
            print(f"Poll error: {poll_e}")
        attempts += 1

    if op.done:
        if op.error:
            print("Operation failed with error:", op.error)
        else:
            print("Operation completed!")
            video_bytes = op.response.generated_videos[0].video.video_bytes
            out_path = "/home/gateman/.openclaw/workspace/taichi_boy_video.mp4"
            with open(out_path, "wb") as f:
                f.write(video_bytes)
            print(f"Success! Video saved to {out_path}")
    else:
        print("Timeout waiting for operation to complete.")

except Exception as e:
    print(f"Caught Exception: {e}")
