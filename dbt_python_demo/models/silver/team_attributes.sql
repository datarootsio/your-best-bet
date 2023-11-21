with source as (

    select * from {{ source('european_soccer_db', 'team_attributes') }}

),

renamed as (

    select
        id,
        team_fifa_api_id,
        team_api_id,
        date(date) AS team_attribute_date,
        buildupplayspeed,
        buildupplayspeedclass,
        buildupplaydribbling,
        buildupplaydribblingclass,
        buildupplaypassing,
        buildupplaypassingclass,
        buildupplaypositioningclass,
        chancecreationpassing,
        chancecreationpassingclass,
        chancecreationcrossing,
        chancecreationcrossingclass,
        chancecreationshooting,
        chancecreationshootingclass,
        chancecreationpositioningclass,
        defencepressure,
        defencepressureclass,
        defenceaggression,
        defenceaggressionclass,
        defenceteamwidth,
        defenceteamwidthclass,
        defencedefenderlineclass,
        date(date) as valid_from,
        date(lead(date) over (partition by team_api_id order by date)) AS valid_to

    from source
    where
        date >= date('{{var("start_date")}}')
        AND date < date('{{var("run_date")}}')

)

select * from renamed
