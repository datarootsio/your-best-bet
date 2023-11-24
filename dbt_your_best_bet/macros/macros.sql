{% macro to_sql_list(listlist) %}
    ({% for x in listlist -%}
        '{{ x }}' {%- if not loop.last -%}
            {{ "," }}
        {%- endif -%}
    {%- endfor %})
{% endmacro %}
