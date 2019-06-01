from webargs import fields
from webargs.flaskparser import use_args
from flask import Blueprint, render_template

import blueprints.base as base


bp_html = Blueprint("html", __name__)


@bp_html.route("/", methods=["GET"])
def index():
    return render_template('index.tpl', data=base.index())


@bp_html.route("/<ticker>", methods=["GET"])
def ticker_get(ticker):
    return render_template('ticker.tpl', data=base.ticker_get(ticker), title=ticker)


@bp_html.route("/<ticker>/insider", methods=["GET"])
def insider_get(ticker):
    return render_template('insiders.tpl', data=base.ticker_get(ticker), title=ticker)


@bp_html.route("/<ticker>/insider/<name>", methods=["GET"])
def insider_item(ticker, name):
    return render_template('insiders.tpl', data=base.insider_item(ticker, name), title=ticker)


@bp_html.route("/<ticker>/analytics", methods=["GET"])
@use_args({
    "date_from": fields.Date(required=True),
    "date_to": fields.Date(required=True)
})
def analytics(args, ticker):
    return render_template('analytics.tpl', data=base.analytics(args, ticker), title=ticker, kwargs=args)


@bp_html.route("/<ticker>/delta", methods=["GET"])
@use_args({
    "value": fields.Decimal(required=True),
    "type": fields.Str(required=True)
})
def delta(args, ticker):
    return render_template('delta.tpl', data=base.delta(args, ticker)[0], title=ticker, kwargs=args)
