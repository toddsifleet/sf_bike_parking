from flask import Flask,request, g, jsonify, abort
from models import ParkingSpot, close_db

app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
))


@app.teardown_appcontext
def clean_up(error):
    close_db()

def parse_bounds(bounds):
    try:
        bounds = map(float, bounds.split(','))
        if not len(bounds) == 4:
            abort(400)
    except ValueError:
        abort(400)
    return bounds

@app.route('/spots/bounds')
def spots_in_bounds():
    bounds = parse_bounds(request.args['bounds'])
    parking_spots = ParkingSpot.in_bounds(bounds)
    return jsonify(result = parking_spots)

def parse_id(spot_id):
    try:
        return int(spot_id)
    except ValueError:
        abort(400)

@app.route('/spots/<spot_id>')
def spot_info(spot_id):
    spot_id = parse_id(spot_id)
    parking_spot = ParkingSpot.find(spot_id)
    if parking_spot is None:
        abort(404)
    return jsonify(parking_spot)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
