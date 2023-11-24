with source as (

    select * from {{ source('eu_soccer_db', 'team') }}

),

renamed as (

    select
        id,
        team_api_id,
        team_fifa_api_id,
        team_long_name,
        team_short_name

    from source

)

select * from renamed
