import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Passenger = Base.classes.passenger

Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"<h4>/api/v1.0/precipitation</h4>"
        f"<h4>/api/v1.0/stations/h4>"
        f"<h4>/api/v1.0/tobs/h4>"
        f"<h4>/api/v1.0/start and /api/v1.0/start/end/h4>"
    )


@app.route("/api/v1.0/precipitation")
def names():

    # Query termperature observations from last year
    results = session.query(Measurement.date, Measurement.tobs).all()

    # Create a dictionary from the row data
    all_observations = []
    for observation in results:
        observation_dict = {}
        observation_dict[observation.date] = observation.tobs
        all_observations.append(observation_dict)

    return jsonify(all_observations)

@app.route("/api/v1.0/stations")
def stations():
    
    #Query list of stations from data
    results = session.query(Measurement.station).all()
    
    # Create a dictionary in JSON
    station_names = list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs/")
def tobs():
    
    # Query list of temperatures observed last year
    results = session.query(Measurement.tobs).\
    filter(Measurement.date <= '2018-01-01').\
    filter(Measurement.date >= '2017-01-01').all()
    #Create list of tobs for previous year
    temp_obs = list(np.ravel(results))
    return jsonify(temp_obs)


@app.route("/api/v1.0/<start>")
def tobs_start(start):
    start_date = "'" + start + "'"
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    temp_start = list(np.ravel(results))
    return jsonify(temp_start)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start, end):
    start_date = "'" + start + "'"
    end_date = "'" + end + "'"
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).filter(Measurement.date >= start_date ,
                                                               Measurement.date <= end_date).all()
    temp_start_end = list(np.ravel(results))
    return jsonify(temp_start_end)

if __name__ == '__main__':
    app.run(debug=True)
