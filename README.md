# SqlGen
NoSQL connector for MySql

python >= 3.4 required

#Install:

##Debian:

sudo apt-get install python3-setuptools

python setup.py install

##Win:

python setup.py install

#Using:

import sqlgen

config = {
    	'user':'root',
	'password':'root',
	'host':'127.0.0.1',
	'database': 'dbname'
}

sqlgen.DB_TABLE_INDEX = 'recid' #default

con = sqlgen.SqlGen(config)


##Get table data with joins

con.getTableData('category', param={'record_status_recid':1})

{'status':'success',
  'data': [
 {'record_status_recid': {'name': 'Одобрен', 'recid': 1}, 
    'name': 'Test',
    'recid': 1}, 
 {'record_status_recid': {'name': 'Одобрен', 'recid': 1}, 
   'name': 'Test22', 
   'recid': 2}, 
 {'record_status_recid': {'name': 'Одобрен', 'recid': 1}, 
   'name': 'Test3', 
   'recid': 3}
]}

##Simple select

con.select('category')

{'status': 'success', 'data': [{'recid': 1, 'record_status_recid': 1, 'name': 'Test'}, {'recid': 2, 'record_status_recid': 1, 'name': 'Test22'}, {'recid': 3, 'record_status_recid': 1, 'name': 'Test3'}]}

##Update record

con.update('category', columns={'name':'Food'}, param={'recid': 1})

{status:'success'}

##Insert record

con.insert('category', columns={'name':'Meat', 'record_status_recid' : 1})

{status:'success'}



