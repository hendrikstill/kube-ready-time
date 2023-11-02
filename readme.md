# kubeReadyTime.py

`kubeReadyTime.py` is a Python script that helps you retrieve information about the readiness of Kubernetes pods in a specific namespace. It provides details about when the pods became ready, when they were scheduled, and when the containers inside them became ready. Additionally, it allows you to specify label selectors for filtering pods.

## Prerequisites

Before using `kubeReadyTime.py`, ensure you have the following prerequisites:

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/): The Kubernetes command-line tool, configured to work with your cluster.

## Usage

You can use the script with the following command-line arguments:

```bash
python kubeReadyTime.py <namespace> [--label-selector=<label_selector>] [--csv] [--csv-filename=<csv_filename>]
```

<namespace>: The namespace where your pods are located.
--label-selector=<label_selector> (Optional): Label selector to filter pods based on labels.
--csv (Optional): Generate output in CSV format.
--csv-filename=<csv_filename> (Optional): Specify the name of the CSV file when using --csv.

### Example Usage
Retrieve readiness information for pods in the my-namespace namespace:

```bash
python kubeReadyTime.py my-namespace
```
Retrieve readiness information for pods with a specific label selector:

```bash
python kubeReadyTime.py my-namespace --label-selector=app=my-app
```
Generate CSV output with a custom filename:

```bash
python kubeReadyTime.py my-namespace --csv --csv-filename=pod_readiness.csv
```

### Output
The script provides information about each pod's readiness status, including:

Pod Name
Namespace
Labels (if specified)
Ready Time (UTC)
PodScheduled Time (UTC)
ContainersReady Time (UTC)
Duration until ready
The output can be displayed in the console or saved to a CSV file when using the --csv option.

