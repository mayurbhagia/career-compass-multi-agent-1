python3 -m venv venv
source venv/bin/activate
pip install nova-act

nano ~/.aws/config
nano ~/.aws/credentials

Create bucket
aws s3 mb s3://my-nova-act-workflows-11jan25m --region us-east-1

Copy the workflow definition to bucket:
aws s3 cp workflow_definition.yaml s3://my-nova-act-workflows-11jan25m/bicycle-search/
then goto console and create a workflow with name mentioned in workflow_definition.yaml

python bicycle_search.py
