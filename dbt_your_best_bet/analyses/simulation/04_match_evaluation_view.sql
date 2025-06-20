select substr(eval.prediction_id, 1, 8) as prediction_id
    , eval.match_date
    , m.home_team_name
    , m.away_team_name
    , bet
    , round(xOdd, 2) as xOdd
    , bookie
    , odd_bookie
    , winner
    , bet_correct
    , round(profit, 2) as profit
from {{ ref('evaluation') }} eval
inner join {{ ref('predict_input') }} m
    on eval.prediction_id = m.prediction_id
inner join {{ ref('experiment_history') }} e
    on eval.model_path = e.best_estimator_path
        and e.rank_test_neg_log_loss = 1
        and e.algorithm = "{{ var('algorithm', 'logistic_regression') }}"
where m.match_date >= {{ var('check_date', '2015-12-29') }}
    and league_name = {{ var('league_name', 'England Premier League') }}
order by m.match_date
