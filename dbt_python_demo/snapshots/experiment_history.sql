{% snapshot experiment_history %}

{{
    config(
      target_schema='snapshots',
      unique_key='experiment_id',
      strategy='timestamp',
      updated_at='execution_timestamp',
    )
}}

select * from {{ ref('experiment') }}

{% endsnapshot %}
