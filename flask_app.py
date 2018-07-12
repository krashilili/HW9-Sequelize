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

def valid_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


@app.route('/')
def welcome():
    manual = ['/api/v1.0/precipitation',
              '/api/v1.0/stations',
              '/api/v1.0/tobs',
              '/api/v1.0/<start>',
              '/api/v1.0/<start>/<end>']
    return jsonify(manual)
    
    
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


@app.route('/api/v1.0/<start>',defaults={'end': None})
@app.route('/api/v1.0/<start>/<end>')
def temp_in_range(start, end):
    last_date_on_db = session.query(*[measurement.date]).order_by(measurement.date.desc()).first()[0]
    first_date_on_db = session.query(*[measurement.date]).order_by(measurement.date.asc()).first()[0]

    tobs = None
    # check if the start and end dates are in valid format
    if valid_date(start) and valid_date(end) and start > end:
        return "Error. Start date is greater than end date."

    # Start date shall be less than or equal to the last date in sqlite db.
    if valid_date(start) and start > last_date_on_db:
        return "Error. Start date exceeds the last date on sqlite db."

    # End date shall be greater than or equal to the first date in sqlite db.
    if valid_date(end) and end < first_date_on_db:
        return "Error. End date is before the first date on sqlite db."

    if valid_date(start) and not end:
        # Given a start_date only
        tobs = session.query(measurement.date,
                             func.min(measurement.tobs),
                             func.avg(measurement.tobs),
                             func.max(measurement.tobs)).filter(measurement.date >= start)\
                                                        .group_by(measurement.date).all()

    elif valid_date(start) and valid_date(end):
        tobs = session.query(measurement.date,
                             func.min(measurement.tobs),
                             func.avg(measurement.tobs),
                             func.max(measurement.tobs)).filter(measurement.date >= start).\
                                                         filter(measurement.date <= end).\
                                                         group_by(measurement.date).all()
    else:
        return "The date is not valid. Please use the right format: YYYY-MM-DD."

    results = [{'date': r[0],
                'TMin': r[1],
                'TAvg': r[2],
                'TMax': r[3]} for r in tobs]

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)