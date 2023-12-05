FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY requirments.txt .
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirments.txt


#CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]