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

    image_path = "/home/gateman/.openclaw/media/inbound/01c205a0-7c55-4345-ac22-526676a58c65.jpg"
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    
    img_part = types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")

    print("Submitting video generation request to veo-3.1-generate-preview...")
    # Very safe prompt, no weapons, no kids mentioned, just eating watermelon.
    prompt = "A person happily eating a large, juicy slice of red watermelon on a bright, sunny summer day. Photorealistic, 4k resolution, joyful and bright atmosphere."
    
    # Veo currently supports image + text prompts for video generation?
    # Actually wait, Veo 3.1 video generation only accepts string prompts right now according to the previous error!
    # Ah! The error from earlier was:
    # `Input should be a valid string ... input_type=list`
    # Veo does not support image inputs via this SDK yet. It only takes text prompts!
    
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
            out_path = "/home/gateman/.openclaw/workspace/watermelon_video.mp4"
            with open(out_path, "wb") as f:
                f.write(video_bytes)
            print(f"Success! Video saved to {out_path}")
    else:
        print("Timeout waiting for operation to complete.")

except Exception as e:
    print(f"Caught Exception: {e}")
