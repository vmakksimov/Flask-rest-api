FROM python:3.12
EXPOSE 80
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:myapp"]

