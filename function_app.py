import azure.functions as func
from embed.controller import post_embed_project

app = func.FunctionApp()


@app.function_name(name="EnscliEmbedProject")
@app.route(route="embed/{project}", methods=["POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    return post_embed_project(req)
