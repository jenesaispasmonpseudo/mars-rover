resource "docker_container" "db" {
  depends_on = [docker_network.mars_net]
  name  = "mars-db"
  image = "mysql:8.0"
  env   = [ "MYSQL_ROOT_PASSWORD=${var.mysql_root_password}" ]

  networks_advanced {
    name = docker_network.mars_net.name
  }
}
