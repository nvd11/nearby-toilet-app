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

image_path = "/home/gateman/.openclaw/media/inbound/686591b3-4eeb-4c3b-869a-48e9b1a86b4b.jpg"
with open(image_path, "rb") as f:
    image_bytes = f.read()

prompt = "A high quality cinematic 4k video of this specific man in a grey winter jacket and glasses, standing in a park. He suddenly summons and wields a massive, glowing red demonic greatsword, striking an epic, intimidating battle pose. Magical red aura, cinematic lighting, photorealistic."

print(f"Starting generation...")
sys.stdout.flush()

try:
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            aspect_ratio="16:9",
            person_generation="ALLOW_ADULT",
            reference_images=[
                types.VideoGenerationReferenceImage(
                    image=types.Image(image_bytes=image_bytes, mime_type="image/jpeg"),
                    reference_type="ASSET"
                )
            ]
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
        with open("aatrox_boss.mp4", "wb") as f:
            f.write(video_bytes)
        print("Saved aatrox_boss.mp4")
except Exception as e:
    import traceback
    traceback.print_exc()

