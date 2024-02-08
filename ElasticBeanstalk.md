# Elastic Beanstalk

## Creating an Elastic Beanstalk environment

1. On AWS go to ElasticBeanstalk via services or search
2. Go to environment and create an environment
3. Choose Webserver env:
    - Provide a name for the app and env
    - Choose Docker platform
    - Select the EC2 keypair created previously when creating an EC2 instance
    - Use default VPC
    - Select Activated in Public IP address and select all instnace subnets
    - Ensure architechture is set correctly e.g. ARM for silicon mac
    - Optional to skip monitoring/loggin
4. Submit and create environment, this will take a few minutes

## Creating a dockerrun.aws.json file

Things needed in a dockerrun json file:

    - Version of ElasticBeanstalk
    - Port Mapping
    - Image name from Docker repository
    - Needs 'update' set to 'true'

Example JSON file:

```
{
    "AWSEBDockerrunVersion": "1",
    "Image": {
        "Name": "<docker username>/<docker repo_name>,
        "Update": "true"
    },
    "Ports":[
        {
            "containerPort": 80
        }
    ],
}
```

## Deployment

1. On environment page, click on upload and deploy
2. Select ONLY the dockerrun.aws.json file
3. Once uploaded, this takes a few minutes to run
4. If you want to check logs, go to:
    - Logs tab
    - Request logs
    - Download zip file
    - Each log in the file relates to different parts of EB
    - Eb-engine.log will have logs of activity
5. Once deployed, you can see the web app is up and running using the publicDNS IP