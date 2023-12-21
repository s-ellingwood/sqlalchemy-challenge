# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
# Start at the homepage. List all available routes.
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"api/v1.0/<start>"
        f"api/v1.0/<start>/<end>"
    )


# /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert query results from percipitation analysis to a dictionary using 'date' as the key and 'prcp' as the value
    precipquery = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").order_by(Measurement.date).all()
    
    results = []
    for date, prcp in precipquery:
        precip = {date : prcp}
        results.append(precip)

    # Return the JSON representation of your dictionary.
    return jsonify(results)


# /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    statquery = session.query(Station.station).all()

    stations = list(np.ravel(statquery))

    return jsonify(stations)


# /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def temperatures():
    # Query the date and temperature observations of the most-active station for the previous year of data.
    tempquery = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016-08-23").all()

    # Return a JSON list of temperature observations for the previous year.
    temperatures = []
    for date, prcp in tempquery:
        temp = {date : prcp}
        temperatures.append(temp)

    return jsonify(temperatures)


# /api/v1.0/<start> and /api/v1.0/<start>/<end> routes
@app.route("/api/v1.0/<start>")
    # Return a JSON list of the minimum, average, and maximum temperature for a specified start or start-end range.
def temp_start(start_date):
    # For a specified start, calculate "TMIN", "TAVG", and "TMAX" for all the dates greater than or equal to the start date.
    start_temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= "start_date").all()
    
    start_list = []
    for minimum, maximum, average in start_temps:
        temp_dict = {}
        temp_dict["Minimum"] = minimum
        temp_dict["Maximum"] = maximum
        temp_dict["Average"] = average
        start_list.append(temp_dict)
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start_date, end_date):
    # For a specified start and end date, calculate "TMIN", "TAVG", and "TMAX" for dates from start date to end date, inclusive.
    start_end_temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= "start_date").\
        filter(Measurement.date <= "end_date").all()
    
    start_end_list = []
    for minimum, maximum, average in start_end_temps:
        temp_dict = {}
        temp_dict["Minimum"] = minimum
        temp_dict["Maximum"] = maximum
        temp_dict["Average"] = average
        start_end_list.append(temp_dict)
    return jsonify(start_end_list)



if __name__ == '__main__':
    app.run(debug=True)

# Close session
session.close()