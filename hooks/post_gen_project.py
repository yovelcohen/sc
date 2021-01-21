import os

use_bit_bucket_pipeline = '{{cookiecutter.configure_bitbucket_pipeline}}'.lower()

if use_bit_bucket_pipeline == 'n':
    pass

file = "{{cookiecutter.project_name}}/bitbucket-pipelines.yml"
if os.path.exists(file):
    os.remove(file)

os.system('pip install -r requirements.txt')
