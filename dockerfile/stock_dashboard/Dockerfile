FROM python:3

WORKDIR /stock

COPY requirements.txt .

# install python3 and package
RUN  pip install -r requirements.txt

RUN mkdir stock_dashboard

COPY run.py .




