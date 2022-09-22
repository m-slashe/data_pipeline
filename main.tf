provider "google" {
    project = "sbx-186706-sustjadesb-89460529"
    region = "us-east1"
 }

resource "google_storage_bucket" "templates_bucket" {
  name          = "templatesteste"
  location      = "us-east1"
  uniform_bucket_level_access = true
  force_destroy = true
}

# resource "google_storage_bucket_object" "dag_test" {
#   name   = "src/dag.py"
#   source = "./src/dag.py"
#   bucket = "${google_storage_bucket.templates_bucket.name}"
# }

# resource "google_storage_bucket_object" "dag_metadata_test" {
#   name   = "src/dag.py_metadata"
#   source = "./src/dag.py_metadata"
#   bucket = "${google_storage_bucket.templates_bucket.name}"
# }

resource "google_pubsub_topic" "test_topic" {
  name = "test_topic"
}

resource "google_cloud_scheduler_job" "test_scheduler" {
  name        = "test_scheduler"
  schedule    = "* * * * *"

  pubsub_target {
    topic_name = google_pubsub_topic.test_topic.id
    data       = base64encode("{ \"text\": \"seila\", \"value\": \"seila\" }")
  }
}

resource "google_pubsub_subscription" "test_subscription" {
  name  = "test_subscription"
  topic = "${google_pubsub_topic.test_topic.name}"

  ack_deadline_seconds = 20
}

resource "google_bigquery_dataset" "test_dataset" {
  dataset_id                  = "test_dataset"
  friendly_name               = "test"
  description                 = "This is a test description"
}

locals {
  dag_template = "${google_storage_bucket.templates_bucket.url}/src/dag_template"
}

resource "google_dataflow_job" "dag_job" {
  name              = "dag_job"
  template_gcs_path = "${local.dag_template}"
  temp_gcs_location = "${google_storage_bucket.templates_bucket.url}/tmp_dir"
  max_workers = 1
  network = "acn-cio-project-vpc"
  subnetwork = "regions/us-east1/subnetworks/us-east1-public-subnet"
  parameters = {
    subscription_name = "${google_pubsub_topic.test_topic.id}"
    table_spec = "${google_bigquery_dataset.test_dataset.id}.table_test"
  }  
  on_delete = "cancel"
}

