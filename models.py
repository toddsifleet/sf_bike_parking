from flask import g
import psycopg2
import psycopg2.extras

def get_db():
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_db()
    return g.postgres_db.cursor(cursor_factory=psycopg2.extras.DictCursor)

def close_db():
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()

def connect_db():
    return  psycopg2.connect("dbname=sf_bike_racks")

class ParkingSpot(dict):
    @classmethod
    def in_bounds(cls, bounds):
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

        return map(cls, db.fetchall())

    @classmethod
    def find(cls, spot_id):
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
        result = db.fetchone()
        if result:
            return cls(result)

