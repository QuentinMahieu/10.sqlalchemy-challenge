from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
#import the function defined in a jupyter nb
from dateconverters import converter,converter2
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    session = Session(engine)
    #calcul min and max date
    min_date = session.query(
        func.min(Measurement.date)).first()[0]
    max_date = session.query(
        func.max(Measurement.date)).first()[0]
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation/date<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start_date<br>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br/>"
        f"Available Dates:<br>"
        f"choose dates between {min_date} and {max_date}"
    )

@app.route("/api/v1.0/precipitation/<date>")
def precipitation(date):
    #create the session
    session = Session(engine)
    #calcul the precipitation for a give date
    datadates = [dates[0] for dates in session.query(Measurement.date).all()]
    if date not in datadates:
        return jsonify({"error": f"{date} not found."}), 404
    #convert the input date
    date = converter(date)
    result = session.query(Measurement.prcp).\
            filter(func.strftime('%Y-%m-%d',Measurement.date) == date).first()
    
    session.close()

    return jsonify(result)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.name, Measurement.station).\
        filter(Station.station == Measurement.station).\
        group_by(Station.name).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #search for the date that represent the last 12 months
    from datetime import datetime as dtt
    query_date = dt.datetime.strptime(session.query(func.max(Measurement.date)).\
                first()[0], '%Y-%m-%d') - dt.timedelta(days=365)
    date = dtt.strftime(query_date,'%Y-%m-%d')
    #search for most active station for the last 12 months
    query_station = session.query(Measurement.station,func.count(Measurement.tobs)).\
        filter(Measurement.date >= date).group_by('station').\
            order_by(func.count(Measurement.tobs).desc()).first()[0]
    results = session.query(Measurement.date,Measurement.tobs).\
        filter_by(station = query_station).\
            filter(Measurement.date >= date).\
                order_by('date').all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start_date>")
def averages_start(start_date):
    session = Session(engine)
    #convert the date
    date = converter(start_date)
    datadates = [dates[0] for dates in session.query(Measurement.date).all()]
    if date not in datadates:
        return jsonify({"error": f"{date} not found."}), 404
    #results of the query
    results = session.query(func.min(Measurement.tobs),func.avg(
            Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >= date).all()

    return jsonify(
        f"TMIN: {results[0][0]}",
        f"TAVG: {results[0][1]}",
        f"TMAX: {results[0][2]}"
    )

@app.route("/api/v1.0/<start_date>/<end_date>")
def averages_duration(start_date,end_date):
    session = Session(engine)
    #convert the date
    startdate = converter(start_date)
    enddate = converter(end_date)
    datadates = [dates[0] for dates in session.query(Measurement.date).all()]
    if (startdate not in datadates) | (enddate not in datadates):
        return jsonify({"error": f"Dates not in range."}), 404
    if startdate >= enddate :
        return jsonify({"error": f"{startdate} later than {enddate}"})
    #results of the query
    results = session.query(func.min(Measurement.tobs),func.avg(
            Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >= startdate).\
            filter(Measurement.date <= enddate).all()

    return jsonify(
        f"TMIN: {results[0][0]}",
        f"TAVG: {results[0][1]}",
        f"TMAX: {results[0][2]}"
    )

if __name__ == '__main__':
    app.run(debug=True)