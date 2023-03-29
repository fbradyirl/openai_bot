FROM python:3.10

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /app

# Copy only requirements into the container at /app
ADD requirements.txt /app

# Install any needed packages specified
RUN pip install -r requirements.txt

# Add all source files, etc. Do this now (after install pip modules) to take advantage of Docker layer caching...
ADD . /app

ARG VERSION
ENV VERSION $VERSION
LABEL "git-sha"=$VERSION
ARG BUILD_TIMESTAMP
ENV BUILD_TIMESTAMP $BUILD_TIMESTAMP
ARG USER
ENV BUILD_USER $USER

# Run app.py when the container launches
CMD ["python", "app.py"]

