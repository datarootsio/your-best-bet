with latest_match_prediction_per_model as (
  select eval.*,
    xp.class as model,
    xp.params
  from {{ref('evaluation')}} eval
  inner join {{ref('experiment_history')}} xp
    on xp.best_estimator_path = eval.model_path
      and xp.rank_test_neg_log_loss = 1
  qualify row_number() 
    over (partition by model_path, id order by prediction_timestamp desc) 
    = 1
)

select model_path, model, params,
  sum(if(xProfit > 0, profit, 0)) as total_profit,
  avg(if(xProfit > 0, profit, 0)) as avg_profit_per_bet,
  count(distinct id) as nbr_matches_predicted
from latest_match_prediction_per_model
where '{{var("train_end_date")}}' < match_date and match_date < '{{var("run_date")}}' 
group by 1, 2, 3
order by total_profit desc
