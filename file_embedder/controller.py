import azure.functions as func

from file_embedder.file_request import FileRequest
from file_embedder.service import execute_embedding

def post_embedder(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file_request = FileRequest(req)

        error_message = file_request.error_message()
        if error_message != None:
            return func.HttpResponse(error_message, status_code=400)
    
        execute_embedding(file_request)

        return func.HttpResponse("success", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=400)
