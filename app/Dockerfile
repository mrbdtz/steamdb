FROM python:3.11-slim-bookworm
WORKDIR /usr/src/app
COPY . .
#RUN pip install --no-cache-dir dash gunicorn psycopg2-binary
RUN pip install -r requirements.txt
EXPOSE 5000
ENV HOST_MACHINE_ADDRESS=host.docker.internal
#ENV FLASK_APP=app.py
#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:server", "--workers=3"] 
#, "--threads=2"]