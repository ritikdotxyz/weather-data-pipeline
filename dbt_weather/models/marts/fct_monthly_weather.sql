
with daily as (

    select *
    from {{ ref('fct_daily_weather') }}

)

select
    station_id,

    date_trunc('month', date)::date
        as observation_month,

    station_name,
    latitude,
    longitude,
    elevation,

    count(*) as daily_records,

    count(mean_temperature) as mean_temperature_observation_days,
    avg(mean_temperature) as avg_mean_temperature,

    count(max_temperature) as max_temperature_observation_days,
    max(max_temperature) as highest_temperature,

    count(min_temperature) as min_temperature_observation_days,
    min(min_temperature) as lowest_temperature,

    avg(temperature_range) as avg_temperature_range,

    count(total_precipitation) as precipitation_observation_days,
    sum(total_precipitation) as total_recorded_precipitation,

    count(mean_wind_speed) as wind_observation_days,
    avg(mean_wind_speed) as avg_mean_wind_speed,

    count(snow_depth) as snow_depth_observation_days,
    avg(snow_depth) as avg_recorded_snow_depth

from daily

group by
    station_id,
    date_trunc('month', date)::date,
    station_name,
    latitude,
    longitude,
    elevation,
