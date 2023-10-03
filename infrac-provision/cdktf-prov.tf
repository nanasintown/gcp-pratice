terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("credentials.json")

  project = "css-nhutcao-2023"
  region  = "europe-north1"
  zone    = "europe-north1-b"
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

variable "bucket_name" {
  type        = string
  description = ""
}

variable "folder_name" {
  type        = string
  description = ""
}

resource "google_storage_bucket" "storage_bucket" {
  name                        = var.bucket_name
  project                     = "css-nhutcao-2023"
  location                    = "EU"
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket_object" "my_folder" {
  name    = var.folder_name
  content = "Folder for testing"
  bucket  = google_storage_bucket.storage_bucket.name
}