with league_season_info as (
    select
        league.id as league_id,
        league.name as league_name,
        match.season,
        country.name as country,
        max(match.stage) as max_stages_per_season,
        count(
            distinct match.stage
        ) as nbr_stages_in_season,
        count(distinct match.id) as nbr_matches_in_season,
        {{ dbt_utils.safe_divide('count(distinct match.id)', 'count(distinct match.stage)') }} as nbr_matches_per_stage,
        count(distinct match.home_team_api_id) as nbr_teams,
        min(match.match_date) AS first_match_date,
        max(match.match_date) AS last_match_date
    from
        {{ ref('league') }}
        league
        inner join {{ ref('country') }}
        country
        on league.country_id = country.id
        left join ({{ ref('match') }}) match
        on league.id = match.league_id 
    {{ dbt_utils.group_by(
            n = 4
        ) }}
)
select
    *
from
    league_season_info
order by league_id, season
