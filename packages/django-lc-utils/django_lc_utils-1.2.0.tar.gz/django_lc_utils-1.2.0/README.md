# Django LC Utils

Django app for various django utilities

`pip install django-lc-utils`

### Prerequisites

This package relies on `django-model-utils`, `Django`.

## Running Tests

```
python manage.py test
```

## Usuage

In order to use the system you must add django_lc_utils to your installed apps in your settings.py file.

```python
INSTALLED_APPS = [
    'django_lc_utils'
]
```

## Utilities

1. Django Soft Delete Mixin

This is a custom mixin to enable soft delete feature on the Django models.

```python
from django_lc_utils.mixins import SoftDeleteMixin
from model_utils.models import TimeStampedModel

class TestModel(TimeStampedModel, SoftDeleteMixin):
    class Meta:
        db_table = "test_model"
        verbose_name = "Django Test Model"
        verbose_name_plural = "Djando Test Models"

    test_field = models.TextField("Test field")
```

## Basic Docker usage

### Build
You'll need to build the dockerfile into an image, to do so, navigate to the root of the repository, and run the following
```bash
docker build -t <"NAME_YOU_WANT_FOR_THE_IMAGE"> .
```
where: . signifies the current directory
    -t signifies the tag flag, to tag the image and give it a name.
for example:
```bash
docker build -t lc_utils_test .
```

You can view all the docker images you have in your system,  by running ```docker images``` on the terminal.

You can remove an image that you pulled or build by running ```docker rmi <IMAGE_NAME/IMAGE_ID>``` on the terminal.

NOTE: To remove a container images from your local system, you need to stop and remove any container with that image running on your system.

### Run

To use a container you can create and start a container, you can do both at the same time by using the docker run command.

```
docker run -it --name=<NAME_FOR_THE_CONTAINER> <IMAGE_NAME> <OPTIONAL_COMMAND>
```
where -it signifies interactive terminal, use this to start and attach to the terminal of the container.
You can additionally pass an optional command to start when the container is first build, by default it runs the python shell in the case of python-slimbuster images, but using cmd we have made it to run bash by default.
an example for the run command would be:

```
docker run -it --name=test_container lc_utils_test /bin/bash

```
This would create a new container and connect to it's bash terminal.

To start a container you can run ```docker start <CONTAINER_NAME/CONTAINER_ID>``` on the terminal.

To stop a container you can run ```docker stop <CONTAINER_NAME/CONTAINER_ID>``` on the terminal.

To delete a container (if it's in the stopped state), you can run the ```docker rm <CONTAINER_NAME/CONTAINER_ID>``` on the terminal.

To list all the running containers you can run ```docker ps``` and to list all the containers regardless of the state you can run ```docker ps -a``` on the terminal.

To connect to a running container you can run ```docker attach <CONTAINER_NAME/CONTAINER_ID>``` on the teminal. Note that this does not start a new process on the container, to do that use the docker exec command instead.

If you want to avoid rebuilding and re-running containers after some change in the codebase, and want those changes to persist, you can mount volumes to the container while running it.


## Unit Tests

### Completed ->

formatters.py
dict_update.py
converters.py (xlxs_to_json function left, but will need a sample xlxs file for it)
### In-Progress ->
dates.py
    - next_business_day -> done
    - tz_aware -> pending
