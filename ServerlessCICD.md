# Serverless CI-CD

To set up a serverless CI-CD, create an index.html page for a static website, create an S3 bucket and use AWS lambda and API gateway to call a lambda function to change this from a static to a dynamic website.

## Setting up an S3 bucket

1. Create an S3 bucket:
    - Can create files (Objects)
    - Doesn't work by region
2. On bucket page, go to permissions
3. Disable "Block all public access"
4. Edit "Bucket policy" using a policy document:
    - Add new statement
    - Search for S3 and select all actions
    - For principal replace {} with "*"
    - In resources replace [] with "arn:aws:s3:::BUCKET_NAME/*"
    - For action, change to s3:GetObject
    - Bucket policy does the following:
        - JSON file
        - Changes who can OR cannot access or do certain things
        - Lists what resources needed in specific AWS services
        - Specifies conditions
    - Bucket policy should look like this:

    ```
    {
    "Version": "2012-10-17",
    "Statement": [
            {
                "Sid": "Statement1",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::BUCKET_NAME/*"
            }
        ]
    }
    ```

5. Go to properties tab and at bottom, enable static website hosting
6. You now have access to "Bucket Website Endpoint", this will be the link to access the webpage
7. There will be a 404 error unless an index.html has been uploaded

## Setting up Jenkins

1. Using the CloudFormation template provided, edit this to show your S3 bucket name, Template found here: 
    https://github.com/makersacademy/serverless-cicd/blob/main/resources/deploy_ec2_network_v1.json
    - Save this as a CloudFormation JSON configuration file - can be called anything
2. Create a new EC2 keypair 
3. Go to CloudFormation and create a new stack with new resources
    - Leave template as template is ready
    - Select Upload a template and upload the saved JSON file in step one
    - Put any stack name
    - InstanceType: t2.micro
    - KeyPair: Choose the keypair created in step two
    - Leave next page as is and create stack
    - Stack creation will take a few minutes
4. In the outputs, find the InstanceDns record to see the hostname of your new server.
5. The configuration file should have installed jenkins, to access go to 
```
http://YOUR_INSTANCE_DNS_VALUE:8080/
```
Instance DNS can be found under Outputs tab on CloudFormation

6. You should see an Unlock Jenkins page
7. SSH into your instance DNS:

```
chmod 400 <path to keypair file>
ssh -i <path to keypair file> ec2-user@<InstanceDNS>
```
8. To get the JENKINS admin password use the following command in SSH:

```
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
9. Copy and paste the key provided into the Admin password field on the Unlock Jenkins page
10. Click on Install suggested Plugins
11. Create a User account and password

## Creating a pipeline

1. Create a git repository with your static website, e.g. index.html
2. Optionally, copy and paste files from here:
https://github.com/makersacademy/serverless-cicd/tree/main/template
3. Important files needed are index.html and package.JSON
4. Create a new pipeline on Jenkins
5. Add a pipeline script to configure:
    - Clones repository
    - Set up NodeJS to run checks
    - Install NodeJS dependencies
    - Run checks using npm run check
    - Deploy to S3 ONLY if everything passes

    Use this link for the template of the pipeline script:
    https://github.com/makersacademy/serverless-cicd/blob/main/03_set_up_pipeline.md#resources

6. Adding github credentials to Jenkins:
    - On JENKINS: Manage Jenkins > Credentials > Global > Add credentials 
    - Select Username and Password
    - Fill in Username (github user) and id field (can be anything), DON'T add password
    - On GITHUB: Settings > Developer settings > Personal access tokens > Fine grained tokens > Generate
    - Give access to the following:
        - Commit statuses: Read & Write
        - Contents: Read Only
        - Metadata: Read Only
    - Put generated token into password field on JENKINS in credentials created
    - Copy ID of credentials and paste into Pipeline script
7. In terminal, SSH into your webserver using the keypair and the publicDNS link from Cloudformation (under Outputs tab)

```
chmod 400 <path to keypair file>
ssh -i <path to keypair file> ec2-user@<DNS link>
```

8. Install git onto the instance using ssh

```
sudo yum install git
```

9. Run the pipeline
10. If any failures, click on the number of the build and go to console logs, towards the bottom, there will be error messages
11. If git is installed correctly and package.json has correct dependencies, first two should pass
12. If HTML fails, this is to do with either whitespaces or incorrect HTML
13. Deployment will fail as AWS credentials have not been added:
    - In AWS, go to IAM and create a new User Group
    - Add permissions to the group directly by going to Permissions > Add Permissions > Create Inline policy
    - Copy and paste the User group policy here: https://github.com/makersacademy/serverless-cicd/blob/main/03_set_up_pipeline.md#resources
    - After, add or create a user to add to the group
    - Open the user account and go to Security Credentials > Access Keys > Create access key > Other > Next
    - Copy Access key and Secret Access key
    - On Jenkins: Dashboard > Manage Jenkins > Plugins > Available Plugins > Install AWS Credentials
    - Create new crentials using AWS Credentials instead of Username and password and create an ID
    - Copy and paste AWS credential ID into Pipeline script and change Bucket name to S3 bucket name
14. Run build
15. If passes, set up a webhook to Github:
    - On Github, go to Repository > Settings > Webhooks > Add Webhook 
    - For Payload URL, use CloudFormation PublicDNS link with port number and /github-webhook/ added to the end 
    e.g
    ```
    <Cloud formation DNS link>:8080/github-webhook/
    ```
    - Set content type to application/json
    - Set it so that the webhook has both pull and push request access
    - Create webhook
    - On Jenkins: Pipeline > configuration > select GitHub hook trigger for GITScm polling under Build triggers

## Setting up Lambda Function and API gateway

1. Create a lambda function
    - Under runtime, set it as python
    - Select correct Architecture: arm64 for silicon mac
2. Copy the function here: https://github.com/makersacademy/serverless-cicd/blob/main/resources/your-first-lambda.py
3. Deploy Lambda function
    - If any changes made, needs to be deployed each time
4. Test Lambda function
5. Create an API gateway:
    - Choose HTTP API 
    - Choose Lambda for integration
    - Choose the created lambda function from dropdown menu
    - Choose GET method and path can be same as function name
    - Keep stage to default and ensure auto-deploy is on
    - Then review and create
6. Function is now accessible via the API main page under stages, this will show the default link, to access function, add route path to end of link or leave it as / if no path name specified
7. Set up CORS (Cross-Origin Resource Sharing):
    - On the left menu bar go to CORS under develop
    - Under Access-Control-Allow-Origin add S3 bucket link
    - Under Access-Control-Allow-Methods choose GET
    - Under Access-Control-Allow-Headers type in 'content-type'
    - Click save
8. Update the Lambda function in the index.html file by using the Lambda function url + route path
9. Push changes to git, wait for the build to complete on Jenkins and function should work on webpage


