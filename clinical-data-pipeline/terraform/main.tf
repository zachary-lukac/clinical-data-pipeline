terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project     = "<YOUR_GCP_PROJECT_ID>"
  region      = "europe-west2" # London region - good for UK compliance!
  credentials = file("./credentials.json")
}

# 1. Data Lake: Google Cloud Storage Bucket for raw Synthea JSONs
resource "google_storage_bucket" "clinical_data_lake" {
  name          = "<YOUR_UNIQUE_BUCKET_NAME>_clinical_lake"
  location      = "europe-west2"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# 2. Data Warehouse: BigQuery Dataset for OMOP CDM
resource "google_bigquery_dataset" "omop_dataset" {
  dataset_id                  = "omop_cdm_v5"
  friendly_name               = "OMOP Common Data Model"
  description                 = "Standardized clinical data warehouse"
  location                    = "europe-west2"
  delete_contents_on_destroy  = true
}
