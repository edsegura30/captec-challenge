# captec-challenge
Capital Technologies technical challenge
Edgar Segura

## Requirements
### For docker-compose usage
* Docker
* docker-compose

### For virtualenv
* Python3.9

## Running
### Using docker-compose
1. Clone repo
2. Copy required CSV to repo folder. The name of the file to process can be defining LOG_FILE_PATH
2. On repo root level use `docker-compose up`, this will build the DB and data-processor container
3. After build, data processor container will wait for DB to available and then will start processing data. The insights will be printed on the console

### Using virtualenv
1. Clone repo
2.  The name of the file to process can be defining LOG_FILE_PATH
3. Create virtualenv for project. You can use:

```python -m virtualenv captec_venv```
4. Activate the newly created virtual environment:

```source {path/to/virtualenv}/bin/activate```
5. Define required env vars (default values on db module):
* DB_HOST
* DB_NAME
* DB_PASSWORD
* DB_PORT
* DB_USER

6. Run script using:

```python calculate_revenue.py```


## Notes

* In order to restart process, you need to clear the DB as the get_or_create functionality is still not defined
* Duplicated *order_id* were skipped as my understanding that order ID should be unique
* The decision to use subprocess instead of pandas is the familiarity, and the capability to run and monitor a process directly from this the same python script. Also, I'm not really familiar with Pandas/Numpy so I'd rather show you what I know instead of making something horrible or not following best practices using frameworks that I'm not that familiar with.
* One of the improvements that I would like to make is to implement this as a CLI using python Click so this could be run as an utility or automated from another step.

