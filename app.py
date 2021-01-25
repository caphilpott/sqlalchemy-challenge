# 1. import Flask and other needed modules
from flask import Flask, jsonify

import numpy as np
import pandas as pd

import datetime as dt
import time
from datetime import datetime
import ast
from datetime import date
from datetime import timedelta


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
# Relative path is always better than an absolute path
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
# Declare a Base using `automap_base()` - CP Add
Base = automap_base()

# reflect the tables
# Use the Base class to reflect the database tables - CP Add
Base.prepare(engine, reflect=True)

# Save references to each table
# Assign the measurement and station class to variables called 'measurement' and 'station' - CP Add
measurement = Base.classes.measurement
station = Base.classes.station

# Save references to each table
# Assign the measurement and station class to variables called 'measurement' and 'station' - CP Add
measurement = Base.classes.measurement
station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (
        f"<strong>Welcome to My Hawaii Climate API App!</strong><br/>"
        f"<br/>"
        f"<strong>Available Links (All output is JSON formatted):</strong><br/>"
        f"<ul>"
        f"<li><a href='http://localhost:5000/about' target='_blank'>About</a></li>"
        f"<li><a href='http://localhost:5000/api/v1.0/precipitation' target='_blank'>Precipitation</a></li>"
        f"<li><a href='http://localhost:5000/api/v1.0/stations' target='_blank'>Stations</a></li>"
        f"<li><a href='http://localhost:5000/api/v1.0/tobs' target='_blank'>Temperature Observations</a></li>"
        f"<li><a href='http://localhost:5000/api/v1.0/<start>' target='_blank'>Temperatures from an inputted /START date</a></li>"
        f"<li><a href='http://localhost:5000/api/v1.0/<start>/<end>' target='_blank'>Temperatures from inputted /START / END dates</a></li>"
        f"</ul>"
        f"<br/>"
        f"<strong>The START and START/END links page will be blank at first:</strong>.<br/>"
        f"<BLOCKQUOTE>For /START, input the start date (format = YYYY-MM-DD) in place of the bracketed 'start' and hit Enter.<br/>"
        f"For /START/END, input the start date and end date (format = YYYY-MM-DD) in place of the bracketed 'start/end' and hit Enter.<br/>"
        f"The available date range for input is from 2010-01-01 to 2017-08-23.<br/>"
        f"<br/>"        
        f"Example Start link: 'http://localhost:5000/api/v1.0/2017-08-15'.<br/>"
        f"Example Start/End link: link 'http://localhost:5000/api/v1.0/2017-08-15/2017-08-23'.</BLOCKQUOTE>"
        f"<img style='height:400px;width:600px;'src='https://img1.10bestmedia.com/Images/Photos/374469/GettyImages-1038532990_54_990x660.jpg'/>"        
    )

# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return( 
        f"<strong>Welcome to my 'About' page!</strong><br/>"
        f"<br/>"
        f"<strong>Link Descriptions (All output is JSON formatted):</strong><br/>"
        f"<ol>"        
        f"<li><strong>Precipitation</strong>: Lists by date, precipitation at all stations in Hawaii</li>"
        f"<li><strong>Stations</strong>: Lists all weather stations in Hawaii and their count or readings</li>"
        f"<li><strong>Tobs</strong>: Lists all temperature readings at the busiestweather stations in Hawaii over the last year</li>"
        f"<li><strong>start</strong>: Lists all temperature readings by date from the inputted start date (input format: YYYY-MM-DD)</li>"
        f"<li><strong>start/end:</strong> Lists all temperature readings by date between the inputted start and end dates (input format: YYYY-MM-DD)</li>"
        f"</ol>"                
        f"<br/>"
        f"<img style='height:425px;width:600px;'src='https://www.gannett-cdn.com/presto/2020/01/15/USAT/610d28ed-f048-4808-bbef-589bc5ef6cc6-Hawaii.jpg'/>"
         )
    

@app.route("/api/v1.0/precipitation")
def rain():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    #Define Start date for the 12 months of data as being the most recent date - 365 days 
    #Result is a tuple. To get just the date, use index [0]
    mst_recent_dt= session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    dt_obj = datetime.strptime(mst_recent_dt, "%Y-%m-%d") 
    start_dte = dt_obj - timedelta(days=365)


    """Return a list of rainfall by date for the last year of available data"""
    # Query precipitation
    results = session.query(measurement.date,measurement.prcp).\
                             filter(measurement.date > start_dte).\
                             order_by(measurement.date).all()

    session.close()

    #Create a dictionary from the row data and append to a list of all_precip
    all_precip = []
    for date, prcp in results:
        precip_dict = {} # this line unpacks the tuple
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    
    """Return a list of rainfall by date for the last year of available data"""
    # Query stations
    station_count_readings = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
            order_by(func.count(measurement.station).desc()).all()
    
    session.close()

    #List the stations

    return jsonify(station_count_readings)

@app.route("/api/v1.0/tobs")
def temp():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    #Define Start date for the 12 months of data as being the most recent date - 365 days 
    #Result is a tuple. To get just the date, use index [0]
    mst_recent_dt= session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    dt_obj = datetime.strptime(mst_recent_dt, "%Y-%m-%d") 
    start_dte = dt_obj - timedelta(days=365)


    """Return a list of temperatures at the most active station by date for the last year of available data"""
    # Query tobs
    results = session.query(measurement.date,measurement.tobs).\
                             filter(measurement.date > start_dte,measurement.station == 'USC00519281').\
                             order_by(measurement.date).all()

    session.close()

    #Create a dictionary from the row data and append to a list of all_temps
    all_temps = []
    for date, tobs in results:
        tobs_dict = {} # this line unpacks the tuple
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_temps.append(tobs_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def temp_from_date(start):
    # Create a session (link) from Python to the DB
    session = Session(engine)

    start_date=start

    """Return a list of low, average, and high temperatures since a provided date"""
    # Query temperature ranges
    results = session.query(measurement.date, func.min(measurement.tobs),\
                                            func.avg(measurement.tobs),\
                                            func.max(measurement.tobs),).\
                                            group_by(measurement.date).\
                                            filter(measurement.date >= start_date).all()

    session.close()

    #Create a dictionary from the row data and append to a list of all_precip
    all_temps = []
    for date, low, avg, high in results:
        temps_dict = {} # this line unpacks the tuple
        temps_dict["date"] = date
        temps_dict["low"] = low
        temps_dict["avg"] = avg
        temps_dict["high"] = high                
        all_temps.append(temps_dict)

    return jsonify(all_temps)


@app.route("/api/v1.0/<start>/<end>")
def temp_in_date_range(start,end):
    # Create a session (link) from Python to the DB
    session = Session(engine)

    start_date=start
    end_date=end

    """Return a list of low, average, and high temperatures within a provided date range"""
    # Query temperature ranges
    results = session.query(measurement.date, func.min(measurement.tobs),\
                                            func.avg(measurement.tobs),\
                                            func.max(measurement.tobs),).\
                                            group_by(measurement.date).\
                                            filter(measurement.date >= start_date,measurement.date <= end_date).all()

    session.close()

    #Create a dictionary from the row data and append to a list of all_precip
    all_temps1 = []
    for date, low, avg, high in results:
        temps_dict = {} # this line unpacks the tuple
        temps_dict["date"] = date
        temps_dict["low"] = low
        temps_dict["avg"] = avg
        temps_dict["high"] = high                
        all_temps1.append(temps_dict)

    return jsonify(all_temps1)


if __name__ == "__main__":
    app.run(debug=True)
