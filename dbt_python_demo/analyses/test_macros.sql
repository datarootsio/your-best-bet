{{ codegen.generate_source(
    schema_name = "european_soccer_db",
    table_names = ["match", "player", "player_attributes", "team", "team_attributes"],
    generate_columns = True,
    include_descriptions = True,
    include_data_types = True,
    name = "european_soccer_db",
    include_schema = True
) }}
