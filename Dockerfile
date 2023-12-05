FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY requirments.txt .
COPY . .
RUN pip install -r requirments.txt


CMD ["flask", "run", "--host", "0.0.0.0"]