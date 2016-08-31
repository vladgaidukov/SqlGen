# SqlGen
NoSQL connector for MySql

python >= 3.4 required

#Install:
  Debian:
    sudo apt-get install python3-setuptools
    python setup.py install
  Win:
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

con.getTableData('category', param={'record_status_recid':1})

[{'record_status_recid': {'name': 'Одобрен', 'recid': 1}, 
    'name': 'Test',
    'recid': 1}, 
 {'record_status_recid': {'name': 'Одобрен', 'recid': 1}, 
   'name': 'Test22', 
   'recid': 2}, 
 {'record_status_recid': {'name': 'Одобрен', 'recid': 1}, 
   'name': 'Тест3', 
   'recid': 3}
]


