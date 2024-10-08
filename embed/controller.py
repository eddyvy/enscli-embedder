import logging
import azure.functions as func

from embed.service import execute_embedding
from llama_index.embeddings.openai import OpenAIEmbeddingModelType


def post_embed_project(req: func.HttpRequest) -> func.HttpResponse:
    try:
        project_name = req.route_params.get('project')

        file = None
        for input_file in req.files.values():
            file = input_file
            break

        model = OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL
        for key, value in req.form.items():
            if key == "model":
                model = value

        if file == None:
            return func.HttpResponse("No file uploaded", status_code=400)

        content: str = file.stream.read().decode("utf-8")
        execute_embedding(content, project_name, model)

        return func.HttpResponse("success", status_code=200)
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
