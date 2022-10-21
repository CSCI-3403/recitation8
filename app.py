import logging
from typing import Tuple, Union

import click
from flask import Flask, abort, render_template, request
from werkzeug.wrappers import Response

View = Union[Response, str, Tuple[str, int]]

app = Flask(__name__)

@app.route('/')
def index() -> View:
    return render_template('index.html')

@app.route('/purchase', methods=['POST'])
def purchase() -> View:
    try:
        cost = int(request.form["cost"])
        shipping = int(request.form["shipping"])
        quantity = int(request.form["quantity"])
    except ValueError:
        return abort(Response("Invalid request: cost, shipping, and quantity must all be integers", 400))

    return render_template(
        'purchase.html',
        cost=cost,
        shipping=shipping,
        quantity=quantity,
    )

@click.command()
@click.option('--debug', is_flag=True)
@click.option('--port', default=80)
def main(debug: bool, port: int) -> None:
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    app.run('0.0.0.0', debug=debug, port=port)

if __name__ == '__main__':
    main()