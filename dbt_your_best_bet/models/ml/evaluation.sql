select dataset.id,
    input.prediction_id,
    dataset.match_date,
    dataset.winner,
    output.bet,
    output.xOdd,
    output.bookie,
    output.odd_bookie,
    output.xProfit,
    output.xYieldsProfit,
    dataset.winner = output.bet as bet_correct,
    -1 + if(dataset.winner = output.bet, output.odd_bookie, 0) as profit,
    output.model_path,
    output.prediction_timestamp
from {{ ref('match_dataset') }} dataset
inner join {{ ref('predict_input_history') }} input
using (id)
inner join {{ ref('predict_output') }} output
using (prediction_id)
where dataset.match_date < '{{var("run_date")}}'
