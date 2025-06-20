select match_date as day
    , home_team_name as home
    , away_team_name as away
    , odds_b365h as b635h
    , odds_b365d as b635d
    , odds_b365a as b635a
    , home_team_form_5m as home_form_5m
    , away_team_form_5m as away_form_5m
    , winner
from {{ ref('match_dataset') }}
where match_date >= {{ var('check_date', '2015-12-29') }}
    and league_name = {{ var('league_name', 'England Premier League') }}
order by match_date
