# Start your base image using via standard Linux distribution
# Python 3.9 is larger in size, more pre-isntalled utilities
# Python:3-alpine3.15 is smaller in size and based on Alpine Linux 
#        - suitable for resource constrained environments
FROM python:3.9

# Image working directory
WORKDIR /app

# Copy essential files from directory
# COPY . . = Copy ALL files in current directory (on host) to current directory in image

# COPY app.py . --> Copy app.py file from workdir
# COPY templates/index.html /templates --> Copy index.html from /templates folder
# COPY static/uploads /static --> Copy uploads folder from /static folder
COPY . .

# Install Flask
RUN pip install Flask


# Port number - needs to match flask
EXPOSE 3000

# Start the app using python commands
CMD [ "python", "app.py" ]
