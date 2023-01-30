# Alertmanager

Here is a design diagram of whole project:

[diagram]

In this repo we extracted the part of the system that is responsible for handling alert delivery and confirmation of receipt.

- ### Alertsender

- ### Alertconfirmer

- ### Alertmanager

---

## Local setup

One has to define following env variables (example of an .env file, specific values may differ):

```bash
INSTANCE_HOST=xxxxxxxx # IP of the postgres database
DB_USER=postgres
DB_PASS=xxxxxxxx
DB_NAME=alerts
DB_PORT=5432
ALERTSENDER_ENDPOINT=[::]:50051
ALERTMANAGER_ENDPOINT=[::]:50052
ALERTCONFIRMER_ENDPOINT=[::]:50053
```

### Build

```bash
docker build -t alertsender:latest alertsender
docker build -t alertmanager:latest alertmanager
docker build -t alertconfirmer:latest alertconfirmer
```

### Run

```
docker run -d -p 50051:50051  --env-file .env alertsender:latest
docker run -d -p 50052:50052  --env-file .env alertmanager:latest
docker run -d -p 50053:50053  --env-file .env alertconfirmer:latest
```

---

## Cloud run setup

Env variables for docker containers:

```yaml
INSTANCE_UNIX_SOCKET: /cloudsql/project_id:region:instance
DB_USER: postgres
DB_PASS: xxxxxxxx
DB_NAME: alerts
DB_PORT: 5432
ALERTMANAGER_ENDPOINT: alertmanager-xxxxxxxx-lz.a.run.app:443
ALERTSENDER_ENDPOINT: alertsender-xxxxxxxx-lz.a.run.app:443
ALERTCONFIRMER_ENDPOINT: alertconfirmer-xxxxxxxx-lz.a.run.app:443
```

Env variables for deployment:

```bash
GCP_PROJECT=xxx # Google cloud project id e.g. cloudruntest-123456
SENDER_IMAGE_NAME=xxx
MANAGER_IMAGE_NAME=xxx
CONFIRMER_IMAGE_NAME=xxx
GCP_ALERTSENDER_APP_NAME
GCP_ALERTSENDER_APP_NAME
GCP_ALERTSENDER_APP_NAME
```

### Build

Build docker images and push them to the container registry:

```bash
./scripts/build-docker.sh alertsender $SENDER_IMAGE_NAME
./scripts/build-docker.sh alertmanager $MANAGER_IMAGE_NAME
./scripts/build-docker.sh alertconfirmer $CONFIRMER_IMAGE_NAME
```

### Deploy

When deploying for the first time there are a few caveats:

- We cannot deduce endpoints of each service before they are deployed for the first time.
  Hence, we will need to update those values after first failed deployment.
- We have to set necessary secrets/env variables for each service. Next revisions will inherit those variables, so it is only one time hassle.

```bash
gcloud run deploy $GCP_ALERTSENDER_APP_NAME \
--image $SENDER_IMAGE_NAME \
--region europe-north1 \
--platform managed \
--allow-unauthenticated
--env-vars-file .env.yaml
```

```bash
gcloud run deploy $GCP_ALERTMANAGER_APP_NAME \
--image $MANAGER_IMAGE_NAME \
--region europe-north1 \
--platform managed \
--allow-unauthenticated
--env-vars-file .env.yaml
--add-cloudsql-instances=INSTANCE_CONNECTION_NAME
```

```bash
gcloud run deploy $GCP_ALERTCONFIRMER_APP_NAME \
--image $CONFIRMER_IMAGE_NAME \
--region europe-north1 \
--platform managed \
--allow-unauthenticated
--env-vars-file .env.yaml
```

```bash
gcloud run deploy $GCP_ALERTREMINDER_APP_NAME \
--image $REMINDER_IMAGE_NAME \
--region europe-north1 \
--platform managed \
--allow-unauthenticated
--env-vars-file .env.yaml
--add-cloudsql-instances=INSTANCE_CONNECTION_NAME
--cpu-throttling
--min-instances=1
```

## Testing

We have functional, stress and load tests. Since they cause quite a strain on the system it is advised to run them only on a non-prod environments/deployments.

### Setup

Again several environment variables have to exported:

```bash
API_ENDPOINT=https://datamanager-api-2xieibhnsq-lz.a.run.app # endpoint of datamanager api service
INSTANCE_HOST=28.222.222.000 # IP of the database used by the deployment
DB_USER: postgres
DB_PASS: xxxxxxxx
DB_NAME: alerts
DB_PORT: 5432

# specifically for sendgrid_test
SENDGRID_API_KEY=xxx  # api key which you can get from sendgrid
SENDER_EMAIL=xxxx@gmail.com # email which is configured as a sender in sendgrid
```

And some dependencies must be installed. Run following:(please use python virtualenv for better experience):

```bash
cd tests
pip install -r requirements.txt
```

### Test execution

To run all tests (all following commands assume being in `tests` directory):

```bash
py.test
```

To run functional tests:

```
py.test integration_test.py
```

To run load tests (they might take a while):

```
py.test load_test.py
```

## CI/CD

There is a CI/CD workflow defined for this repository. It is triggered by pushing/pulling any changes to the `master` branch.
It consists of four stages:

- authenticating in gcloud cli
- building docker containers for each service
- pushing containers to a remote container registry
- deploying all services to cloud run

It will not work if the services are not set up manually for the first time! That's because, as mentioned before, service endpoints cannot be deduced beforehand.
