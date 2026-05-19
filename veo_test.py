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
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt="A highly professional and beautiful young female secretary confidently walking down a modern sunlit hallway, holding a sleek tablet. Cinematic lighting, ultra photorealistic, highly detailed, 4k.",
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            person_generation="ALLOW_ADULT"
        )
    )

    print(f"Operation started: {operation.name}")
    
    op = operation
    attempts = 0
    while not op.done and attempts < 30:
        print(f"Waiting 10s... (Attempt {attempts+1})")
        time.sleep(10)
        # Re-fetch operation status using get
        op = client.operations.get(operation=op)
        attempts += 1

    if op.done:
        if op.error:
            print("Operation failed with error:", op.error)
        else:
            print("Operation completed!")
            video_bytes = op.response.generated_videos[0].video.video_bytes
            out_path = "/home/gateman/.openclaw/workspace/final_beauty_video.mp4"
            with open(out_path, "wb") as f:
                f.write(video_bytes)
            print(f"Success! Video saved to {out_path}")
    else:
        print("Timeout waiting for operation to complete.")

except Exception as e:
    print(f"Caught Exception: {e}")
