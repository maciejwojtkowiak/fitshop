FROM python:3

RUN adduser --system --no-create-home django

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH /code



EXPOSE 8000
USER django

CMD ["./main.py"]