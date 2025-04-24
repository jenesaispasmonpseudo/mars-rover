terraform {
    required_providers {
      docker = {
        source = "kreuzwerker/docker"
      }
    }
}
provider "docker" {}

resource "docker_image" "nginx" {
  name = "nginx:latest"
}
resource "docker_container" "web" {
  depends_on = [docker_network.mars_net]
  name = "mars-rover-web"
  image = docker_image.nginx.name
  ports {
    internal = 80
    external = 8080
  }
  networks_advanced {
    name = docker_network.mars_net.name
  }
}