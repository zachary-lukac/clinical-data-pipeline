from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from google.cloud import storage

# TODO: Add your bucket name
BUCKET_NAME = "<YOUR_UNIQUE_BUCKET_NAME>_clinical_lake"

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Assuming GOOGLE_APPLICATION_CREDENTIALS is set in the Airflow environment
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

default_args = {
    'owner': 'health_data_engineer',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'synthea_daily_ingestion',
    default_args=default_args,
    description='A simple DAG to ingest Synthea data to GCS',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # In a real scenario, this task would run the Synthea Java generator
    # For now, we simulate uploading a pre-generated file
    upload_task = PythonOperator(
        task_id='upload_patients_to_gcs',
        python_callable=upload_to_gcs,
        op_kwargs={
            'bucket_name': BUCKET_NAME,
            'source_file_name': '/opt/airflow/data/patients.csv', # Local path in container
            'destination_blob_name': f'raw/patients_{datetime.now().strftime("%Y%m%d")}.csv'
        },
    )

    upload_task
