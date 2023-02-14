import json
import os
import argparse
import boto3
import time

sm_client = boto3.client(service_name="sagemaker", region_name="ap-southeast-1")

def create_model(model_name, ecr_image, model_uri, role):
    container = {
              'Image':        ecr_image,
              'ModelDataUrl': model_uri,
              'Mode':         'SingleModel'
            }
    response = sm_client.create_model(
              ModelName        = model_name,
              ExecutionRoleArn = role,
              Containers       = [container],
              )
    print("{} Model Created".format(model_name))
    
def create_config(model_name, config_name, instance_type,instance_count):
    response = sm_client.create_endpoint_config(
                EndpointConfigName = config_name,
                ProductionVariants=[
                     {
                        'InstanceType':        instance_type,
                        'InitialInstanceCount': instance_count,
                        'InitialVariantWeight': 1,
                        'ModelName':            model_name,
                        'VariantName':          'Variant1'
                      }
                ]
           )
    print("{} Config Created".format(config_name))
    
def create_endpoint(endpoint_name, config_name):
    response = sm_client.create_endpoint(
              EndpointName       = endpoint_name,
              EndpointConfigName = config_name
              )
    
    print("Endpoint Name : {}".format(endpoint_name))
    start=time.time()
    waiter = boto3.client('sagemaker', region_name='ap-southeast-1').get_waiter('endpoint_in_service')
    print("Waiting for endpoint to create...")
    waiter.wait(EndpointName=endpoint_name)
    resp = sm_client.describe_endpoint(EndpointName=endpoint_name)
    print("Endpoint Status: {}".format(resp['EndpointStatus']))
    print("Endpoint Creation Time : {}".format(time.time()-start))
    
def delete_resources(endpoint_name, config_name, model_name, aws_region):
    sagemaker_client = boto3.client('sagemaker', region_name=aws_region)
    try:
        sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
        print(f"Endpoint Deleted : {endpoint_name}")
    except Exception as e:
        print(e)
    
    try:
        sagemaker_client.delete_endpoint_config(EndpointConfigName=config_name)
        print(f"Endpoint Configuration Deleted : {config_name}")
    except Exception as e:
        print(e)
    
    try:
        sagemaker_client.delete_model(ModelName=model_name)
        print(f"Endpoint Configuration Deleted : {model_name}")
    except Exception as e:
        print(e)
    
    

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", type=str, help='endpoint configuration file path')
    parser.add_argument("--action", type=str, help='Supported Actions : create_endpoint, delete_endpoint')
    args = parser.parse_args()
    
    config_path = args.cfg
    action = args.action
    
    assert action in ['delete_endpoint', 'create_endpoint'], f"Supported Actions are : create_endpoint and delete_endpoint"
    assert os.path.exists(config_path), f"{config_path} does not exist"
    
    endpoint_config = json.load(open(config_path))
    
    if action == "create_endpoint":
        create_model(model_name=endpoint_config.get('model_name'),
             ecr_image=endpoint_config.get('container_uri'),
             model_uri=endpoint_config.get('model_uri'),
             role=endpoint_config.get('iam_role'))
        create_config(model_name=endpoint_config.get('model_name'),
              config_name=endpoint_config.get('config_name'),
              instance_type=endpoint_config.get('instance_type'),
              instance_count=endpoint_config.get('instance_count'))
        
        create_endpoint(endpoint_name=endpoint_config.get('endpoint_name'),
                config_name=endpoint_config.get('config_name'))
    
    if action == "delete_endpoint":
        delete_resources(endpoint_name=endpoint_config.get('endpoint_name'),
                 config_name=endpoint_config.get('config_name'),
                 model_name=endpoint_config.get('model_name'),
                 aws_region=endpoint_config.get('region'))

