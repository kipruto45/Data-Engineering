CREATE TABLE IF NOT EXISTS dim_taxpayer (
    taxpayer_id INTEGER PRIMARY KEY,
    name TEXT,
    pin TEXT,
    registration_date DATE,
    sector TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER
);
