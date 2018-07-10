from ..app import app
from .models import Measurement, Station


@app.route('precipitation')
def precipitation():
    r = Measurement.query.filter(Measurement.date >= '2017-07-08').first()
    return r


@app.route('stations')
def stations():
    return 'Hello World!'


@app.route('tabs')
def tobs():
    return 'Hello World!'


@app.route('<start>')
@app.route('<start>/<end>')
def start_end(start, end):
    return 'Hello World!'