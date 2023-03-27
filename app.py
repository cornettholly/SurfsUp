import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import pandas as pd


################################################
# Database Setup
################################################
engine = create=engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

################################################
# Flask Setup
################################################
app = Flask(__name__)


################################################
# Flask Routes
################################################

@app.route("/")
def welcome():
    """List all available app routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation,br/."
        f"/api/v1.0/station"
        f"/api/v1.0/tobs"
        
    )


@app.route("/api/v1.0/precipitation")
def get_precipiation():
    # Create our session (link) from Python to the DB
    Session = Session(engine)
    
    
    Year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
   # Perform a query to retrieve the date and precipitation scores

    precip_results=Session.query(measurement.date, measurement.prcp).filter(measurement.date>= Year_ago).all()
   # Save the query results as a Pandas DataFrame and set the index to the date column
    precip_df=pd.DataFrame(precip_results, columns=['date', 'precipitation']).set_index('date')
    
   # Create dict for percipitation
    precip_df=precip_df.sort_index()
    
    return precip_df.to_dict()['percipitation']


@app.route("/api/v1.0/station")
def get_stations():
    # Create our session (link) from Python to the DB
    Session = Session(engine)
    
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query station list
    results = results =session.query(station).all()
    results = [r.name for r in results]
    session.close()
    return {"stations": list(results)}

@app.route("/api/v1.0/tobs")
def get_tobs():
    # Create our session (link) from Python to the DB
    Session = Session(engine)
    
    Year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    
    # Query station list and create dataframe
    most_active_station = Session.query(measurement.station,func.count(measurement.station)).\
        group_by(measurement.station).order)by(func.count(measurment.station).desc()).all()
    
    most_active_results=Session.query(measurment.date,measurement.tobs).filter(measurement.date>= year_ago).filter(measurement.station == most_active_station).all()
    
    most_active_df = pd.DataFrame(most_active_results,columns=['date','tobs']).set_index('date')
    
    # create dict for tobs
    most_active_df=most_active_df.sort_index()
    
    return most active_df.to_dict()['tobs']






if __name__=='__main__':
    app.run(debug=True)