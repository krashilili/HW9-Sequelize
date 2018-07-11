from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
import datetime, numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///hawaii.sqlite', connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route('/api/v1.0/precipitation')
def precipitation():
    last_date_on_db = session.query(*[measurement.date]).order_by(measurement.date.desc()).first()[0]
    one_year_ago = datetime.datetime.strptime(last_date_on_db, '%Y-%m-%d') - datetime.timedelta(365)
    one_year_ago_str = datetime.datetime.strftime(one_year_ago, '%Y-%m-%d')
    # query the temperature in the past year
    result = session.query(*[measurement.date, measurement.tobs]).filter(measurement.date >= one_year_ago_str).all()
    r_list_of_dict = [{r[0]: r[1]} for r in result]
    jsonify_result = jsonify(r_list_of_dict)
    return jsonify_result


@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(station.station).all()
    list_of_stations = [s[0] for s in stations]
    jsonify_stations = jsonify(list_of_stations)
    return jsonify_stations


@app.route('/api/v1.0/tobs')
def tobs():
    last_date_on_db = session.query(*[measurement.date]).order_by(measurement.date.desc()).first()[0]
    one_year_ago = datetime.datetime.strptime(last_date_on_db, '%Y-%m-%d') - datetime.timedelta(365)
    one_year_ago_str = datetime.datetime.strftime(one_year_ago, '%Y-%m-%d')
    # query the tobs in the past year
    tobs = session.query(measurement.tobs).filter(measurement.date >= one_year_ago_str).all()
    list_of_tobs = [t[0] for t in tobs]
    jsonify_tobs = jsonify(list_of_tobs)
    return jsonify_tobs


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def temp_in_range(start, end):
    if start and not end:

    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)