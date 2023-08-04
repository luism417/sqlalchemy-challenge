# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement =Base.classes.measurement
Station=Base.classes.station

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
def home():return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
  # Query for the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Query for stations
    results = session.query(Station.station).all()

    # Convert the query results to a list
    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query for the last 12 months of temperature observation data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a dictionary
    tobs_data = {date: tobs for date, tobs in results}

    return jsonify(tobs_data)
@app.route("/api/v1.0/<start>")
def start(start):
    # Query for TMIN, TAVG, TMAX for all dates greater than or equal to start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert the query results to a list
    temp_stats = list(np.ravel(results))

    return jsonify(temp_stats)
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Query for TMIN, TAVG, TMAX for dates between start and end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert the query results to a list
    temp_stats = list(np.ravel(results))

    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)
    