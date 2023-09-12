terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "~> 4.51.0"
        }
    }
}

provider "google" {
  credentials = file("google.json")
  project = "pypet-k8"
  region = "me-west1"
  zone = "me-west1-c"
}

resource "google_container_cluster" "primary" {
    name = "gke-cluster-pypet"
    remove_default_node_pool = true
    initial_node_count = 1

    master_auth {
      client_certificate_config {
        issue_client_certificate = false 
      }
    }

    node_config {
      service_account = "pypet-admin@pypet-k8.iam.gserviceaccount.com"
    }
}

resource "google_container_node_pool" "primary_nodes" {
    name = "gke-node-pypet"
    cluster = google_container_cluster.primary.name
    node_count = 1

    node_config {
      preemptible = true
      machine_type = "e2-medium"
      service_account = "pypet-admin@pypet-k8.iam.gserviceaccount.com"
      oauth_scopes = [
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
      ]
    } 
}