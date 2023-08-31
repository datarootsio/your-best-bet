with source as (

    select * from {{ source('european_soccer_db', 'player_attributes') }}

),

renamed as (

    select
        id,
        player_fifa_api_id,
        player_api_id,
        date(date) as date,
        overall_rating,
        potential,
        preferred_foot,
        attacking_work_rate,
        defensive_work_rate,
        crossing,
        finishing,
        heading_accuracy,
        short_passing,
        volleys,
        dribbling,
        curve,
        free_kick_accuracy,
        long_passing,
        ball_control,
        acceleration,
        sprint_speed,
        agility,
        reactions,
        balance,
        shot_power,
        jumping,
        stamina,
        strength,
        long_shots,
        aggression,
        interceptions,
        positioning,
        vision,
        penalties,
        marking,
        standing_tackle,
        sliding_tackle,
        gk_diving,
        gk_handling,
        gk_kicking,
        gk_positioning,
        gk_reflexes,
        date(date) as valid_from,
        date(lead(date) over (partition by player_api_id order by date)) AS valid_to

    from source
    where
        date BETWEEN date('{{var("start_date")}}')
        AND date('{{var("run_date")}}')
)

select * from renamed
