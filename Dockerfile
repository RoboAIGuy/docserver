# set python version
FROM python:3.9

# set working directory
WORKDIR /reelblend

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy to docker cache
COPY ./requirements.txt /reelblend/requirements.txt

# install all requirements
RUN pip install --no-cache-dir --upgrade -r /reelblend/requirements.txt

# copy codebase to working directory
COPY ./app /reelblend/app
COPY ./templates /reelblend/templates

# ENV PYTHONPATH = /code

# run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
