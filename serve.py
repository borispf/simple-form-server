from datetime import datetime
from pathlib import Path
import pandas as pd
from flask import Flask, request, render_template, abort
from flask_basicauth import BasicAuth


app = Flask(__name__, static_folder='case')

app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = 'rank'
app.config['BASIC_AUTH_PASSWORD'] = 'weshouldprobablychangethis'
basic_auth = BasicAuth(app)


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
    return render_template('index.html', folders=folders, cases=cases)


@app.route('/submit', methods=['POST'])
def save_form():
    form = pd.DataFrame(columns=list(request.form.keys()))
    form.loc[0] = list(request.form.values())
    filename = f'submissions/{datetime.utcnow():%Y-%m-%dT%H-%M-%SZ}.csv'
    form.to_csv(filename, index=False)
    return "Submission successful!"
