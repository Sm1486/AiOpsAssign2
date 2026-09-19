import json
import re
from kubernetes import client, config

RESULTS_RE = re.compile(r"RESULT_JSON (\{.*\})")

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace =' default', label_selector = 'app=signup-shard-validator')

    results = []
    for pod in pods.items:
        pod_name = pod.metadata.name
        node_name = pod.spec.node_name
        log = v1.read_namespaced_pod_log(name = pod_name, namespace = "default")
        match = RESULT_RE.search(log)
        result["node_name_from_api"] = node_name
        results.append(result)
        with open("shards/collected_results.json", "w") as f:
            json.dump(results, f)

if __name__ == "__main__":
    main()
