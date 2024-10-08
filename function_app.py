import azure.functions as func
from auth import basic_auth
from embed.controller import post_embed_project
from query.controller import post_query_project

app = func.FunctionApp()


@app.function_name(name="EnscliEmbedProject")
@app.route(route="embed/{project}", methods=["POST"])
@basic_auth()
def embed_project(req: func.HttpRequest) -> func.HttpResponse:
    return post_embed_project(req)


@app.function_name(name="EnscliQueryProject")
@app.route(route="query/{project}", methods=["POST"])
@basic_auth()
def query_project(req: func.HttpRequest) -> func.HttpResponse:
    return post_query_project(req)
