terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.56.0"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

# New server
resource "hcloud_server" "deepseek" {
  name        = "deepseek"
  server_type = "cx33"
  image       = "ubuntu-22.04"
  location    = "nbg1"

  # izmanto jau esošu SSH key Hetzner panelī
  ssh_keys = ["Edijs"]

  labels = {
    project = "deepseek"
    env     = "prod"
  }

  user_data = templatefile("cloud-init/deepseek.yml", {
    ssh_user       = var.ssh_user
    ssh_public_key = file(var.ssh_public_key)
  })
}

resource "hcloud_firewall" "deepseek" {
  name = "deepseek-fw"

  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "22"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
    description = "SSH access"
  }
}

resource "hcloud_firewall_attachment" "deepseek" {
  firewall_id = hcloud_firewall.deepseek.id
  server_ids  = [hcloud_server.deepseek.id]
}