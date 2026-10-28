
select
    station_id,
    date,

    station_name,
    latitude,
    longitude,
    elevation,

    mean_temperature,
    max_temperature,
    min_temperature,
    temperature_range,
    -- midpoint_temprature,

    mean_dew_point_temperature,
    mean_sea_level_pressure,
    mean_station_level_pressure,
    mean_visibility,
    mean_wind_speed,
    max_wind_speed,
    max_wind_gust,
    total_precipitation,
    snow_depth,

    case
        when max_temperature is not null
         and min_temperature is not null
        then true
        else false
    end as has_temperature_observations,

    case
        when total_precipitation is not null
        then true
        else false
    end as has_precipitation_observation

from {{ ref('int_weather_daily') }}
