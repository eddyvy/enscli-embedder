import azure.functions as func
from file_embedder.main import run

app = func.FunctionApp()

@app.function_name(name="EnscliFileEmbedder")
@app.route(route="req")
def main(req: func.HttpRequest) -> func.HttpResponse:
    return run(req)

