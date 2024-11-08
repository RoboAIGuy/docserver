# set python version
FROM python:3.9

# set working directory
WORKDIR /docserver

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy to docker cache
COPY ./requirements.txt /docserver/requirements.txt

# install all requirements
RUN pip install --no-cache-dir --upgrade -r /docserver/requirements.txt

# copy codebase to working directory
COPY ./app /docserver/app

# ENV PYTHONPATH = /code

# run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
