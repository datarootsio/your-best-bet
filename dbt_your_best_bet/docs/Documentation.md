# European Soccer Database Documentation

This document provides an overview of the source tables and columns defined in the `eu_soccer_db` source, as described in the dbt source YAML file. Each table and column is listed with its data type and a description. Documentation strings are provided in Jinja `docs` blocks for easy integration with dbt.

---

## Source: `eu_soccer_db`

{% docs eu_soccer_db %}
The `eu_soccer_db` source contains tables related to European soccer matches, players, teams, and their attributes, as extracted from the European Soccer Database.
{% enddocs %}

### Table: `match`
{% docs eu_soccer_db_match %}
Contains information about individual soccer matches, including teams, players, scores, and betting odds.
{% enddocs %}
| Column                | Data Type | Description |
|-----------------------|-----------|-------------|
| id                    | BIGINT    | {% docs match_id %}Primary key for the match table.{% enddocs %} |
| country_id            | BIGINT    | {% docs match_country_id %}Foreign key to the country where the match was played.{% enddocs %} |
| league_id             | BIGINT    | {% docs match_league_id %}Foreign key to the league in which the match was played.{% enddocs %} |
| season                | STRING    | {% docs match_season %}Season identifier (e.g., 2015/2016).{% enddocs %} |
| stage                 | BIGINT    | {% docs match_stage %}Stage of the competition or league.{% enddocs %} |
| date                  | STRING    | {% docs match_date %}Date when the match was played.{% enddocs %} |
| match_api_id          | BIGINT    | {% docs match_match_api_id %}Unique API identifier for the match.{% enddocs %} |
| home_team_api_id      | BIGINT    | {% docs match_home_team_api_id %}API identifier for the home team.{% enddocs %} |
| away_team_api_id      | BIGINT    | {% docs match_away_team_api_id %}API identifier for the away team.{% enddocs %} |
| home_team_goal        | BIGINT    | {% docs match_home_team_goal %}Number of goals scored by the home team.{% enddocs %} |
| away_team_goal        | BIGINT    | {% docs match_away_team_goal %}Number of goals scored by the away team.{% enddocs %} |
| home_player_x1        | DOUBLE    | {% docs match_home_player_x1 %}Team lineup: X-coordinate of home player 1's position.{% enddocs %} |
| home_player_x2        | DOUBLE    | {% docs match_home_player_x2 %}Team lineup: X-coordinate of home player 2's position.{% enddocs %} |
| home_player_x3        | DOUBLE    | {% docs match_home_player_x3 %}Team lineup: X-coordinate of home player 3's position.{% enddocs %} |
| home_player_x4        | DOUBLE    | {% docs match_home_player_x4 %}Team lineup: X-coordinate of home player 4's position.{% enddocs %} |
| home_player_x5        | DOUBLE    | {% docs match_home_player_x5 %}Team lineup: X-coordinate of home player 5's position.{% enddocs %} |
| home_player_x6        | DOUBLE    | {% docs match_home_player_x6 %}Team lineup: X-coordinate of home player 6's position.{% enddocs %} |
| home_player_x7        | DOUBLE    | {% docs match_home_player_x7 %}Team lineup: X-coordinate of home player 7's position.{% enddocs %} |
| home_player_x8        | DOUBLE    | {% docs match_home_player_x8 %}Team lineup: X-coordinate of home player 8's position.{% enddocs %} |
| home_player_x9        | DOUBLE    | {% docs match_home_player_x9 %}Team lineup: X-coordinate of home player 9's position.{% enddocs %} |
| home_player_x10       | DOUBLE    | {% docs match_home_player_x10 %}Team lineup: X-coordinate of home player 10's position.{% enddocs %} |
| home_player_x11       | DOUBLE    | {% docs match_home_player_x11 %}Team lineup: X-coordinate of home player 11's position.{% enddocs %} |
| away_player_x1        | DOUBLE    | {% docs match_away_player_x1 %}Team lineup: X-coordinate of away player 1's position.{% enddocs %} |
| away_player_x2        | DOUBLE    | {% docs match_away_player_x2 %}Team lineup: X-coordinate of away player 2's position.{% enddocs %} |
| away_player_x3        | DOUBLE    | {% docs match_away_player_x3 %}Team lineup: X-coordinate of away player 3's position.{% enddocs %} |
| away_player_x4        | DOUBLE    | {% docs match_away_player_x4 %}Team lineup: X-coordinate of away player 4's position.{% enddocs %} |
| away_player_x5        | DOUBLE    | {% docs match_away_player_x5 %}Team lineup: X-coordinate of away player 5's position.{% enddocs %} |
| away_player_x6        | DOUBLE    | {% docs match_away_player_x6 %}Team lineup: X-coordinate of away player 6's position.{% enddocs %} |
| away_player_x7        | DOUBLE    | {% docs match_away_player_x7 %}Team lineup: X-coordinate of away player 7's position.{% enddocs %} |
| away_player_x8        | DOUBLE    | {% docs match_away_player_x8 %}Team lineup: X-coordinate of away player 8's position.{% enddocs %} |
| away_player_x9        | DOUBLE    | {% docs match_away_player_x9 %}Team lineup: X-coordinate of away player 9's position.{% enddocs %} |
| away_player_x10       | DOUBLE    | {% docs match_away_player_x10 %}Team lineup: X-coordinate of away player 10's position.{% enddocs %} |
| away_player_x11       | DOUBLE    | {% docs match_away_player_x11 %}Team lineup: X-coordinate of away player 11's position.{% enddocs %} |
| home_player_y1        | DOUBLE    | {% docs match_home_player_y1 %}Team lineup: Y-coordinate of home player 1's position.{% enddocs %} |
| home_player_y2        | DOUBLE    | {% docs match_home_player_y2 %}Team lineup: Y-coordinate of home player 2's position.{% enddocs %} |
| home_player_y3        | DOUBLE    | {% docs match_home_player_y3 %}Team lineup: Y-coordinate of home player 3's position.{% enddocs %} |
| home_player_y4        | DOUBLE    | {% docs match_home_player_y4 %}Team lineup: Y-coordinate of home player 4's position.{% enddocs %} |
| home_player_y5        | DOUBLE    | {% docs match_home_player_y5 %}Team lineup: Y-coordinate of home player 5's position.{% enddocs %} |
| home_player_y6        | DOUBLE    | {% docs match_home_player_y6 %}Team lineup: Y-coordinate of home player 6's position.{% enddocs %} |
| home_player_y7        | DOUBLE    | {% docs match_home_player_y7 %}Team lineup: Y-coordinate of home player 7's position.{% enddocs %} |
| home_player_y8        | DOUBLE    | {% docs match_home_player_y8 %}Team lineup: Y-coordinate of home player 8's position.{% enddocs %} |
| home_player_y9        | DOUBLE    | {% docs match_home_player_y9 %}Team lineup: Y-coordinate of home player 9's position.{% enddocs %} |
| home_player_y10       | DOUBLE    | {% docs match_home_player_y10 %}Team lineup: Y-coordinate of home player 10's position.{% enddocs %} |
| home_player_y11       | DOUBLE    | {% docs match_home_player_y11 %}Team lineup: Y-coordinate of home player 11's position.{% enddocs %} |
| away_player_y1        | DOUBLE    | {% docs match_away_player_y1 %}Team lineup: Y-coordinate of away player 1's position.{% enddocs %} |
| away_player_y2        | DOUBLE    | {% docs match_away_player_y2 %}Team lineup: Y-coordinate of away player 2's position.{% enddocs %} |
| away_player_y3        | DOUBLE    | {% docs match_away_player_y3 %}Team lineup: Y-coordinate of away player 3's position.{% enddocs %} |
| away_player_y4        | DOUBLE    | {% docs match_away_player_y4 %}Team lineup: Y-coordinate of away player 4's position.{% enddocs %} |
| away_player_y5        | DOUBLE    | {% docs match_away_player_y5 %}Team lineup: Y-coordinate of away player 5's position.{% enddocs %} |
| away_player_y6        | DOUBLE    | {% docs match_away_player_y6 %}Team lineup: Y-coordinate of away player 6's position.{% enddocs %} |
| away_player_y7        | DOUBLE    | {% docs match_away_player_y7 %}Team lineup: Y-coordinate of away player 7's position.{% enddocs %} |
| away_player_y8        | DOUBLE    | {% docs match_away_player_y8 %}Team lineup: Y-coordinate of away player 8's position.{% enddocs %} |
| away_player_y9        | DOUBLE    | {% docs match_away_player_y9 %}Team lineup: Y-coordinate of away player 9's position.{% enddocs %} |
| away_player_y10       | DOUBLE    | {% docs match_away_player_y10 %}Team lineup: Y-coordinate of away player 10's position.{% enddocs %} |
| away_player_y11       | DOUBLE    | {% docs match_away_player_y11 %}Team lineup: Y-coordinate of away player 11's position.{% enddocs %} |
| home_player_1         | DOUBLE    | {% docs match_home_player_1 %}API ID of home player 1.{% enddocs %} |
| home_player_2         | DOUBLE    | {% docs match_home_player_2 %}API ID of home player 2.{% enddocs %} |
| home_player_3         | DOUBLE    | {% docs match_home_player_3 %}API ID of home player 3.{% enddocs %} |
| home_player_4         | DOUBLE    | {% docs match_home_player_4 %}API ID of home player 4.{% enddocs %} |
| home_player_5         | DOUBLE    | {% docs match_home_player_5 %}API ID of home player 5.{% enddocs %} |
| home_player_6         | DOUBLE    | {% docs match_home_player_6 %}API ID of home player 6.{% enddocs %} |
| home_player_7         | DOUBLE    | {% docs match_home_player_7 %}API ID of home player 7.{% enddocs %} |
| home_player_8         | DOUBLE    | {% docs match_home_player_8 %}API ID of home player 8.{% enddocs %} |
| home_player_9         | DOUBLE    | {% docs match_home_player_9 %}API ID of home player 9.{% enddocs %} |
| home_player_10        | DOUBLE    | {% docs match_home_player_10 %}API ID of home player 10.{% enddocs %} |
| home_player_11        | DOUBLE    | {% docs match_home_player_11 %}API ID of home player 11.{% enddocs %} |
| away_player_1         | DOUBLE    | {% docs match_away_player_1 %}API ID of away player 1.{% enddocs %} |
| away_player_2         | DOUBLE    | {% docs match_away_player_2 %}API ID of away player 2.{% enddocs %} |
| away_player_3         | DOUBLE    | {% docs match_away_player_3 %}API ID of away player 3.{% enddocs %} |
| away_player_4         | DOUBLE    | {% docs match_away_player_4 %}API ID of away player 4.{% enddocs %} |
| away_player_5         | DOUBLE    | {% docs match_away_player_5 %}API ID of away player 5.{% enddocs %} |
| away_player_6         | DOUBLE    | {% docs match_away_player_6 %}API ID of away player 6.{% enddocs %} |
| away_player_7         | DOUBLE    | {% docs match_away_player_7 %}API ID of away player 7.{% enddocs %} |
| away_player_8         | DOUBLE    | {% docs match_away_player_8 %}API ID of away player 8.{% enddocs %} |
| away_player_9         | DOUBLE    | {% docs match_away_player_9 %}API ID of away player 9.{% enddocs %} |
| away_player_10        | DOUBLE    | {% docs match_away_player_10 %}API ID of away player 10.{% enddocs %} |
| away_player_11        | DOUBLE    | {% docs match_away_player_11 %}API ID of away player 11.{% enddocs %} |
| goal                  | STRING    | {% docs match_goal %}Goal events in XML format.{% enddocs %} |
| shoton                | STRING    | {% docs match_shoton %}Shots on target in XML format.{% enddocs %} |
| shotoff               | STRING    | {% docs match_shotoff %}Shots off target in XML format.{% enddocs %} |
| foulcommit            | STRING    | {% docs match_foulcommit %}Fouls committed in XML format.{% enddocs %} |
| card                  | STRING    | {% docs match_card %}Card events in XML format.{% enddocs %} |
| cross                 | STRING    | {% docs match_cross %}Cross events in XML format.{% enddocs %} |
| corner                | STRING    | {% docs match_corner %}Corner events in XML format.{% enddocs %} |
| possession            | STRING    | {% docs match_possession %}Possession data in XML format.{% enddocs %} |
| b365h                 | DOUBLE    | {% docs match_b365h %}Bet365 odds for home win.{% enddocs %} |
| b365d                 | DOUBLE    | {% docs match_b365d %}Bet365 odds for draw.{% enddocs %} |
| b365a                 | DOUBLE    | {% docs match_b365a %}Bet365 odds for away win.{% enddocs %} |
| bwh                   | DOUBLE    | {% docs match_bwh %}Bwin odds for home win.{% enddocs %} |
| bwd                   | DOUBLE    | {% docs match_bwd %}Bwin odds for draw.{% enddocs %} |
| bwa                   | DOUBLE    | {% docs match_bwa %}Bwin odds for away win.{% enddocs %} |
| iwh                   | DOUBLE    | {% docs match_iwh %}Interwetten odds for home win.{% enddocs %} |
| iwd                   | DOUBLE    | {% docs match_iwd %}Interwetten odds for draw.{% enddocs %} |
| iwa                   | DOUBLE    | {% docs match_iwa %}Interwetten odds for away win.{% enddocs %} |
| lbh                   | DOUBLE    | {% docs match_lbh %}Ladbrokes odds for home win.{% enddocs %} |
| lbd                   | DOUBLE    | {% docs match_lbd %}Ladbrokes odds for draw.{% enddocs %} |
| lba                   | DOUBLE    | {% docs match_lba %}Ladbrokes odds for away win.{% enddocs %} |
| psh                   | DOUBLE    | {% docs match_psh %}Pinnacle odds for home win.{% enddocs %} |
| psd                   | DOUBLE    | {% docs match_psd %}Pinnacle odds for draw.{% enddocs %} |
| psa                   | DOUBLE    | {% docs match_psa %}Pinnacle odds for away win.{% enddocs %} |
| whh                   | DOUBLE    | {% docs match_whh %}William Hill odds for home win.{% enddocs %} |
| whd                   | DOUBLE    | {% docs match_whd %}William Hill odds for draw.{% enddocs %} |
| wha                   | DOUBLE    | {% docs match_wha %}William Hill odds for away win.{% enddocs %} |
| sjh                   | DOUBLE    | {% docs match_sjh %}Stan James odds for home win.{% enddocs %} |
| sjd                   | DOUBLE    | {% docs match_sjd %}Stan James odds for draw.{% enddocs %} |
| sja                   | DOUBLE    | {% docs match_sja %}Stan James odds for away win.{% enddocs %} |
| vch                   | DOUBLE    | {% docs match_vch %}VC Bet odds for home win.{% enddocs %} |
| vcd                   | DOUBLE    | {% docs match_vcd %}VC Bet odds for draw.{% enddocs %} |
| vca                   | DOUBLE    | {% docs match_vca %}VC Bet odds for away win.{% enddocs %} |
| gbh                   | DOUBLE    | {% docs match_gbh %}Gamebookers odds for home win.{% enddocs %} |
| gbd                   | DOUBLE    | {% docs match_gbd %}Gamebookers odds for draw.{% enddocs %} |
| gba                   | DOUBLE    | {% docs match_gba %}Gamebookers odds for away win.{% enddocs %} |
| bsh                   | DOUBLE    | {% docs match_bsh %}Betsson odds for home win.{% enddocs %} |
| bsd                   | DOUBLE    | {% docs match_bsd %}Betsson odds for draw.{% enddocs %} |
| bsa                   | DOUBLE    | {% docs match_bsa %}Betsson odds for away win.{% enddocs %} |

