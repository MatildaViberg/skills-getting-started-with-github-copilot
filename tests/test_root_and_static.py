def test_root_redirects(client):
    resp = client.get("/", allow_redirects=False)
    assert resp.status_code in (301, 302, 307)


def test_static_served(client):
    resp = client.get("/static/app.js")
    assert resp.status_code == 200
    assert "document.addEventListener" in resp.text
