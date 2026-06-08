variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "backend_image" {
  type = string
}

variable "frontend_image" {
  type = string
}
