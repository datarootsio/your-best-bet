-- home teams
select
    match.id as match_id,
    team.team_api_id AS team_id,
    team.team_long_name AS team_name,
    match.match_date,
    match.league_id,
    match.season,
    match.stage,
    'home' AS home_or_away,
    opponent_team.team_api_id AS opponent_team_id,
    opponent_team.team_long_name AS opponent_team_name,
    match.home_team_goal AS goals_scored,
    match.away_team_goal AS goals_conceded,
    case
        when match.home_team_goal > match.away_team_goal then 'W'
        when match.home_team_goal = match.away_team_goal then 'D'
        when match.home_team_goal < match.away_team_goal then 'L'
    end as result,
    case
        when match.home_team_goal > match.away_team_goal then 3
        when match.home_team_goal = match.away_team_goal then 1
        when match.home_team_goal < match.away_team_goal then 0
    end as match_points
from
    {{ ref('match') }}
    match
    left join {{ ref('team') }}
    team
    on team.team_api_id = match.home_team_api_id
    left join {{ ref('team') }}
    opponent_team
    on opponent_team.team_api_id = match.away_team_api_id
union all
    -- away teams
select
    match.id as match_id,
    team.team_api_id AS team_id,
    team.team_long_name AS team_name,
    match.match_date,
    match.league_id,
    match.season,
    match.stage,
    'away' AS home_or_away,
    opponent_team.team_api_id AS opponent_team_id,
    opponent_team.team_long_name AS opponent_team_name,
    match.away_team_goal AS goals_scored,
    match.home_team_goal AS goals_conceded,
    case
        when match.home_team_goal > match.away_team_goal then 'L'
        when match.home_team_goal = match.away_team_goal then 'D'
        when match.home_team_goal < match.away_team_goal then 'W'
    end as result,
    case
        when match.home_team_goal > match.away_team_goal then 0
        when match.home_team_goal = match.away_team_goal then 1
        when match.home_team_goal < match.away_team_goal then 3
    end as match_points
from
    {{ ref('match') }}
    match
    left join {{ ref('team') }}
    team
    on team.team_api_id = match.away_team_api_id
    left join {{ ref('team') }}
    opponent_team
    on opponent_team.team_api_id = match.home_team_api_id
