
{% macro set_null(column_name) %}
    nullif({{ column_name }}, -9999.9)
{% endmacro %}
