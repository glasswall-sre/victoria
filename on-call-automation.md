# SRE On-call Automation Feasibility

It's very tedious and boring being on-call. We should have a toolbelt that can
do EVERYTHING for us.

## The vision
A python command line tool that has subcommands to do everything we need.

Features:
- Subcommands for each thing that we'll have to do, like:
    - Create/move/assign PBIs on an Azure DevOps board
    - Move releases to a new environment in Azure DevOps
    - Check Kubernetes cluster logs and restarts
    - Access/use alert manager in a cluster easily
    - Interact with PagerDuty (when we have it...)
    - Reply to emails requesting things
    - Find TX IDs for emails with some metadata to quickly identify problem
      mails where support don't give us the IDs
    - Download an entire blob as a zip
    - Quickly run log analytics queries and sub values in
- We'll always be finding new things to do, so the program will need to be
  easily extensible, so people can constantly add more automations
- The core functionality needs to be highly decoupled from the CLI user
  interface, so that future extensions (i.e. different user interfaces) are
  easy to make. What about a GUI?

## Components

### Azure DevOps integration
- Azure DevOps API has a [Python client](https://github.com/microsoft/azure-devops-python-api)
  It seems to loosely wrap the [REST API](https://docs.microsoft.com/en-us/rest/api/azure/devops)
    - [Creating work items](https://github.com/microsoft/azure-devops-python-api/blob/dev/azure-devops/azure/devops/v5_1/work_item_tracking/work_item_tracking_client.py#L1578)
    - Moving work items seems to be done via an update on `System.State` field
        - [See here](https://github.com/microsoft/azure-devops-python-api/blob/dev/azure-devops/azure/devops/v5_1/work_item_tracking/work_item_tracking_client.py#L1730)
    - Assigning work items seems to be done via an update on `System.AssignedTo` field
        - [See here](https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work%20items/update?view=azure-devops-rest-5.1#update-an-identity-field-by-display-name)
    - Deploying releases
        - [See here](https://docs.microsoft.com/en-us/rest/api/azure/devops/release/releases/update%20release%20environment?view=azure-devops-rest-5.1#examples)

### Kubernetes integration
- Kubernetes API has a [Python client](https://github.com/kubernetes-client/python)
    - Getting logs
        - Looks like you can get logs [like this](https://stackoverflow.com/questions/56124320/how-to-get-log-and-describe-of-pods-in-kubernetes-by-python-client)
    - Getting restart counts
        - pod `status.containerStatuses.restartCount`
        - Query [this endpoint](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#read_namespaced_pod)
        - [This](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ContainerStatus.md) piece of data
    - Port forwarding
        - I think you can do it [like this](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#connect_get_namespaced_pod_portforward)

### Office 365 mail integration
- [Yeet](https://stackoverflow.com/questions/46160886/how-to-send-smtp-email-for-office365-with-python-using-tls-ssl)

### Azure Log Analytics integration
- Log analytics has a [REST API](https://docs.microsoft.com/en-us/rest/api/loganalytics/)
    - We will mostly be using the [query execute endpoint](https://docs.microsoft.com/en-us/rest/api/loganalytics/query/execute)
- Or we could just use the [Python SDK](https://azure.github.io/azure-sdk-for-python/ref/azure.loganalytics.html#azure.loganalytics.LogAnalyticsDataClient.query)
- Draw results with [tabulate](https://pypi.org/project/tabulate/)
- Output results to a number of different formats