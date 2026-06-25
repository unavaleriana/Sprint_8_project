SELECT 
    COUNT(trips.trip_id) AS trips_amount,
    cabs.company_name AS company_name
FROM 
    trips
    INNER JOIN cabs ON cabs.cab_id = trips.cab_id
WHERE 
    CAST(start_ts AS date) = '2017-11-15'
    OR 
    CAST(start_ts AS date) = '2017-11-16'
GROUP BY 
    cabs.company_name
ORDER BY 
    trips_amount DESC

-- Segundo punto
SELECT 
    COUNT (trips.trip_id) AS trips_amount,
    cabs.company_name AS company_name
FROM 
    trips
INNER JOIN 
    cabs ON cabs.cab_id = trips.cab_id
WHERE 
    CAST(trips.start_ts AS date) BETWEEN '2017-11-01' AND '2017-11-07'
    AND (cabs.company_name LIKE '%%Yellow%%' 
    OR cabs.company_name LIKE '%%Blue%%')
GROUP BY 
    cabs.company_name
-- Tarea 3
SELECT 
     CASE 
        WHEN company_name = 'Flash Cab' THEN 'Flash Cab'
        WHEN company_name = 'Taxi Affiliation Services' THEN 'Taxi Affiliation Services'
        ELSE 'Other'
    END AS company,
    COUNT(trips.trip_id) AS trips_amount
FROM 
    trips
INNER JOIN 
    cabs ON cabs.cab_id = trips.cab_id
WHERE 
    CAST(trips.start_ts AS DATE) BETWEEN '2017-11-01' AND '2017-11-07'  
GROUP BY 
    company
ORDER BY 
    trips_amount DESC
-- Tarea 4
SELECT 
    neighborhoods.neighborhood_id AS neighborhood_id,
    neighborhoods.name AS name
FROM 
    neighborhoods
WHERE 
    neighborhoods.name LIKE '%Hare'
    OR neighborhoods.name LIKE 'Loop'
-- Tarea 5  
SELECT 
    CASE
       WHEN weather_records.description LIKE '%rain%' THEN 'Bad' 
       WHEN weather_records.description LIKE '%storm%' THEN 'Bad'
       ELSE 'Good' 
    END AS weather_conditions, 
    weather_records.ts
FROM 
    weather_records
-- Tarea 6
SELECT 
    trips.start_ts AS start_ts,
    subquery.weather_conditions,
    trips.duration_seconds AS duration_seconds
FROM 
    trips 
INNER JOIN ( 
    SELECT 
        weather_records.ts as ts,
        CASE
           WHEN weather_records.description LIKE '%rain%' THEN 'Bad' 
           WHEN weather_records.description LIKE '%storm%' THEN 'Bad'
           ELSE 'Good' 
        END AS weather_conditions
    FROM weather_records) AS subquery ON subquery.ts = trips.start_ts
WHERE 
    trips.pickup_location_id = 50 AND  -- Loop
    dropoff_location_id = 63 AND -- O'Hare
    EXTRACT(DOW from trips.start_ts) = 6
    
ORDER BY trip_id