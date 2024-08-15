import azure.functions as func
import file_embedder.main as file_embedder


def test_main():
    req = func.HttpRequest(
        method='GET',
        url='/api/req',
        headers={},
        params={},
        body=None
    )

    resp = file_embedder.run(req)

    assert isinstance(resp, func.HttpResponse)
    assert resp.status_code == 200
    assert resp.get_body().decode() == 'success'
