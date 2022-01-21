
# Sprint 5: API Functional and Security testing via containerized test clients deployed on AWS ECS
## Table of Contents

1. [Project Description](#Project-Description)
2. [AWS Services Used](#AWS-Services-Used)
3. [Instructions](#Instructions)
4. [Author](#Author)

## Project Description

Using a static React Web App, display the list of URLs supporting pagination of items. The front-end web app should be able to continuously deploy (CD) and it should provide a way to authenticate users via AWS Cognito. Successfully implemented the web app while incorporating the functionality from previous sprint.

## AWS Services Used

1. AWS ECS
2. AWS ECR
3. AWS API Gateway
4. AWS Pipeline
5. AWS Events
6. AWS Fargate
7. Docker
8. PyRestTest
9. Syntribos


## Instructions:

To get this repo up and running follow these steps:

1. cd to your desired folder and run this command in terminal
	
	    git clone https://github.com/Sikandar-Bakht/ProximaCentauri.git

2. cd to the project directory using this command:

	   cd ./ProximaCentauri/Sikandar_Bakht/sprint5/SprintFiveProj

3. (Optional) Bootstrap the environment by running the following command.

		cdk bootstrap --qualifier "sikandars5" --toolkit-stack-name "sikandartoolkit" --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess 315997497220/us-east-1
  
    The `qualifier` and `toolkit-stack-name` are variable parameters, you can change them to whatever you like. If you change qualifier name, change the same in `cdk.json` file
    in the project directory as well.

4. In the `./SprintThreeProj` directory, run the following command in terminal:
    
       cdk deploy sikandarpipeline
       
5. Manually approve the prod stage in CodePipeline
       
6. The pipeline is created and two stacks by names starting with 'beta' and 'prod' are created. 
7. Select first one, go to stages in the left hand menu and copy the URL endpoint displayed.

## Author

Sikandar Bakht

For queries, reach out to me at:
sikandar.bakht.s@skipq.org


To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
