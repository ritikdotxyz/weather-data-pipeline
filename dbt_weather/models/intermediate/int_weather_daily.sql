with weather as (
    select * from {{ ref('stg_weather_ssod') }}
),

daily as (
    select 
        station_id,
        station_name,
    latitude,
    longitude,
    elevation,

        date,
        max_temperature,
        min_temperature,
        mean_temperature,
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
            then max_temperature - min_temperature
            else null
        end as temperature_range,

        case 
            when max_temperature is not null
            and min_temperature is not null
            then ( max_temperature + min_temperature ) / 2.0
            else null
        end as midpoint_temprature

    from weather
)

select * from daily