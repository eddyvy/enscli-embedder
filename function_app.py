import azure.functions as func
from file_embedder.controller import post_embedder

app = func.FunctionApp()


@app.function_name(name="EnscliFileEmbedder")
@app.route(route="embed/{project_name}", methods=["POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    return post_embedder(req)
