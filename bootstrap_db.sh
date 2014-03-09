dropdb sf_bike_racks

createdb sf_bike_racks -E UNICODE

psql sf_bike_racks << EOF
  CREATE EXTENSION postgis;
  CREATE EXTENSION fuzzystrmatch;

  CREATE TABLE parking_spots ( 
    id SERIAL PRIMARY KEY,
    address VARCHAR(128),
    location VARCHAR(128),
    latitude NUMERIC(12, 8),
    longitude NUMERIC(12, 8),
    placement VARCHAR(128),
    racks INTEGER,
    spaces INTEGER,
    status CHAR(20)
  ); 
   
  CREATE INDEX parking_spots_latitude_idx
    ON parking_spots
    USING GIST (latitude); 

  CREATE INDEX parking_spots_longitude_idx
    ON parking_spots
    USING GIST (latitude); 
EOF

psql sf_bike_racks << EOF
  COPY 
    parking_spots(
      address,
      location,
      latitude,
      longitude,
      placement,
      racks,
      spaces,
      status
    )
    FROM 
      '`pwd`/postgres_seed.csv'
    DELIMITER 
      ',' 
    CSV;
EOF

