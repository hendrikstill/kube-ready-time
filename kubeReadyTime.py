import subprocess
import json
import argparse
import csv
from datetime import datetime, timezone

def get_pod_ready_time(namespace, label_selector=None, output_csv=False, csv_filename=None):
    # Create the kubectl command based on the namespace and optional label selector
    command = f"kubectl get pods -n {namespace} -o json"
    if label_selector:
        command += f" -l {label_selector}"

    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("Error retrieving pod information:")
        print(result.stderr)
        return

    pod_info = json.loads(result.stdout)

    if output_csv:
        if not csv_filename:
            csv_filename = f"pod_info_{namespace}.csv"
        with open(csv_filename, mode="w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Pod Name", "Namespace", "Labels", "Ready Time (UTC)", "PodScheduled Time (UTC)", "ContainersReady Time (UTC)", "Duration until ready"])

            for pod in pod_info.get("items", []):
                pod_name = pod["metadata"]["name"]
                labels = ",".join([f"{key}={value}" for key, value in pod["metadata"]["labels"].items()])
                ready_time = None
                scheduled_time = None
                containers_ready_time = None

                for condition in pod.get("status", {}).get("conditions", []):
                    if condition["type"] == "Ready":
                        ready_time = datetime.fromisoformat(condition["lastTransitionTime"].rstrip('Z')).replace(tzinfo=timezone.utc)
                    if condition["type"] == "PodScheduled":
                        scheduled_time = datetime.fromisoformat(condition["lastTransitionTime"].rstrip('Z')).replace(tzinfo=timezone.utc)
                    if condition["type"] == "ContainersReady":
                        containers_ready_time = datetime.fromisoformat(condition["lastTransitionTime"].rstrip('Z')).replace(tzinfo=timezone.utc)

                if ready_time and scheduled_time:
                    duration = ready_time - scheduled_time
                    if containers_ready_time:
                        csv_writer.writerow([pod_name, namespace, labels, ready_time, scheduled_time, containers_ready_time, duration])
                    else:
                        csv_writer.writerow([pod_name, namespace, labels, ready_time, scheduled_time, "", duration])
        print(f"CSV output saved to {csv_filename}")
    else:
        for pod in pod_info.get("items", []):
            pod_name = pod["metadata"]["name"]
            labels = ",".join([f"{key}={value}" for key, value in pod["metadata"]["labels"].items()])
            ready_time = None
            scheduled_time = None
            containers_ready_time = None

            for condition in pod.get("status", {}).get("conditions", []):
                if condition["type"] == "Ready":
                    ready_time = datetime.fromisoformat(condition["lastTransitionTime"].rstrip('Z')).replace(tzinfo=timezone.utc)
                if condition["type"] == "PodScheduled":
                    scheduled_time = datetime.fromisoformat(condition["lastTransitionTime"].rstrip('Z')).replace(tzinfo=timezone.utc)
                if condition["type"] == "ContainersReady":
                    containers_ready_time = datetime.fromisoformat(condition["lastTransitionTime"].rstrip('Z')).replace(tzinfo=timezone.utc)

            if ready_time and scheduled_time:
                duration = ready_time - scheduled_time
                print(f"Pod '{pod_name}' in Namespace '{namespace}' - Labels: {labels}, Ready: {ready_time} UTC, PodScheduled: {scheduled_time} UTC, ContainersReady: {containers_ready_time} UTC, Duration until ready: {duration}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find out when Kubernetes pods in a namespace are ready, scheduled, and containers are ready.")
    parser.add_argument("namespace", help="Namespace of the pods")
    parser.add_argument("--label-selector", help="Label selector for the pods (optional)")
    parser.add_argument("--csv", action="store_true", help="Generate CSV output (optional)")
    parser.add_argument("--csv-filename", help="Specify the CSV filename (optional)")
    args = parser.parse_args()

    get_pod_ready_time(args.namespace, args.label_selector, args.csv, args.csv_filename)
