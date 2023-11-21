{% set match_columns = dbt_utils.get_filtered_columns_in_relation(ref('match_dataset')) %}
{% set leakage_columns = [
 'away_match_points',
 'away_players',
 'away_team_goal',
 'home_match_points',
 'home_players',
 'home_team_goal',
 'winner'] %}

select
    {{ dbt_utils.generate_surrogate_key(match_columns | reject("in", leakage_columns)) }} AS prediction_id,
    {{ dbt_utils.star(ref('match_dataset'), except=leakage_columns) }}
from
    {{ ref('match_dataset') }} dataset
where "{{ var('train_end_date') }}" < dataset.match_date
