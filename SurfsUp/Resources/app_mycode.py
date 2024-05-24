# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    session.close()  # Close the session after use
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Station = Base.classes.station
    session = Session(engine)
    
    stations_data = session.query(Station.station, Station.name).all()
    stations_dict = {station: name for station, name in stations_data}
    
    session.close()  # Close the session after use
    return jsonify(stations_dict)

# Define other routes similarly for tobs, start, and start_end

if __name__ == '__main__':
    app.run(debug=True)