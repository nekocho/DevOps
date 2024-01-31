## Setting up EC2 Instance

1. Click on Launch instance from EC2 dashboard
2. Check in top right of screen near user details you are in correct region
3. Name server
4. Use Amazon Linux OS - Achitechture x64-bit Arm if using apple silicon
5. Select or create a new key pair name 
6. Edit network tab to ensure launch-wizard is unique
7. Leave everything else as default 
8. Launch Instance

Important to remember to change/edit inbound rules in the security tab once instance has launched.
Make sure to set custom TCP and change port number to match what's in your application

## Setting up Docker Repository

1. Login to Docker Hub
2. Go to Repository > Create Repository
3. Build docker image from local machine:

```
docker build -t <image name> .
```

4. Login to docker in terminal:

```
docker login
```

5. Push image to repository:

```
docker tag <image name> <docker username>/<repository name>

docker push <docker username>/<repository name>
```

## Moving Docker Image to EC2

1. Locate keypair.pem file on local machine - note down path to file
2. Secure keypair file:

```
chmod 400 <path>/keypair.pem
```

3. Connect to instance via SSH:

```
ssh -i <path>/keypair.pem ec2-user@<instance public DNS address>
```
Keep in mind, ec2-user is the default user set up when creating an instance on EC2, if this has changed, replace it!

4. Install docker to instance:

```
sudo yum update -y
sudo yum install docker -y
sudo usermod -aG docker ec2-user # allows user to use docker commands without sudo
sudo systemctl start docker # starts docker engine
```

5. Login to docker:

```
docker login 
```

6. Pull from docker repository and run:

```
docker pull <docker username>/<repository name>
docker run -p <host port>:<container port> <docker username>/<repository name>
```

If there are issues running docker commands, use sudo !! to rerun previous command with sudo
