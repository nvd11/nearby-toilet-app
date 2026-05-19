import sys
import os
import time
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gateman/sa-key.json"

image_path = sys.argv[1]
output_path = sys.argv[2]
prompt = "A person in a yellow sweater and dark pants is happily walking and playing on a wooden suspension bridge. Bright, joyful atmosphere, cinematic lighting."

try:
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    print("Initializing GenAI client...")
    client = genai.Client(
        vertexai=True,
        project="jason-hsbc",
        location="us-central1"
    )

    print("Submitting video generation request to veo-3.1-generate-preview...")
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            person_generation="ALLOW_ADULT",
            reference_images=[
                types.VideoGenerationReferenceImage(
                    image=types.Image(imageBytes=image_bytes, mimeType="image/jpeg"),
                    reference_type="ASSET"
                )
            ]
        )
    )

    print(f"Operation started: {operation.name}")
    
    op = operation
    attempts = 0
    while not op.done and attempts < 60:
        print(f"Waiting 10s... (Attempt {attempts+1})")
        time.sleep(10)
        op = client.operations.get(operation=op)
        attempts += 1

    if op.done:
        if op.error:
            print("Operation failed with error:", op.error)
        else:
            print("Operation completed!")
            video_bytes = op.response.generated_videos[0].video.video_bytes
            with open(output_path, "wb") as f:
                f.write(video_bytes)
            print(f"Success! Video saved to {output_path}")
    else:
        print("Timeout waiting for operation to complete.")

except Exception as e:
    print(f"Caught Exception: {e}")
