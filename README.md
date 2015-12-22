# dreamboat
Configurable heartbeat maker for multiple endpoints

Note: This project depends on the acacia base Docker image that is currently part of headspring. Before using this repo, download headspring and create the acacia base Docker image using the command:

docker build -t acacia acacia/

To Build Docker Image:

1) Build docker image:
docker build -t gcr.io/hx-test/dreamboat-multi .

2) Upload image to Google's image repo:
gcloud docker push gcr.io/hx-test/dreamboat-multi

To Deploy on GCP:

1) Create cluster:
gcloud container clusters create dreamboat-container --num-nodes 1 --machine-type g1-small --scopes https://www.googleapis.com/auth/cloud-platform

2) Create a pod and pass environment variables:
kubectl run dreamboat-container --image=gcr.io/hx-test/dreamboat-multi --env="your_variable=your_value"

Possible configurable env variables:

endpoint = comma separated list of endpoints (default: 127.0.0.1:8080/post)

msg_per_sec = number of heartbeat messages to send per second (default: 2)

field = field of json (default: \_heartbeat\_)

value = value of json (default: yes)

log_level = log level (default: DEBUG)

By default, the message written by the heartbeat is:

{"\_heartbeat\_","yes"}, however this is customizable using the 'field' and 'value' parameters above.
