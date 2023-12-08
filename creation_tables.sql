# SQL file to initialize DB
DROP TABLE IF EXISTS `arrivals`;  
DROP TABLE IF EXISTS `forecasts`;
DROP TABLE IF EXISTS `cities`;
DROP TABLE IF EXISTS `airports`;    


CREATE TABLE `cities` (
	id_city INT AUTO_INCREMENT,
    city VARCHAR(100),
    country VARCHAR(100),
    population INT,
    timezone VARCHAR(30),
    PRIMARY KEY (id_city)
);

CREATE TABLE `forecasts` (
	id INT AUTO_INCREMENT,
    id_city INT,
    date_forecast DATETIME,
    main_temp FLOAT,
    rain_percent FLOAT,
    wind_speed FLOAT,
    description VARCHAR(256),
    PRIMARY KEY (id),
    FOREIGN KEY (id_city) REFERENCES cities (id_city)
);

  CREATE TABLE `airports` (
	id_airport INT AUTO_INCREMENT,
	name VARCHAR(200),
    icao VARCHAR(6) UNIQUE,
    city VARCHAR(200),
    country VARCHAR(200),
    PRIMARY KEY (id_airport)
);

CREATE TABLE `arrivals` (
	id BIGINT,
	identification VARCHAR(50),
	arrivalAirport VARCHAR(6),
	departureAirport VARCHAR(6),
	landing_time DATETIME,
    PRIMARY KEY (id),
	FOREIGN KEY (arrivalAirport) REFERENCES airports (icao),
    FOREIGN KEY (departureAirport) REFERENCES airports (icao)
);
