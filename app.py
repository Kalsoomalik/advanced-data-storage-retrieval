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


# `/api/v1.0/precipitation`
#  Query for the dates and temperature observations from the last year.
#  Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
#  Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def names():

    results = session.query(Measurement.date, Measurement.tobs).all()
  
    all_observations = []
    for observation in results:
        observation_dict = {}
        observation_dict[observation.date] = observation.tobs
        all_observations.append(observation_dict)

    return jsonify(all_observations)



# `/api/v1.0/stations`
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Measurement.station).all()
    
    station_names = list(np.ravel(results))
    return jsonify(station_names)



# `/api/v1.0/tobs`
# Return a JSON list of Temperature Observations (tobs) for the previous year

@app.route("/api/v1.0/tobs/")
def tobs():
    
    # Query list of temperatures observed last year
    results = session.query(Measurement.tobs).\
    filter(Measurement.date <= '2018-01-01').\
    filter(Measurement.date >= '2017-01-01').all()
    #Create list of tobs for previous year
    temp_obs = list(np.ravel(results))
    return jsonify(temp_obs)


# `/api/v1.0/<start>`
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start>")
def tobs_start(start):
    start_date = "'" + start + "'"
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    temp_start = list(np.ravel(results))
    return jsonify(temp_start)


# `/api/v1.0/<start>/<end>`
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

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
