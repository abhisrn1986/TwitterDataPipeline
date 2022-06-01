FROM python:3.9
WORKDIR /etl
COPY requirements.txt /etl
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["streamlit", "run", "etl.py"]
