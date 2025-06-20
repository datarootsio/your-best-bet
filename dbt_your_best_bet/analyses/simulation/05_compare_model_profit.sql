with latest_match_prediction_per_model as (
  select eval.* except(model_path),
    xp.algorithm as model,
    xp.params,
    split(model_path, '/')[size(split(model_path, '/')) - 1] as model_path,
  from {{ ref('evaluation') }} eval
  inner join {{ ref('experiment_history') }} xp
    on xp.best_estimator_path = eval.model_path
      and xp.rank_test_neg_log_loss = 1
  qualify row_number()
    over (partition by model_path, id order by prediction_timestamp desc)
    = 1
)

select model_path, model,
  sum(if(xProfit > 0, profit, 0)) as total_profit,
  avg(if(xProfit > 0, profit, 0)) as avg_profit_per_bet,
  count(distinct id) as nbr_matches_predicted
from latest_match_prediction_per_model
where {{ var('train_end_date', '2015-07-31') }} < match_date and match_date < {{ var('run_date', '2015-12-29') }}
  and league_name = {{ var('league_name', 'England Premier League') }}
group by 1, 2
order by total_profit desc
