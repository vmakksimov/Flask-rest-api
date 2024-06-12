FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:myapp"]
#CMD ["/bin/bash", "docker-entrypoint.sh"]
# Copy the entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["/app/docker-entrypoint.sh"]


