import logging
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd
from flask import Flask, request, render_template, abort
from flask_basicauth import BasicAuth


app = Flask(__name__, static_folder='case')

app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = 'rank'
app.config['BASIC_AUTH_PASSWORD'] = 'weshouldprobablychangethis'
basic_auth = BasicAuth(app)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url if request else "-"
        record.remote_addr = request.remote_addr if request else "-"
        record.referrer = request.referrer if request else "-"
        record.user_agent = request.user_agent if request else "-"
        return super().format(record)


handler = RotatingFileHandler("log/serve.log", maxBytes=10_000_000, backupCount=100)
handler.setLevel(logging.DEBUG)
log_fmt = '[{asctime}] {levelname:8} [{name}] [{remote_addr}; {url}; {referrer}; {user_agent}]: {message}'
formatter = RequestFormatter(log_fmt, style="{")
logging.Formatter.converter = time.gmtime
handler.setFormatter(formatter)

root = logging.getLogger("werkzeug")
root.addHandler(handler)
app.logger.addHandler(handler)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def list_cases(path):
    print(path)
    case_dir = Path('./case')
    dir_ = case_dir / path
    if not dir_.exists():
        abort(404)
    cases = sorted(f for f in dir_.iterdir() if f.is_file())
    folders = sorted(f.relative_to(case_dir) for f in dir_.iterdir() if f.is_dir())
    app.logger.info("folder loaded")
    return render_template('index.html', folders=folders, cases=cases)


@app.route('/submit', methods=['POST'])
def save_form():
    form = pd.DataFrame(columns=list(request.form.keys()))
    form.loc[0] = list(request.form.values())
    filename = f'submissions/{datetime.utcnow():%Y-%m-%dT%H-%M-%SZ}.csv'
    form.to_csv(filename, index=False)
    app.logger.info("form submitted")
    return "Submission successful!"
