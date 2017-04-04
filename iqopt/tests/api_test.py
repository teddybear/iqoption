# -*- coding: utf-8 -*-
import pytest
from ..app import app as appl
import json


@pytest.fixture(scope="session")
def app(request):
    _app = appl
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
    print dir(client)
    resp = client.post(
        "/translate",
        data=json.dumps({"text": u"Текст", "lang": "en-ru"}),
        content_type="application/json"
    )
    assert resp.status_code == 200


def test_stats(client):
    resp = client.post(
        "/translate/stats",
        data=json.dumps({"text": u"Текст", "lang": "en-ru"}),
        content_type="application/json"
    )
    assert resp.status_code == 200
