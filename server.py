import os

import flask
import pydantic
from flask import jsonify, request
from flask.views import MethodView

from models import Session, Advertisement
from sqlalchemy.exc import IntegrityError

app = flask.Flask('app')


class HttpError(Exception):

    def __init__(self, status_code: int, error_massage: dict | str | list):
        self.status_code = status_code
        self.error_massage = error_massage


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"error": er.error_massage})
    response.status_code = er.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: flask.Response):
    request.session.close()
    return http_response


def get_ad_by_id(ad_id):
    ad = request.session.get(Advertisement, ad_id)
    if ad is None:
        raise HttpError(404, "post not found")
    return ad


def add_ad(ad):
    request.session.add(ad)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "post already exists")
    return ad


def delete_ad_by_id(ad_id):
    ad: Advertisement = get_ad_by_id(ad_id)
    request.session.delete(ad)
    request.session.commit()


class UserView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)


    def post(self):
        json_data = request.json
        ad = Advertisement(**json_data)
        add_ad(ad)
        return jsonify(ad.dict)


    def delete(self, ad_id):
        delete_ad_by_id(ad_id)
        return jsonify({'message': 'post deleted'})

ad_view = UserView.as_view('posts')

app.add_url_rule("/posts/", view_func=ad_view, methods=['POST'])

app.add_url_rule("/posts/<int:ad_id>/", view_func=ad_view, methods=['GET', 'DELETE'])

app.run()