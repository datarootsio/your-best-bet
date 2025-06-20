select train_end_date
    , algorithm
    , substr(experiment_id, 1, 8) as experiment_id
    , rank_test_neg_log_loss as rank_log_loss
    , round(mean_test_roc_auc_ovr, 4) as mean_test_auc
    , params
    , best_estimator_path
from {{ ref('experiment_history') }}
order by mean_test_neg_log_loss desc
limit {{ var('top_experiments', 10) }}
