from flask import Flask,request, g, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
))

def get_db():
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_db()
    return g.postgres_db.cursor(cursor_factory=psycopg2.extras.DictCursor)

def connect_db():
    return  psycopg2.connect("dbname=sf_bike_racks")

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()

def get_spots_in_bounds(bounds):
    db = get_db()
    db.execute('''
        SELECT
            id,
            latitude::TEXT,
            longitude::TEXT
        FROM
            parking_spots
        WHERE
            status = 'COMPLETE'
            and spaces > 0
            and latitude > %s
            and longitude > %s
            and latitude < %s
            and longitude <%s
    ''', bounds)

    return map(dict, db.fetchall())

def get_spot_info(spot_id):
    db = get_db()
    db.execute('''
        SELECT
            id,
            address,
            COALESCE(location, address) AS location,
            placement,
            racks,
            status,
            spaces,
            latitude::TEXT,
            longitude::TEXT
        FROM
            parking_spots
        WHERE
            id = %s
    ''', (spot_id,))
    return dict(db.fetchone())

@app.route('/spots/bounds')
def spots_in_bounds():
    bounds = request.args['bounds'].split(',')
    bounds = map(float, bounds)
    return jsonify(result = get_spots_in_bounds(bounds))

@app.route('/spots/<spot_id>')
def spot_info(spot_id):
    return jsonify(get_spot_info(spot_id))

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
