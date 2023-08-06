FROM python:3.8

# set a directory for the app
WORKDIR /app

# copy all the files to the container
COPY ./Flask_app/ .
RUN ls -la /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "flask_app.py"]

