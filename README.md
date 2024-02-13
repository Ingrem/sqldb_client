# sqldb_client

#### Installation:

pip install git+ssh://git@gitaddress.com/qa/sqldb_client.git

env:
* sqlalchemy
* psycopg2-binary
* qa/logger.git
* python-logstash

## Description

Module for working with sql databases

## Adding new functions to the library

To add default parameters when creating objects, you can add the default parameter to the object fields
For example, for the exp_tabl table there is no point in specifying name every time, so let's add default to the name field:
name = Column(String(256), nullable=False, default="exp_tabl name")
now all exp_tabl will be created without the need to set this parameter.
DO NOT USE VALUES FOR FIELDS THAT ARE NOT IDEMPOTENT

## Example of work:
```python
# settings.py
from db_contractor.db_connect import DBConnect
from db_contractor.entities_generator import EntitiesGenerator

db_connect = DBConnect(host="0.0.0.0", port="5432", db_name="db_name", username="user", password="pass", logger=logger)

# *.py
from db_contractor.processing_scheme import GlobalSetting, Match, Sport, Region, Competition
from settings import db_connect, entities_generator

# custom select
result_int = db_connect.get_one_result("SELECT id FROM table LIMIT 100")
result_list = db_connect.get_list_result("SELECT * FROM table LIMIT 100")
result_dict = db_connect.get_dict_result("SELECT * FROM table LIMIT 100")

#custom insert, delete, update
db_connect.session.execute("DELETE FROM table WHERE id = -100000")
```

## Recommendations for work

It is recommended to initialize the object for working with the database once in the entire project, and then import the object itself.

