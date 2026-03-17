FROM apache/airflow:2.7.1
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
# Install necessary Python packages for GCP and dbt
RUN pip install --no-cache-dir \
    google-cloud-storage \
    google-cloud-bigquery \
    dbt-bigquery \
    pandas
