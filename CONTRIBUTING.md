#CONTRIBUTING

## HOW TO RUN THE DOCKERFILE LOCKALLY

````
docker run -dp 5000:5000 -w /app -v "/d/vm/Python/Flask1:/app" flask-rest-api sh -c "flask run --host 0.0.0.0"
#CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
In docker compose in app: command: gunicorn -w 4 -b 0.0.0.0:5000 app:myapp
````
