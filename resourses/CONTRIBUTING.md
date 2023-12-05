#CONTRIBUTING

## HOW TO RUN THE DOCKERFILE LOCKALLY

````
docker run -dp 5000:5000 -w /app -v "/d/vm/Python/Flask1:/app" flask-rest-api sh -c "flask run --host 0.0.0.0"
#CMD ["flask", "run", "--host", "0.0.0.0"]
````