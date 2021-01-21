import os

file = 'bitbucket-pipelines.yml'
{%- if cookiecutter.configure_bitbucket_pipeline == "y" -%}
    print('removing bitbucket pipeline')
    if os.path.isfile(file):
        os.remove(file)
{% endif %}
