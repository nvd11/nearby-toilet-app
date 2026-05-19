import sys
from google.genai import types
print(dir(types.GenerateVideosConfig))
print("---")
import inspect
print(inspect.signature(types.GenerateVideosConfig))
