FROM python:3.14-slim
WORKDIR /code
COPY services/catalog/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "services.catalog.main:app", "--host", "0.0.0.0", "--port", "8000"]