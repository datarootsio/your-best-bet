{% set team_attrs = ["buildupplaydribbling",
        "buildupplaydribblingclass",
        "buildupplayspeed",
        "buildupplayspeedclass",
        "buildupplaypassing",
        "buildupplaypassingclass",
        "buildupplaypositioningclass",
        "chancecreationpassing",
        "chancecreationpassingclass",
        "chancecreationcrossing",
        "chancecreationcrossingclass",
        "chancecreationshooting",
        "chancecreationshootingclass",
        "chancecreationpositioningclass",
        "defencepressure",
        "defencepressureclass",
        "defenceaggression",
        "defenceaggressionclass",
        "defenceteamwidth",
        "defenceteamwidthclass",
        "defencedefenderlineclass"] %}

select
    match.id,
    match.league_id,
    season.season,
    match.stage,
    match.match_date,

    match.home_team_goal,
    match.away_team_goal,
    case when match.home_team_goal > match.away_team_goal then 'home'
        when match.home_team_goal = match.away_team_goal then 'draw'
        when match.home_team_goal < match.away_team_goal then 'away'
    end as winner,

    home_team.team_id AS home_team_id,
    home_team.team_name AS home_team_name,
    away_team.team_id AS away_team_id,
    away_team.team_name AS away_team_name,

    {% for c in team_attrs %}
    home_team.{{c}} as home_{{c}},
    away_team.{{c}} as away_{{c}},
    {% endfor %}

    {{ dbt_utils.safe_divide(
        'match.stage',
        'max_stages_per_season'
    ) }} as season_progress
    
    -- match.match_date as valid_from,
    -- lead(match.match_date) over (partition by team_id order by match_date) AS valid_to
from
    {{ ref('match') }}
    match
    inner join {{ ref('season') }}
    season
    on match.league_id = season.league_id
    and match.season = season.season
    left join {{ ref('team_kpi') }}
    home_team
    on home_team.team_id = match.home_team_api_id
        and home_team.match_id = match.id
    left join {{ ref('team_kpi') }}
    away_team
    on away_team.team_id = match.away_team_api_id
        and away_team.match_id = match.id
