with source as (

    select * from {{ source('european_soccer_db', 'player') }}

),

renamed as (

    select
        id,
        player_api_id,
        player_name,
        player_fifa_api_id,
        birthday,
        height,
        weight

    from source

)

select * from renamed
