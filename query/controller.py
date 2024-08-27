import json
import logging
import azure.functions as func

from query.service import index_query
from llama_index.embeddings.openai import OpenAIEmbeddingModelType


def post_query_project(req: func.HttpRequest) -> func.HttpResponse:
    try:
        project_name = req.route_params.get('project')
        req_body = req.get_json()
        query = req_body.get('query')
        top_k = int(req_body.get('top_k', 0))
        model = req_body.get('model')

        if query is None or top_k is None:
            return func.HttpResponse("Missing 'query' or 'top_k' or 'model' request body params", status_code=400)

        if model is None:
            model = OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL

        chunks = index_query(project_name, query, top_k, model)
        chunks_json = json.dumps(chunks)

        return func.HttpResponse(chunks_json, status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
