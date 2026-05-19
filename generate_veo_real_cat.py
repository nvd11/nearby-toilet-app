import os
import sys
import time
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gateman/sa-key.json"

client = genai.Client(
    vertexai=True,
    project="jason-hsbc",
    location="us-central1"
)

prompt = sys.argv[1]

print(f"Starting generation for: {prompt}")
sys.stdout.flush()

try:
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
    sys.stdout.flush()

    op = operation
    while not op.done:
        print("Waiting 10s...")
        sys.stdout.flush()
        time.sleep(10)
        op = client.operations.get(operation=op)

    if op.error:
        print("Error!", op.error)
    else:
        print("Success!")
        video_bytes = op.response.generated_videos[0].video.video_bytes
        with open("realistic_cat_fish.mp4", "wb") as f:
            f.write(video_bytes)
        print("Saved realistic_cat_fish.mp4")
except Exception as e:
    import traceback
    traceback.print_exc()

