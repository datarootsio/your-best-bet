with team_match_attributes AS (
    select
        team_match.*,
        buildupplaydribbling,
        buildupplaydribblingclass,
        buildupplayspeed,
        buildupplayspeedclass,
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
        defencedefenderlineclass
    from
        {{ ref('team_match') }} team_match
        left join {{ ref('team_attributes') }}
        team_attributes
        on team_match.team_id = team_attributes.team_api_id
    where
        team_attributes.valid_from <= team_match.match_date
        and team_match.match_date < coalesce(
            team_attributes.valid_to,
            '2999-12-31'
        )
),

player_match_attributes AS (
    select player_match.*,
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
        gk_reflexes
    from {{ ref("player_match") }} player_match
    left join {{ ref("player_attributes") }} player_attributes
        on player_match.player_id = player_attributes.player_api_id
        and player_match.match_date < coalesce(
            player_attributes.valid_to,
            '2999-12-31'
        )
)


select
    team_match_attributes.*,
        player_id,
        player_name,
        birthday,
        height,
        weight,
        -- buildupplaydribbling,
        -- buildupplaydribblingclass,
        -- buildupplayspeed,
        -- buildupplayspeedclass,
        -- buildupplaypassing,
        -- buildupplaypassingclass,
        -- buildupplaypositioningclass,
        -- chancecreationpassing,
        -- chancecreationpassingclass,
        -- chancecreationcrossing,
        -- chancecreationcrossingclass,
        -- chancecreationshooting,
        -- chancecreationshootingclass,
        -- chancecreationpositioningclass,
        -- defencepressure,
        -- defencepressureclass,
        -- defenceaggression,
        -- defenceaggressionclass,
        -- defenceteamwidth,
        -- defenceteamwidthclass,
        -- defencedefenderlineclass,
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
        gk_reflexes
from team_match_attributes
inner join player_match_attributes
    on team_match_attributes.match_id = player_match_attributes.match_id
    and team_match_attributes.team_id = player_match_attributes.team_id

