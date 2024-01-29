# Start your image
FROM python:3.9

# Locate directory that 
WORKDIR /first_task

# Copy essential files from directory
COPY app.py .
COPY templates/index.html templates/ 
# Needs

# Install Flask
RUN pip install Flask

# Port number - needs to match flask
EXPOSE 3000

# Start the app using python commands
CMD [ "python", "app.py" ]
