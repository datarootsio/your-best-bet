with player_match AS (
    {% for home_or_away in ["home", "away"] %}
        {% for i in range(1, 12) %}
            select 
                match.id as match_id,
                match.{{home_or_away}}_team_api_id AS team_id,
                match.match_date,
                match.season,
                match.stage,
                player.player_api_id as player_id,
                player.player_name,
                player.birthday,
                player.height,
                player.weight     
            from
                {{ ref('match') }} match
                left join {{ ref('player') }}
                player
                on match.{{home_or_away}}_player_{{i}} = player.player_api_id
            -- sometimes the player is not filled in
            where match.{{home_or_away}}_player_{{i}} is not null     
            {% if not loop.last %}union all{% endif %}
        {% endfor %}
        {% if not loop.last %}union all{% endif %}
    {% endfor %}
)


select player_match.*,
    team.team_long_name as team_name
from player_match
left join {{ ref('team') }} team
    on team.team_api_id = player_match.team_id
