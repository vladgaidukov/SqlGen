# SqlGen
NoSQL connector (sql generator) for MySql

python >= 3.4 required

# Install:

## Ubuntu:

sudo apt-get install python3-setuptools

python setup.py install

## Win:

python setup.py install

#Using:

```python
import sqlgen

config = {
    'user':'root',
	'password':'root',
	'host':'127.0.0.1',
	'database': 'dbname'
}
con = sqlgen.SqlGen(config)

#Simple select
con.select('category')

[{'recid': 1, 'record_status_recid': 1, 'name': 'Test'}, {'recid': 2, 'record_status_recid': 1, 'name': 'Test2'}, {'recid': 3, 'record_status_recid': 1, 'name': 'Test3'}]

#Update record
con.update('category', columns={'name':'Food'}, param={'recid': 1})

{'recid': 1, 'record_status_recid': 1, 'name': 'Food'}

#Insert record
con.insert('category', columns={'name':'Meat', 'record_status_recid' : 1})

{'recid': 1, 'record_status_recid': 1, 'name': 'Meat'}
```
