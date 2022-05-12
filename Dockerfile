FROM python:3.9
# requirments
# create the app user

WORKDIR /

# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application (e.g. django logs)
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1
ENV CONFIG_TYPE prod
ENV TESTING false

# Copy app source codes
COPY src/ ./src/
COPY requirements.txt ./requirements.txt

# Install python packages using requirements.txt file
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/src
EXPOSE 80/tcp

# Start Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]