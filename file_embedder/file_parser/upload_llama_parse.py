import os
import requests
import time

from file_embedder.file_parser.parsing_params import ParsingParams
from requests_toolbelt.multipart.encoder import MultipartEncoder

def upload_llama_parse_pdf(file_content: bytes, file_name: str, parsing_params: ParsingParams) -> str:
    llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

    if not llama_cloud_api_key:
        raise EnvironmentError("LLAMA_CLOUD_API_KEY environment variable is not set")

    url = "https://api.cloud.llamaindex.ai/api/v1/parsing/upload"

    headers = {
        "Content-Type": "multipart/form-data",
        "Accept": "application/json",
        "Authorization": "Bearer " + llama_cloud_api_key
    }

    fields = {
        "file": (file_name, file_content, "application/pdf")
    }

    parsing_instruction = parsing_params.get_parsing_instruction()
    if parsing_instruction:
        fields["parsing_instruction"] = parsing_instruction

    lang = parsing_params.get_lang()
    if lang:
        fields["lang"] = lang

    multipart_data = MultipartEncoder(fields=fields)

    response = requests.request(method="POST", url=url, headers=headers, data=multipart_data.to_string())
    response_json = response.json()
    id_value = response_json.get("id")
    status = response_json.get("status")

    if not id_value or not status:
        raise ValueError("Failed to obtain uploaded id file from LLAMA Cloud")
    
    get_url = "https://api.cloud.llamaindex.ai/api/v1/parsing/job/" + id_value
    get_headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + llama_cloud_api_key
    }

    times = 0
    while status == "PENDING":
        time.sleep(2)
        response = requests.request(method="GET", url=get_url, headers=get_headers)
        response_json = response.json()
        status = response_json.get("status")
        times += 1
        if times >= 60:
            raise ValueError("Max time exceeded to parse PDF file with LLAMA Cloud")

    if status != "SUCCESS":
        raise ValueError("Failed to parse PDF file with LLAMA Cloud")

    return id_value
