import requests
import os

def get_llama_parse(job_id: str) -> str:
    llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    if not llama_cloud_api_key:
        raise EnvironmentError("LLAMA_CLOUD_API_KEY environment variable is not set")

    url = f"https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}/result/text"

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + llama_cloud_api_key
    }

    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()

    return response.json()["text"].encode("utf-8")
