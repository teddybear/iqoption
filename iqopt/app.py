import os
from flask import Flask
from flask import request
from flask import jsonify
from cerberus import Validator
from flask_sqlalchemy import SQLAlchemy
import requests


v_api = Validator(
    {
        "text": {
            "type": "string",
            "required": True,
            "maxlength": 400,
            "minlength": 2
        },
        "lang": {
            "type": "string",
            "required": True,
            "regex": r"^(\w{2}-\w{2})|(\w{2})$"
        },
        "format": {
            "type": "string",
            "allowed": ["plain", "html"]
        }
    }
)

YT_API_KEY = "API_KEY"
YT_API_URL = "https://translate.yandex.net/api/v1.5/tr.json"


if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgresql://"\
        "translt:test@127.0.0.1/translate_api"
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

db = SQLAlchemy()


def create_app(DB_URI=SQLALCHEMY_DATABASE_URI, debug=False):
    app = Flask(__name__, )
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.debug = debug
    db.init_app(app)

    @app.route("/translate", methods=["POST"])
    def translate():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No data"}), 404
        valid = v_api.validate(data)
        if not valid:
            return jsonify({"error": v_api.errors}), 500

        stat = Stats.query.filter_by(
            lang=data["lang"], text=data["text"]).all()

        if not stat:
            stat = Stats(data["lang"], data["text"])
        elif len(stat) == 1:
            stat = stat[0]
            stat.requests += 1

        params = {
            "text": stat.text,
            "lang": stat.lang,
            "format": data.get("format", "plain"),
            "key": YT_API_KEY
        }
        r = requests.post(YT_API_URL + "/translate", data=params)
        if r.status_code == 200:
            out = r.json()
            stat.translated = out.get("text", "")[0]
            db.session.add(stat)
            db.session.commit()
            return jsonify(
                {"translated": out["text"], "lang": out["lang"]}
            )

    @app.route("/translate/stats", methods=["POST"])
    def get_stats():
        params = request.get_json(silent=True)
        if params:
            q = Stats.query
            if "lang" in params:
                lang = params["lang"]
                q = q.filter_by(lang=lang)
            if "text" in params:
                text = params["text"]
                q = q.filter_by(text=text)
            stats = [x.dict() for x in q]
            return jsonify(stats)
        return jsonify({"error": "provide either lang or text"})

    return app


class Stats(db.Model):
    __tablename__ = "stats"
    lang = db.Column(db.String(5), nullable=False)
    text = db.Column(db.String(400), nullable=False)
    translated = db.Column(db.String)
    requests = db.Column(db.Integer)
    __table_args__ = (db.PrimaryKeyConstraint('text', 'lang', name='stat_pk'),)

    def __init__(self, lang, text, translated="", requests=1):
        self.lang = lang
        self.text = text
        self.translated = translated
        self.requests = requests

    def __repr__(self):
        return u"<Stats(%r, %r)>" % (self.lang, self.text)

    def dict(self):
        return {
            k: getattr(self, k)
            for k in ["lang", "text", "requests", "translated"]
        }


if __name__ == '__main__':
    app = create_app(debug=True)
    db.create_all()
    app.run()
