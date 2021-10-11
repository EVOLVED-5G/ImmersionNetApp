resource "kubernetes_pod" "imm-netapp" {
  metadata {
    name = "imm-netapp"
    namespace = "evolved5g"
    labels = {
      app = "example"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/imm-netapp:latest"
      name  = "example-netapp"
    }
  }
}

resource "kubernetes_service" "imm-netapp_service" {
  metadata {
    name = "example-netapp-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.example.metadata.0.labels.app
    }
    port {
      port = 8080
      target_port = 8080
    }
  }
}
