FROM python:latest
WORKDIR /app
COPY . .
RUN pip install Flask pymssql
EXPOSE 5001
CMD ["python", "user_api.py"]
