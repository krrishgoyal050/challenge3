terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.35"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "carbon-platform"
  format        = "DOCKER"
}

resource "google_sql_database_instance" "postgres" {
  name             = "carbon-postgres"
  database_version = "POSTGRES_16"
  region           = var.region
  settings {
    tier              = "db-f1-micro"
    availability_type = "ZONAL"
    backup_configuration {
      enabled = true
    }
  }
  deletion_protection = true
}

resource "google_sql_database" "database" {
  name     = "carbon"
  instance = google_sql_database_instance.postgres.name
}

resource "google_secret_manager_secret" "jwt_secret" {
  secret_id = "carbon-jwt-secret"
  replication {
    auto {}
  }
}

resource "google_cloud_run_v2_service" "backend" {
  name     = "carbon-backend"
  location = var.region
  template {
    containers {
      image = var.backend_image
      ports {
        container_port = 8000
      }
      env {
        name  = "ENVIRONMENT"
        value = "production"
      }
    }
  }
}

resource "google_cloud_run_v2_service" "frontend" {
  name     = "carbon-frontend"
  location = var.region
  template {
    containers {
      image = var.frontend_image
      ports {
        container_port = 3000
      }
    }
  }
}
