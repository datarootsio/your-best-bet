with latest_match_prediction_per_model as (
  select eval.*,
    xp.class as model,
    xp.params
  from {{ref("evaluation")}} eval
  inner join {{ref("experiment_history")}} xp
    on xp.best_estimator_path = eval.model_path
      and xp.rank_test_neg_log_loss = 1
  qualify row_number() over (partition by model_path, id order by prediction_timestamp desc) = 1
)

select match_date, model_path,
  sum(if(xProfit > 0, profit, 0)) as day_profit,
  avg(if(xProfit > 0, profit, 0)) as avg_profit,
  count(distinct id) as nbr_matches_predicted,
  sum(sum(if(xProfit > 0, profit, 0))) over (partition by model_path order by match_date) AS total_profit,
  sum(count(distinct id)) over (partition by model_path order by match_date) AS total_nbr_predictions
from latest_match_prediction_per_model
where '{{var("train_end_date")}}' < match_date
group by match_date, model_path
order by match_date desc, model_path
