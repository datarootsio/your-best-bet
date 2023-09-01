with match as (
    select
        id,
        country_id,
        league_id,
        season,
        stage,
        date(date) as match_date,
        match_api_id,
        home_team_api_id,
        away_team_api_id,
        home_team_goal,
        away_team_goal,
        {% for i in range(11) %}
        CAST( home_player_{{ loop.index }}  AS {{ dbt.type_int() }}),
        CAST( away_player_{{ loop.index }}  AS {{ dbt.type_int() }}),
        {% endfor %}

        -- match metadata => leave out for now, weird parsing scheme
        goal,
        shoton,
        shotoff,
        foulcommit,
        card,
        cross,
        corner,
        possession,

        -- bookie odds
        b365h,
        b365d,
        b365a,
        bwh,
        bwd,
        bwa,
        iwh,
        iwd,
        iwa,
        lbh,
        lbd,
        lba,
        psh,
        psd,
        psa,
        whh,
        whd,
        wha,
        sjh,
        sjd,
        sja,
        vch,
        vcd,
        vca,
        gbh,
        gbd,
        gba,
        bsh,
        bsd,
        bsa
    from
        {{ source(
            'european_soccer_db',
            'match'
        ) }}
    where
        date BETWEEN date('{{var("start_date")}}')
        AND date('{{var("run_date")}}')
)
select
    *
from
    match
