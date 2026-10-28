
with stations as (
    select
    station_id,
    station_name,
    latitude,
    longitude,
    elevation

from {{ ref('int_weather_daily') }}
)



select * from stations
