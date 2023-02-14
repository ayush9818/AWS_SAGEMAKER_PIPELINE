
# Sagemaker MLOps Pipeline

An end to end pipeline for labeling, training and deployment of an object detection model.

![image](https://user-images.githubusercontent.com/43469729/218812586-bc4acd09-c1c0-481a-b297-aca228b35828.png)
## Installation

Cloning the repository and setting up virtual environment

```bash
  git clone https://github.com/ayush9818/AWS-MLops-Pipeline
  cd AWS-MLops-Pipeline
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
    
## Features

- Labelling Objects using Sagemaker Ground Truth
- Custom Training Jobs on Sagemaker
- Deployment of custom models using Real Time Endpoint on Sagemaker
- Inference using Real Time Endpoint


## Run Locally
<details>
  <summary>Click me</summary>
  
  ### Labelling Job

  - Upload the Labelling Template [Link](https://github.com/ayush9818/AWS-MLops-Pipeline/blob/main/labelling/configs/instructions.template) on s3 

  - Update the config : [Link](https://github.com/ayush9818/AWS-MLops-Pipeline/blob/main/labelling/configs/labelling_config.json). Config parameters reference : [Link](https://github.com/ayush9818/AWS-MLops-Pipeline/wiki/Sagemaker-Labelling-Jobs#parameters-description-) 
  - To create a labelling job, run the following commands

    ```bash
      cd labelling
      python create_labelling_job.py --cfg configs/labelling_config.json
    ```
  - Now worker will be assigned a labelling job, once the worker complete the task, an output.manifest file will be written on s3 which will be used for model training.
  ----

  ### Training Job 

  #### Building Training Container Image in local
  - Use GPU base image to enable GPU support.
  ```bash
    cd training
    docker build -f Dockerfiles/AwsCPUDockerfile -t <image_name> .
  ```
  #### Pushing the image to ECR
  - Need to add ECR FullAccessRole Policy in Sagemaker IAM Role
  - Login into ECR repo using commands on ECR UI 
  - To tag and push the image, run the following commands 
  ```bash
    docker tag <image_name> <ecr_repo_uri>:<tag_name>
    docker push <ecr_repo_uri>:<tag_name>
  ```

  #### Creating a Training Job on  Sagemaker

  - Prepare a Job Config : [Link](https://github.com/ayush9818/AWS-MLops-Pipeline/blob/main/configs/job_config.json). Parameters Reference : Link
  - Prepare a Train Config : [Link](https://github.com/ayush9818/AWS-MLops-Pipeline/blob/main/data/config.json). Parameters Reference : Link
  - To create a training job, run the following commands
  ```bash
    cd AWS-MLops-Pipeline
    python create_training_job.py --cfg configs/job_config.json
  ```
  ----

  ### Endpoint Deployment
  #### Building Inference Container Image in local
  - Use GPU base image to enable GPU support.
  ```bash
    cd inference
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com
    docker build -f Dockerfiles/CpuDockerfile -t <image_name> .
  ```
  #### Pushing the image to ECR
  - Need to add ECR FullAccessRole Policy in Sagemaker IAM Role
  - Login into ECR repo using commands on ECR UI 
  - To tag and push the image, run the following commands 
  ```bash
    docker tag <image_name> <ecr_repo_uri>:<tag_name>
    docker push <ecr_repo_uri>:<tag_name>
  ```

  #### Creating a Real Time Endpoint
  - Prepare an endpoint config : [Link](https://github.com/ayush9818/AWS-MLops-Pipeline/blob/main/configs/endpoint_config.json). Parameters Reference : Link
  - To create an inference endpoint, run the following commands
  ```bash
    cd AWS-MLops-Pipeline
    python inference_resources.py --cfg configs/endpoint_config.json --action create_endpoint
  ```

  #### Deleting the Endpoint Resources 
  ```bash
    python inference_resources.py --cfg configs/endpoint_config.json --action delete_endpoint
  ```
  ----
  ### Model Inference 
  - Create a inference config : [Link](https://github.com/ayush9818/AWS-MLops-Pipeline/blob/main/configs/inference_config.json). Parameters Reference : Link
  ```bash
    cd AWS-MLops-Pipeline
    python invoke_endpoint.py --cfg configs/inference_config.json
  ```
</details>

## Authors

- [Ayush Agarwal](https://www.github.com/ayush9818)

