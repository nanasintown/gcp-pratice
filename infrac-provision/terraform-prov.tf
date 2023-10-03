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
  region  = "europe-central2"
  zone    = "europe-central2-b"
}

variable "vm_name_input" {
    type = string
    description = ""
}

output "public_ip" {
  value = google_compute_instance.vm_instance.network_interface.0.access_config.0.nat_ip 
}

output "vm_name" {
  value = google_compute_instance.vm_instance.name
}

resource "google_compute_address" "static" {
  name = "public-static-ip"
}


resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

resource "google_compute_firewall" "allow-http" {
  name    = "allow-http-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "vm_instance" {
  name         = var.vm_name_input
  machine_type = "f1-micro"
  tags = ["http-server"]

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y apache2
  EOF

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  labels = {
    "course" = "css-gcp"
  }
  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
    }
}
