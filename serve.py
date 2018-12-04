from datetime import datetime
from pathlib import Path
import pandas as pd
from flask import Flask, request, render_template
app = Flask(__name__, static_folder='case')

@app.route('/')
def list_cases():
    case_dir = Path('./case')
    print(list(case_dir.iterdir()))
    return render_template('index.html', cases=list(case_dir.iterdir()))


@app.route('/submit', methods=['POST'])
def save_form():
    form = pd.DataFrame(columns=list(request.form.keys()))
    form.loc[0] = list(request.form.values())
    filename = f'submissions/{datetime.utcnow():%Y-%m-%dT%H-%M-%SZ}.csv'
    form.to_csv(filename, index=False)
    return "Submission successful!"
