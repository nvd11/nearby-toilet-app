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

    image_path = "/home/gateman/.openclaw/media/inbound/df0832c8-f3fd-43e7-a7e4-be8d7a531174.png"
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    # Using snake_case for Pydantic models (image_bytes -> imageBytes under the hood usually, but kwargs usually accept snake_case in google-genai)
    ref_img = types.VideoGenerationReferenceImage(
        reference_type="ASSET", 
        image=types.Image(image_bytes=img_bytes, mime_type="image/png")
    )

    print("Submitting video generation request to veo-3.1-generate-preview...")
    # Safe prompt, no weapons or children mentioned explicitly to avoid filters.
    prompt = "A heroic young futuristic character holding a bright glowing blue neon energy staff, striking a very cool heroic pose. Standing in a highly detailed, cinematic sci-fi spaceship hallway with dark shadows and neon lights. 4k resolution, epic sci-fi lighting."
    
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            person_generation="ALLOW_ADULT",
            reference_images=[ref_img]
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
            out_path = "/home/gateman/.openclaw/workspace/veo_jedi_hero.mp4"
            with open(out_path, "wb") as f:
                f.write(video_bytes)
            print(f"Success! Video saved to {out_path}")
    else:
        print("Timeout waiting for operation to complete.")

except Exception as e:
    print(f"Caught Exception: {e}")
