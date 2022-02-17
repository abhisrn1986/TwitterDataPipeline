FROM python:3.8
WORKDIR /etl
COPY requirements.txt /etl
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "etl.py"]