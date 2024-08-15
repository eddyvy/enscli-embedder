import azure.functions as func

def run(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("success", status_code=200)

