select substr(p.prediction_id, 1, 8) as prediction_id
    , m.match_date
    , m.home_team_name as home_team
    , m.away_team_name as away_team
    , p.bet
    , round(p.xOdd, 2) as xOdd
    , p.bookie
    , p.odd_bookie
    , round(p.xProfit, 2) as xProfit
    -- , p.model_path
    -- , e.algorithm
from {{ref("predict_output")}} p
inner join {{ref("predict_input")}} m
    on p.prediction_id = m.prediction_id
inner join {{ref("experiment_history")}} e
    on p.model_path = e.best_estimator_path
        and e.rank_test_neg_log_loss = 1
        and e.algorithm = "{{ var('algorithm', 'logistic_regression') }}"
where m.match_date >= {{ var('check_date', '2015-12-29') }}
    and league_name = {{ var('league_name', 'England Premier League') }}
order by m.match_date
    , home_team
limit {{ var('top_predictions', 100) }}
