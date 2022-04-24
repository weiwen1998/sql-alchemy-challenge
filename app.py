import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


Station = Base.classes.station
Measurement = Base.classes.measurement


app = Flask(__name__)


@app.route("/")
def introduction():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results1= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    
    for date, prcp in results1:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    sel = [Measurement.station, func.count(Measurement.id)]

    per_station_total = session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    per_station_total

    session.close()

    all_stations = list(np.ravel(per_station_total))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    sel5 = [Measurement.station, func.max(Measurement.date), Measurement.tobs]
    latest_date = session.query(*sel5).filter(Measurement.station=="USC00519281").all()

    last_12_months = dt.date(2017, 8 ,18) - dt.timedelta(days=365)
    last_12_months

    results2 = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station=="USC00519281").filter(Measurement.date >= last_12_months).all()

    session.close()

    highest_station_tobs = list(np.ravel(results2))

    return jsonify(highest_station_tobs)

@app.route("/api/v1.0/<start>/")
def start(start=None):
    
    session = Session(engine)

    start = dt.datetime.strptime(start, "%Y-%m-%d")
    sel2 = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    min_max_avg_1 = session.query(*sel2).filter(Measurement.date >= start).all()

    session.close()

    return jsonify(min_max_avg_1)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
   
    session = Session(engine)

    start2 = dt.datetime.strptime(start, "%Y-%m-%d")
    end2 = dt.datetime.strptime(end, "%Y-%m-%d")                                                                       
    sel3 = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    min_max_avg_2 = session.query(*sel3).filter(Measurement.date >= start2, Measurement.date <= end2).all()
    
    session.close()
    
    return jsonify(min_max_avg_2)