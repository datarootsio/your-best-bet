select id
    , substr(prediction_id, 1, 8) as prediction_id
    , match_date
    , home_team_id
    , home_team_name
    , home_team_form_5m
    , home_latest_results_5m
    , home_points_per_match
    , home_total_points
from {{ ref('predict_input_history')}}
where 1 = 1
    {% if var('check_date') %}
    and match_date >= {{ var('check_date', '2015-12-29') }}
    {% endif %}
    {% if var('league_name') %}
    and league_name = {{ var('league_name', 'England Premier League') }}
    {% endif %}

qualify count(id) over (partition by id) > 1
order by match_date, id
