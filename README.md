# Custom Python Services for NetsBlox
This contains a Python server for hosting your own NetsBlox services which can also be used from https://editor.netsblox.org.

There are some types of services that would be great to do in NetsBlox - such as training your own word embeddings - but would be too computationally intensive for the browser and infeasible as a free, public deployment. This project enables you to create your own services which can be used by you (and perhaps your class or summer camp) without requiring your own deployment of NetsBlox!

## Quick Start
First, install the python dependencies with pip:
```
pip install -r requirements.txt
```
Next, start the server using flask:
```
export FLASK_APP=netsblox-services/server.py
python -m flask run --port 5050
```

*Note*: If you are using Windows, the `FLASK_APP` environment variable will need to be set using `set`.
