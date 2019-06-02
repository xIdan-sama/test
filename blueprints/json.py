from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from functools import wraps

import blueprints.base as base


def json_wraper(func):
    """ Обертка приведения результата в json стркутуру """

    @wraps(func)
    def wrap(*args, **kwargs):
        response = []
        result = func(*args, **kwargs)

        for elem in result:
            response.append(str(elem))

        return jsonify(response)
    return wrap


bp_json = Blueprint("json", __name__)


@bp_json.route("/", methods=["GET"])
@json_wraper
def index():
    return base.index()


@bp_json.route("/<ticker>", methods=["GET"])
@json_wraper
def ticker_get(ticker):
    return base.ticker_get(ticker)


@bp_json.route("/<ticker>/insider", methods=["GET"])
@json_wraper
def insider_get(ticker):
    return base.insider_get(ticker)


@bp_json.route("/<ticker>/insider/<name>", methods=["GET"])
@json_wraper
def insider_item(ticker, name):
    return base.insider_item(ticker, name)


@bp_json.route("/<ticker>/analytics", methods=["GET"])
@use_args({
    "date_from": fields.Date(required=True),
    "date_to": fields.Date(required=True)
})
@json_wraper
def analytics(args, ticker):
    return base.analytics(args, ticker)


@bp_json.route("/<ticker>/delta", methods=["GET"])
@use_args({
    "value": fields.Decimal(required=True),
    "type": fields.Str(required=True)
})
@json_wraper
def delta(args, ticker):
    return base.delta(args, ticker)
