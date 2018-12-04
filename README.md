# Install Dependencies

```
pip install -r requirements.txt
```

# Run Developement Server

Place all case html files in `case/`. The form action should be
`<form action="/submit">`. Then run

```
FLASK_APP=serve.py FLASK_DEBUG=1 flask run
```

All submitted form data is saved in `submissions/`
