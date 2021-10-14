FROM python:3


ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH /code



EXPOSE 8000

CMD ["./main.py"]