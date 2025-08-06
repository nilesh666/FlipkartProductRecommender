from huggingface_hub import InferenceClient
from src.config import Config

client = InferenceClient(
    model="BAAI/bge-base-en-v1.5",
    token="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"
)

response = client.feature_extraction("test sentence")
print(response)
