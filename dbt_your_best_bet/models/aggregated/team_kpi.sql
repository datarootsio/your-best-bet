{% set stat_functions = ['avg', 'median', 'min', 'max'] %}
{% set team_attrs = ["buildupplaydribbling", "buildupplaydribblingclass","buildupplayspeed","buildupplayspeedclass","buildupplaypassing","buildupplaypassingclass","buildupplaypositioningclass","chancecreationpassing","chancecreationpassingclass","chancecreationcrossing","chancecreationcrossingclass","chancecreationshooting","chancecreationshootingclass","chancecreationpositioningclass","defencepressure","defencepressureclass","defenceaggression","defenceaggressionclass","defenceteamwidth","defenceteamwidthclass","defencedefenderlineclass"] %}
{% set player_stats_numeric = ['overall_rating','potential','crossing','finishing','heading_accuracy','short_passing','volleys','dribbling','curve','free_kick_accuracy','long_passing','ball_control','acceleration','sprint_speed','agility','reactions','balance','shot_power','jumping','stamina','strength','long_shots','aggression','interceptions','positioning','vision','penalties','marking','standing_tackle','sliding_tackle','gk_diving','gk_handling','gk_kicking','gk_positioning','gk_reflexes'] %}
{% set player_stats_categorical = ['preferred_foot', 'attacking_work_rate', 'defensive_work_rate'] %}

with team_match_attributes AS (
    select
        team_match.*,
        buildupplaydribbling,
        buildupplaydribblingclass,
        buildupplayspeed,
        buildupplayspeedclass,
        buildupplaypassing,
        buildupplaypassingclass,
        buildupplaypositioningclass,
        chancecreationpassing,
        chancecreationpassingclass,
        chancecreationcrossing,
        chancecreationcrossingclass,
        chancecreationshooting,
        chancecreationshootingclass,
        chancecreationpositioningclass,
        defencepressure,
        defencepressureclass,
        defenceaggression,
        defenceaggressionclass,
        defenceteamwidth,
        defenceteamwidthclass,
        defencedefenderlineclass,
        lag(match_id) over (team_window) as previous_match_id,
        sum(match_points) over (team_window_5) as team_form_5m,
        concat(array_agg(result) over (team_window_5)) as latest_results_5m,
        sum(match_points) over (team_season_window) as total_points,
        avg(match_points) over (team_season_window) as points_per_match
    from
        {{ ref('team_match') }} team_match
        left join {{ ref('team_attributes') }}
        team_attributes
        on team_match.team_id = team_attributes.team_api_id
        and team_attributes.valid_from <= team_match.match_date
        and team_match.match_date < coalesce(
            team_attributes.valid_to,
            '2999-12-31'
        )
    window
        team_window as (partition by team_id order by match_date),
        team_window_5 AS (partition by team_id order by match_date rows between 5 preceding and 1 preceding),
        team_season_window as (partition by league_id, season, team_id 
                                order by match_date 
                                rows between unbounded preceding and 1 preceding)
),

player_match_aggregated AS (
    select player_match.match_id,
        player_match.team_id,

        {% for f in stat_functions %}
            {{f}}({{ dbt.datediff('birthday', 'match_date', 'year') }}) AS {{f}}_age,
            cast({{f}}(height) as decimal) AS {{f}}_height,
            cast({{f}}(weight) as decimal) AS {{f}}_weight,
        {% endfor %}

        {% for att in player_stats_numeric %}
            {% for f in stat_functions %}
                cast({{f}}({{ att }}) as decimal) AS {{f}}_{{att}},
            {% endfor %}
        {% endfor %}

        {% for att in player_stats_categorical %}
            {% set categories = dbt_utils.get_column_values(table=ref('player_attributes'), column=att) %}
            {% for cat in categories if cat %}
                count_if({{att}} = '{{cat}}') AS count_{{ att }}_{{ cat }},
            {% endfor %}
        {% endfor %}

        array_agg(player_match.player_id) as players

    from {{ ref("player_match") }} player_match
    left join {{ ref("player_attributes") }} player_attributes
        on player_match.player_id = player_attributes.player_api_id
        and valid_from <= player_match.match_date 
        and player_match.match_date < coalesce(
            player_attributes.valid_to,
            '2999-12-31'
        )
    group by player_match.match_id, player_match.team_id
)

, team_kpi as (
    select
        team_match_attributes.*,
        player_match_aggregated.* except (match_id, team_id)
    from team_match_attributes
    -- Notice how we're joining with the previous game to get insights on the team strength
    left join player_match_aggregated
        on team_match_attributes.previous_match_id = player_match_aggregated.match_id
        and team_match_attributes.team_id = player_match_aggregated.team_id
)

select *
from team_kpi