---

### Table: `player`
{% docs eu_soccer_db_player %}
Contains information about individual players, including their names, identifiers, and physical attributes.
{% enddocs %}
| Column            | Data Type | Description |
|-------------------|-----------|-------------|
| id                | BIGINT    | {% docs player_id %}Primary key for the player table.{% enddocs %} |
| player_api_id     | BIGINT    | {% docs player_player_api_id %}Unique API identifier for the player.{% enddocs %} |
| player_name       | STRING    | {% docs player_player_name %}Full name of the player.{% enddocs %} |
| player_fifa_api_id| BIGINT    | {% docs player_player_fifa_api_id %}FIFA API identifier for the player.{% enddocs %} |
| birthday          | STRING    | {% docs player_birthday %}Date of birth of the player.{% enddocs %} |
| height            | DOUBLE    | {% docs player_height %}Height of the player in centimeters.{% enddocs %} |
| weight            | BIGINT    | {% docs player_weight %}Weight of the player in kilograms.{% enddocs %} |

---

### Table: `player_attributes`
{% docs eu_soccer_db_player_attributes %}
Contains detailed attributes for players, such as ratings, skills, and physical characteristics, for different dates.
{% enddocs %}
| Column                | Data Type | Description |
|-----------------------|-----------|-------------|
| id                    | BIGINT    | {% docs player_attributes_id %}Primary key for the player_attributes table.{% enddocs %} |
| player_fifa_api_id    | BIGINT    | {% docs player_attributes_player_fifa_api_id %}FIFA API identifier for the player.{% enddocs %} |
| player_api_id         | BIGINT    | {% docs player_attributes_player_api_id %}API identifier for the player.{% enddocs %} |
| date                  | STRING    | {% docs player_attributes_date %}Date when the attributes were recorded.{% enddocs %} |
| overall_rating        | DOUBLE    | {% docs player_attributes_overall_rating %}Overall rating of the player.{% enddocs %} |
| potential             | DOUBLE    | {% docs player_attributes_potential %}Potential rating of the player.{% enddocs %} |
| preferred_foot        | STRING    | {% docs player_attributes_preferred_foot %}Preferred foot (left or right).{% enddocs %} |
| attacking_work_rate   | STRING    | {% docs player_attributes_attacking_work_rate %}Attacking work rate.{% enddocs %} |
| defensive_work_rate   | STRING    | {% docs player_attributes_defensive_work_rate %}Defensive work rate.{% enddocs %} |
| crossing              | DOUBLE    | {% docs player_attributes_crossing %}Crossing skill rating.{% enddocs %} |
| finishing             | DOUBLE    | {% docs player_attributes_finishing %}Finishing skill rating.{% enddocs %} |
| heading_accuracy      | DOUBLE    | {% docs player_attributes_heading_accuracy %}Heading accuracy rating.{% enddocs %} |
| short_passing         | DOUBLE    | {% docs player_attributes_short_passing %}Short passing skill rating.{% enddocs %} |
| volleys               | DOUBLE    | {% docs player_attributes_volleys %}Volley skill rating.{% enddocs %} |
| dribbling             | DOUBLE    | {% docs player_attributes_dribbling %}Dribbling skill rating.{% enddocs %} |
| curve                 | DOUBLE    | {% docs player_attributes_curve %}Curve skill rating.{% enddocs %} |
| free_kick_accuracy    | DOUBLE    | {% docs player_attributes_free_kick_accuracy %}Free kick accuracy rating.{% enddocs %} |
| long_passing          | DOUBLE    | {% docs player_attributes_long_passing %}Long passing skill rating.{% enddocs %} |
| ball_control          | DOUBLE    | {% docs player_attributes_ball_control %}Ball control skill rating.{% enddocs %} |
| acceleration          | DOUBLE    | {% docs player_attributes_acceleration %}Acceleration rating.{% enddocs %} |
| sprint_speed          | DOUBLE    | {% docs player_attributes_sprint_speed %}Sprint speed rating.{% enddocs %} |
| agility               | DOUBLE    | {% docs player_attributes_agility %}Agility rating.{% enddocs %} |
| reactions             | DOUBLE    | {% docs player_attributes_reactions %}Reactions rating.{% enddocs %} |
| balance               | DOUBLE    | {% docs player_attributes_balance %}Balance rating.{% enddocs %} |
| shot_power            | DOUBLE    | {% docs player_attributes_shot_power %}Shot power rating.{% enddocs %} |
| jumping               | DOUBLE    | {% docs player_attributes_jumping %}Jumping rating.{% enddocs %} |
| stamina               | DOUBLE    | {% docs player_attributes_stamina %}Stamina rating.{% enddocs %} |
| strength              | DOUBLE    | {% docs player_attributes_strength %}Strength rating.{% enddocs %} |
| long_shots            | DOUBLE    | {% docs player_attributes_long_shots %}Long shots rating.{% enddocs %} |
| aggression            | DOUBLE    | {% docs player_attributes_aggression %}Aggression rating.{% enddocs %} |
| interceptions         | DOUBLE    | {% docs player_attributes_interceptions %}Interceptions rating.{% enddocs %} |
| positioning           | DOUBLE    | {% docs player_attributes_positioning %}Positioning rating.{% enddocs %} |
| vision                | DOUBLE    | {% docs player_attributes_vision %}Vision rating.{% enddocs %} |
| penalties             | DOUBLE    | {% docs player_attributes_penalties %}Penalties skill rating.{% enddocs %} |
| marking               | DOUBLE    | {% docs player_attributes_marking %}Marking skill rating.{% enddocs %} |
| standing_tackle       | DOUBLE    | {% docs player_attributes_standing_tackle %}Standing tackle skill rating.{% enddocs %} |
| sliding_tackle        | DOUBLE    | {% docs player_attributes_sliding_tackle %}Sliding tackle skill rating.{% enddocs %} |
| gk_diving             | DOUBLE    | {% docs player_attributes_gk_diving %}Goalkeeper diving rating.{% enddocs %} |
| gk_handling           | DOUBLE    | {% docs player_attributes_gk_handling %}Goalkeeper handling rating.{% enddocs %} |
| gk_kicking            | DOUBLE    | {% docs player_attributes_gk_kicking %}Goalkeeper kicking rating.{% enddocs %} |
| gk_positioning        | DOUBLE    | {% docs player_attributes_gk_positioning %}Goalkeeper positioning rating.{% enddocs %} |
| gk_reflexes           | DOUBLE    | {% docs player_attributes_gk_reflexes %}Goalkeeper reflexes rating.{% enddocs %} |

