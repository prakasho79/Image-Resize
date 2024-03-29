# About The Project

A JSON-based REST API service which resizes images into 100x100px thumbnails.

## Installation
1. Clone the repo: 
```bash
git clone https://github.com/prakasho79/Image-Resize.git
```

2. Use the [docker-compose](https://docs.docker.com/compose/) to build & run the application.

```bash
sudo docker-compose up -d --build
```

## Test

To test the endpoints we can either use postman or curl command from CLI or mointor the tasks from Flower (Web based UI. See section for Monitor)

1. Upload a image
```
curl -X POST "http://localhost:8000/create" -H "Content-Type: multipart/form-data" -H "Accept: application/json" -F image_data=@./dataset/Square_on_hyperbolic_plane.png
```
#### Output -
```
{
    "status": "success",
    "data": {
        "task_id": "bddea89f-4a70-4951-afa3-3551844d4533"
    }
}
```

2. Query Job - 
Get the status of the job using the celery task Id
```
curl http://localhost:8000/status/bddea89f-4a70-4951-afa3-3551844d4533
```
#### Output - 
``` bash
{
    "status": "SUCCESS",
    "result": {
        "Original": {
            "file_path": "./images/uploaded/Square_on_hyperbolic_plane.png",
            "Size": [
                613,
                624
            ]
        },
        "Thumbnail": {
            "file_path": "./images/thumbnail/Square_on_hyperbolic_plane.png",
            "Size": [
                99,
                100
            ]
        }
    }
}
```

## Architecture

The architecture used is queue based worker employing Celery which is an asynchronous task queue/job queue based on distributed message passing. Internally Celery uses Redis as message broker.
The application uses tool called Flower which will help to monitoring real time Celery Events. Task progress and history.

There are number of things we could do to scale horizontally. Some of them are described as below -
* We could increase the number of Gunicorn workers (see docker-compose.yml)
* The celery container has auto-scale parameter (see docker-compos.yml). This will ensure auto scale up / down based on the load.
* We can have distributed cluster setup for each of these containers using Kubernetes or Docker Swarm or Mesos.


##  Components

The application has the following services / components running -
* Web Container - The main JSON / REST style application running on Gunicorn (WSGI) server.
* Celery Container - The distributed task queue.
* Flower Container - The tool for monitoring real time Celery Events. Task progress and history.
* Redis Container - The message broker

The request hits the Gunicorn server, where the middleware multipart parses the form data to get the file. The file is submitted to celery task. The background processing happens
asynchronously. The celery internally use message broker (Redis) to submit the task to message queue and the worker will consume and process the task.

### Deployment:
We can have either on-prem or on-cloud deployment.

* On-prem deployment:
The containers can be deployed on-prem using a Docker Swarm / Mesos cluster setup with NGNIX accepting incoming request acting as reverse-proxy.

* On-Cloud deployment:
The containers can be deployed on Kubernetes cluster on the pods in either AWS, Azure or GCP with NGNIX accepting incoming request acting as reverse-proxy.


## Logging:
* gunicorn_access.log - All access to gunicorn server are logged.
* gunicorn_error.log - All errors encouter in the application hosted in  gunicorn server are logged.
* celery.log - Contains the log out from celery tasks

## Monitor Tasks:
* Launch [Flower](http://localhost:5555)
* Navigate to Tasks tab to see all running Celery tasks

## Limitations:
* Only tested the solution with JPG, PNG file format.
* Concurent users invoking endpoint or scalability test not done. 

## Future Improvements:
* Securing the REST endpoint - Only authorized user can invoke the endpoint. May be use OAuth, token based security approach.
* Proper exception handling - The user needs to get user friendly error stating the reson for exception.
* Proper logging - Probably centralized logging using logStats, Elastic Search and Kibana
* Validation check improvements on the params passed in the request.
* Doing a performace load tesing (probably using Taurus)
* NGnix / Nginx Plus needs to be used as reverse-proxy to secure the request made by the client program.
* All the constants (static key/value pair) should be defined in the .ini file
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
