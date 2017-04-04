# -*- coding: utf-8 -*-
import pytest
from ..app import create_app
from ..app import db
import json


@pytest.fixture(scope="session")
def app(request):
    _app = create_app(DB_URI="sqlite://")
    db.app = _app
    db.create_all()
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


def test_smth():
    assert 1 == 1


def test_translate(client):
    resp = client.post(
        "/translate",
        data=json.dumps({"text": u"Текст", "lang": "ru-en"}),
        content_type="application/json"
    )
    assert resp.status_code == 200
    d = json.loads(resp.data)
    assert "lang" in d and d["lang"] == "ru-en"
    assert "translated" in d


def test_stats(client):
    resp = client.post(
        "/translate/stats",
        data=json.dumps({"text": u"Текст", "lang": "ru-en"}),
        content_type="application/json"
    )
    assert resp.status_code == 200
    d = json.loads(resp.data)
    print(resp.data)
    assert "lang" in d[0] and d[0]["lang"] == "ru-en"
    assert "text" in d[0] and d[0]["text"] == u"Текст"
    assert "translated" in d[0]
    assert "requests" in d[0] and d[0]["requests"] == 1
