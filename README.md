# Kubernetes-Utility

1. `create_from_json.py` is a utility to create any object of kubernetes using its json file. Currently, kubernetes client has different functions to create different objects like to create deployment (create_namespaced_deployment) and to create statefulset (create_namespaced_statefulset), all those selecting appropriate API and calling appropriate function is handled by the utility.

TO DO: Currently it doesn't support multiple kubernetes objects in same json file.

2. `kubectl_cp_as_python_client` is a utility to copy a file inside the pod and copy a file from the pod to host. You can provide the pod_name to/from you want to copy the file, src_path source path of file you want to copy and dest_path destination path of folder you want to copy it to.

TODO: Currently, it doesn't support the copying of entire folder from/to the pod. This functionality is yet to be added.
