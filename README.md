# Alertmanager

Here is a design diagram of whole project:

[diagram]

In this repo we extracted the part of the system that is responsible for handling alert delivery and confirmation of receipt.

## Alertsender

This service is responsible for delivering emails to a given recipient. It is an auxiliary service for alertmanager since it only handles the logic of sending emails via sendgrid API.

### Build

Remember to set `GCP_PROJECT` variable. (for local deployment its value doesn't matter but it cannot be empty since `//` is an illegal pattern in a container tag)

```
docker build -t gcr.io/$GCP_PROJECT/alertsender:latest alertsender
```

### Run

To run it one has to export a few env variables:

```
SENDGRID_API_KEY=xxx  #get it from sendgrid website
SENDER_EMAIL=john.doe@gmail.com # email which is configured in sendgrid to send out messages
PORT=localhost::50051 #on which port should the service run
```

Running container, given variables mentioned above are defined in an .env file

```
docker run -p $PORT:$PORT  --env-file .env  gcr.io/$GCP_PROJECT/alertsender:latest
```

## Alertconfirmer

[Description]

### Build

```
docker build -t gcr.io/$GCP_PROJECT/alertconfirmer:latest alertconfirmer
```

### Run

First export following variables or place them in an .env file.

```
ALERTMANAGER_ENDPOINT=[::]:50052 # endpoint on which alertmanager service is listening on
PORT=localhost::50053 # on which port should the service run
```

Start container:

```
docker run -p $PORT:$PORT  --env-file .env  gcr.io/$GCP_PROJECT/alertconfirmer:latest
```

## Alertmanager

[Desc]

### Build

```
docker build -t gcr.io/$GCP_PROJECT/alertmanager:latest alertmanager
```

### Run

First export following variables or place them in an .env file.

```
ALERTSENDER_ENDPOINT=[::]:50051 # endpoint on which alertsender service is listening on
ALERTCONFIRMER_ENDPOINT=[::]:50053 # endpoint on which alertconfirmer service is listening on
PORT=localhost::50052 # on which port should the service run
```

Furthermore one has to export/define in an .env file following db connection parameters:

```
DB_USER=postgres
DB_PASS=h#}+UM0J&1]sF/9/
DB_NAME=alerts
DB_PORT=5432
INSTANCE_HOST=127.0.0.1 # database host
```

Start container:

```
docker run -p $PORT:$PORT  --env-file .env  gcr.io/$GCP_PROJECT/alertconfirmer:latest
```
