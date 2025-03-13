FROM python:3.12.3

WORKDIR /app
COPY . .

ENV PYTHONUNBUFFERED=1
RUN --mount=type=cache,target=/root/.cache pip3 install -r requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
WORKDIR /app/booking_service

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]