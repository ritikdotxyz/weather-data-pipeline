with renamed as (
    select 
        -- station
        CAST(STATION AS varchar) AS station_id,
        CAST(STATION_NAME AS varchar) AS station_name,

        -- datetime
        CAST(DATE AS timestamp) AS date,
        CAST(Year AS numeric) AS year,
        CAST(Month AS integer) AS month,
        CAST(Day AS integer) AS day,

        -- location
        CAST(LATITUDE AS numeric) AS latitude,
        CAST(LONGITUDE AS numeric) AS longitude,
        CAST(ELEVATION AS numeric) AS elevation,

        -- metrics
        CAST(mean_temperature AS numeric) AS mean_temperature,
        CAST(mean_temperature_Measurement_Code AS numeric) AS mean_temperature_measurement_code,
        CAST(mean_dew_point_temperature AS numeric) AS mean_dew_point_temperature,
        CAST(mean_dew_point_temperature_Measurement_Code AS numeric) AS mean_dew_point_temperature_measurement_code,
        CAST(mean_sea_level_pressure AS numeric) AS mean_sea_level_pressure,
        CAST(mean_sea_level_pressure_Measurement_Code AS numeric) AS mean_sea_level_pressure_measurement_code,
        CAST(mean_station_level_pressure AS numeric) AS mean_station_level_pressure,
        CAST(mean_station_level_pressure_Measurement_Code AS numeric) AS mean_station_level_pressure_measurement_code,
        CAST(mean_visibility AS numeric) AS mean_visibility,
        CAST(mean_visibility_Measurement_Code AS numeric) AS mean_visibility_measurement_code,
        CAST(mean_wind_speed AS numeric) AS mean_wind_speed ,
        CAST(mean_wind_speed_Measurement_Code AS numeric) AS mean_wind_speed_measurement_code,
        CAST(max_wind_speed AS numeric) AS max_wind_speed,
        CAST(max_wind_gust AS numeric) AS max_wind_gust,
        CAST(max_temperature AS numeric) AS max_temperature,
        CAST(max_temperature_Measurement_Code AS numeric) AS max_temperature_measurement_code,
        CAST(min_temperature AS numeric) AS min_temperature,
        CAST(min_temperature_Measurement_Code AS numeric) as min_temperature_measurement_code,
        CAST(total_precipitation AS numeric) AS total_precipitation,
        CAST(total_precipitation_Measurement_Code AS integer) as total_precipitation_measurement_code,
        CAST(snow_depth AS numeric) AS snow_depth,
        CAST(observed_pres_wx AS integer) AS observed_pres_wx 

    from {{ source('staging', 'weather_ssod_t1') }}
)



SELECT
    * REPLACE (
        {{ set_null('mean_temperature') }} AS mean_temperature,
        {{ set_null('mean_dew_point_temperature') }} AS mean_dew_point_temperature,
        {{ set_null('mean_sea_level_pressure') }} AS mean_sea_level_pressure,
        {{ set_null('mean_station_level_pressure') }} AS mean_station_level_pressure,
        {{ set_null('mean_visibility') }} AS mean_visibility,
        {{ set_null('mean_wind_speed') }} AS mean_wind_speed,
        {{ set_null('max_wind_speed') }} AS max_wind_speed,
        {{ set_null('max_wind_gust') }} AS max_wind_gust,
        {{ set_null('max_temperature') }} AS max_temperature,
        {{ set_null('min_temperature') }} AS min_temperature,
        {{ set_null('snow_depth') }} AS snow_depth
    )
FROM renamed
