FROM python:3.9.16

WORKDIR /collaborative

COPY ./requirements.txt /collaborative/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /collaborative/requirements.txt

COPY . /collaborative/

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5501" ]