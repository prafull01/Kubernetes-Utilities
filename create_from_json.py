import re
from os import path
import json
from kubernetes import client, config
from kubernetes.client.rest import ApiException


def create_from_json(json_file):
    """

    :param json_file:
    :return:
    """

    with open(path.abspath(json_file)) as f:
        json_object = json.load(f)

        group, _, version = json_object["apiVersion"].partition("/")
        if version == "":
            version = group
            group = "core"

        group = "".join(group.split(".k8s.io,1"))
        func_to_call = "{0}{1}Api".format(group.capitalize(), version.capitalize())

        k8s_api = getattr(client, func_to_call)()

        kind = json_object["kind"]
        kind = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', kind)
        kind = re.sub('([a-z0-9])([A-Z])', r'\1_\2', kind).lower()

        if "namespace" in json_object["metadata"]:
            namespace = json_object["metadata"]["namespace"]
        else:
            namespace = "default"

        try:
            if hasattr(k8s_api, "create_namespaced_{0}".format(kind)):
                resp = getattr(k8s_api, "create_namespaced_{0}".format(kind))(
                    body=json_object, namespace=namespace, **kwargs)
            else:
                resp = getattr(k8s_api, "create_{0}".format(kind))(
                    body=json_object, **kwargs)
        except Exception as e:
            raise e

            print("{0} created. status='{1}'".format(kind, str(resp.status)))

        return k8s_api


config.load_kube_config()
try:
    resp = create_from_json("/home/velotio/nginx.json")
except ApiException as e:
    print(e)
except Exception as e:
    print("general exception")
    print(e)

print(resp)
