import os
import time
from google import genai
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gateman/sa-key.json"

# Initialize the client. Since we are using Vertex AI, we need to specify vertexai=True and the location/project
client = genai.Client(vertexai=True, project="jason-hsbc", location="us-central1")

print("Starting Veo 3.1 generation...")

# Generate the video using the long-running operation
op = client.models.generate_videos(
    model='veo-3.1-generate-preview',
    prompt='A beautiful anime style scene: A mischievous blue cat wearing a tiny red scarf tries to catch a shimmering golden fish swimming in a floating water bubble, magical atmosphere, vibrant colors, Studio Ghibli inspired, high quality 4k animation',
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        person_generation="ALLOW_ADULT"
    )
)

print(f"Operation started: {op.name}")

# Poll the operation status
print("Polling for completion...")
while not op.done:
    print(".", end="", flush=True)
    time.sleep(10)
    op = client.operations.get(operation=op)

print("\nOperation completed!")

if op.error:
    print(f"Error: {op.error}")
else:
    # Assuming the response structure has the video bytes
    try:
        if op.response and op.response.generated_videos:
            video_bytes = op.response.generated_videos[0].video.video_bytes
            with open("/home/gateman/.openclaw/workspace/final_blue_cat.mp4", "wb") as f:
                f.write(video_bytes)
            print("Video saved to /home/gateman/.openclaw/workspace/final_blue_cat.mp4")
        else:
            print("No video bytes found in the response.")
            print(op.response)
    except Exception as e:
        print(f"Failed to extract video: {e}")
        print(op)
