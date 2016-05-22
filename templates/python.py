"""
Problem {{ id }}: {{ name }}

{{ description }}

{% if resources %}
This problem has the following references:
{% for resource in resources %}
{{ resource }}
{%- endfor -%}
{% endif %}

"""
