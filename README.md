# Kubernetes-Utilities

1. `create_from_json.py` is a utility to create any object of kubernetes using its json file. Currently, kubernetes client has different functions to create different objects like to create deployment (create_namespaced_deployment) and to create statefulset (create_namespaced_statefulset), all those selecting appropriate API and calling appropriate function is handled by the utility.

TO DO: Currently it doesn't support multiple kubernetes objects in same json file.
