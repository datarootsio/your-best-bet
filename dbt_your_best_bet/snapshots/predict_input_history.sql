{% snapshot predict_input_history %}
    {{ config(
        target_schema = 'snapshots',
        unique_key = 'id',
        strategy = 'check',
        check_cols = ['prediction_id'],
    ) }}

    select
        *
    from
        {{ ref('predict_input') }}
{% endsnapshot %}
