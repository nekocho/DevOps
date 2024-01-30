FROM python:3
# Base image containing python 3 (to run python programs)

WORKDIR /usr/src/app
# Now our image's working directory is /usr/src/app

# Copy all current directory files (on the host) to the current directory (in the image)
COPY . . 
# Now our image contains source files

RUN pip install --no-cache-dir -r requirements.txt
# Now our image contains the flask library

EXPOSE 5000
# We need to expose 5000 because the Flask app is listening on 5000

CMD ["python", "main.py"]