---

### Table: `team`
{% docs eu_soccer_db_team %}
Contains information about soccer teams, including their names and identifiers.
{% enddocs %}
| Column            | Data Type | Description |
|-------------------|-----------|-------------|
| id                | BIGINT    | {% docs team_id %}Primary key for the team table.{% enddocs %} |
| team_api_id       | BIGINT    | {% docs team_team_api_id %}API identifier for the team.{% enddocs %} |
| team_fifa_api_id  | DOUBLE    | {% docs team_team_fifa_api_id %}FIFA API identifier for the team.{% enddocs %} |
| team_long_name    | STRING    | {% docs team_team_long_name %}Full name of the team.{% enddocs %} |
| team_short_name   | STRING    | {% docs team_team_short_name %}Short name or abbreviation of the team.{% enddocs %} |

---

### Table: `team_attributes`
{% docs eu_soccer_db_team_attributes %}
Contains detailed attributes for teams, such as play style, aggression, and tactical ratings, for different dates.
{% enddocs %}
| Column                      | Data Type | Description |
|-----------------------------|-----------|-------------|
| id                          | BIGINT    | {% docs team_attributes_id %}Primary key for the team_attributes table.{% enddocs %} |
| team_fifa_api_id            | BIGINT    | {% docs team_attributes_team_fifa_api_id %}FIFA API identifier for the team.{% enddocs %} |
| team_api_id                 | BIGINT    | {% docs team_attributes_team_api_id %}API identifier for the team.{% enddocs %} |
| date                        | STRING    | {% docs team_attributes_date %}Date when the attributes were recorded.{% enddocs %} |
| buildupplayspeed            | BIGINT    | {% docs team_attributes_buildupplayspeed %}Speed of buildup play.{% enddocs %} |
| buildupplayspeedclass       | STRING    | {% docs team_attributes_buildupplayspeedclass %}Class of buildup play speed (e.g., slow, balanced, fast).{% enddocs %} |
| buildupplaydribbling        | DOUBLE    | {% docs team_attributes_buildupplaydribbling %}Dribbling skill in buildup play.{% enddocs %} |
| buildupplaydribblingclass   | STRING    | {% docs team_attributes_buildupplaydribblingclass %}Class of dribbling in buildup play.{% enddocs %} |
| buildupplaypassing          | BIGINT    | {% docs team_attributes_buildupplaypassing %}Passing skill in buildup play.{% enddocs %} |
| buildupplaypassingclass     | STRING    | {% docs team_attributes_buildupplaypassingclass %}Class of passing in buildup play.{% enddocs %} |
| buildupplaypositioningclass | STRING    | {% docs team_attributes_buildupplaypositioningclass %}Class of positioning in buildup play.{% enddocs %} |
| chancecreationpassing       | BIGINT    | {% docs team_attributes_chancecreationpassing %}Passing skill in chance creation.{% enddocs %} |
| chancecreationpassingclass  | STRING    | {% docs team_attributes_chancecreationpassingclass %}Class of passing in chance creation.{% enddocs %} |
| chancecreationcrossing      | BIGINT    | {% docs team_attributes_chancecreationcrossing %}Crossing skill in chance creation.{% enddocs %} |
| chancecreationcrossingclass | STRING    | {% docs team_attributes_chancecreationcrossingclass %}Class of crossing in chance creation.{% enddocs %} |
| chancecreationshooting      | BIGINT    | {% docs team_attributes_chancecreationshooting %}Shooting skill in chance creation.{% enddocs %} |
| chancecreationshootingclass | STRING    | {% docs team_attributes_chancecreationshootingclass %}Class of shooting in chance creation.{% enddocs %} |
| chancecreationpositioningclass | STRING | {% docs team_attributes_chancecreationpositioningclass %}Class of positioning in chance creation.{% enddocs %} |
| defencepressure             | BIGINT    | {% docs team_attributes_defencepressure %}Pressure applied in defense.{% enddocs %} |
| defencepressureclass        | STRING    | {% docs team_attributes_defencepressureclass %}Class of defensive pressure.{% enddocs %} |
| defenceaggression           | BIGINT    | {% docs team_attributes_defenceaggression %}Aggression in defense.{% enddocs %} |
| defenceaggressionclass      | STRING    | {% docs team_attributes_defenceaggressionclass %}Class of defensive aggression.{% enddocs %} |
| defenceteamwidth            | BIGINT    | {% docs team_attributes_defenceteamwidth %}Width of defensive team shape.{% enddocs %} |
| defenceteamwidthclass       | STRING    | {% docs team_attributes_defenceteamwidthclass %}Class of defensive team width.{% enddocs %} |
| defencedefenderlineclass    | STRING    | {% docs team_attributes_defencedefenderlineclass %}Class of defensive line (e.g., offside trap, deep line).{% enddocs %} |

---

> **Note:**
> All descriptions are now auto-filled and wrapped in Jinja `docs` blocks for dbt documentation integration.
