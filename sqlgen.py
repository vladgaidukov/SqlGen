import mysql.connector
import traceback

DB_TABLE_INDEX = 'recid'

class SqlGen:
    def __init__(self,config):
        try:
            self.scripts = {}
            self.tables = []
            self.connect(config)
        except:
            traceback.print_exc()
            
    def connect(self,config):
        try:
            self.cnx = mysql.connector.connect(user=config['user'],
                                               password=config['password'],
                                               host=config['host'],
                                               database=config['database'],
                                               buffered=True)
            self.cursor = self.cnx.cursor()
            self._generate_scripts()
        except:
            traceback.print_exc()
            
    def checkConn(self):
        try:
            if self.cnx.is_connected():
                return True
            else:
                self.connect()
        except:
            traceback.print_exc()
            
    def _generate_scripts(self):
        try:
            s1 = 'select %s from '
            s2 = ' where 1=1 '
            u1 = 'update %s set'
            i1 = 'insert into %s'

            self.cursor.execute('SHOW TABLES')
            tables = self.cursor.fetchall()

            for table in tables:
                self.tables.append(table[0]);
                self.cursor.execute('describe ' + table[0])
                columns = [rec[0] for rec in self.cursor.fetchall()]
                ids = (', ').join(columns)
                self.scripts[table[0]] = {}
                self.scripts[table[0]]['columns'] = columns
                self.scripts[table[0]]['select'] = (s1 % ids) + table[0] + s2
                self.scripts[table[0]]['update'] = u1 % table[0]
                self.scripts[table[0]]['insert'] = i1 % table[0]
            print('Scripts generation complete !!!')
        except:
            traceback.print_exc()
            return {'status': 'error', 'message': traceback.format_exc()}

    def select(self, table, param={}, order=None):
        try:
            self.checkConn()
            string = ''
            if table in self.scripts:
                values = []
                for p in param:
                    if p in self.scripts[table]['columns']:
                        if isinstance(param[p], list):
                            string = string + ' and %s in (%s)' % (p, ', '.join(['%s' for el in param[p]]))
                            for x in param[p]: values.append(x)
                        else:
                            string = string + ' and %s = %s' % (p, '%s')
                            values.append(param[p])
                string = self.scripts[table]['select'] + string
                if order:
                    string = string  + ', '.join([' order by ' + str(o) + ' ' + order[o] for o in order if o in self.scripts[table]['columns']])
                self.cursor.execute(string, values)
                res = self.cursor.fetchall()
                hres = []
                for rec in res:
                    hres.append({col:rec[self.scripts[table]['columns'].index(col)] for col in self.scripts[table]['columns']})
                return hres
            else:
                return {'status': 'error', 'message': 'Таблица не существует'}
        except:
            traceback.print_exc()
            return {'status': 'error', 'message': traceback.format_exc()}

    def update(self, table, columns={}, param={}):
        try:
            self.checkConn()
            if table in self.scripts:
                string = ' where 1=1'
                values = []
                tmpstring = ''
                for c in columns:
                    if c in self.scripts[table]['columns']:
                        tmpstring = tmpstring + ' %s = %s,' % (c, '%s')
                        values.append(columns[c])
                tmpstring = tmpstring[:-1]
                string = tmpstring + string
                for p in param:
                    if isinstance(param[p], list):
                        string = string + ' and %s in (%s)' % (p, ', '.join(['%s' for el in param[p]]))
                        for x in param[p]: values.append(x)
                    else:
                        string = string + ' and %s = %s' % (p, '%s')
                        values.append(param[p])
                self.cursor.execute(self.scripts[table]['update'] + string, values)
                self.cnx.commit()
                return {'status':'success'}
            else:
                return False
        except:
            traceback.print_exc()
            return {'status': 'error', 'message': traceback.format_exc()}

    def insert(self, table, columns={}):
        try:
            self.checkConn()
            if table in self.scripts:
                values = []
                tmpstring = ' ('
                string = ''
                if DB_TABLE_INDEX in columns.keys():
                    del(columns[DB_TABLE_INDEX])
                for c in columns:
                    if c in self.scripts[table]['columns']:
                        tmpstring = tmpstring + c + ','
                        values.append(columns[c])
                tmpstring = tmpstring[:-1] + ')'
                string = tmpstring + string
                string = string + ' values (%s)' % (', '.join(['%s' for el in columns]))
                self.cursor.execute(self.scripts[table]['insert'] + string, values)
                self.cnx.commit()
                return {'status':'success'}
            else:
                return False
        except:
            traceback.print_exc()
            return {'status': 'error', 'message': traceback.format_exc()}
			
    def getTableData(self, table, param=None, order=None):
        data = self.select(table, param=param or [], order={'poryad':'desc'} or order)
        tmpTable = ''
        joindata = {}
        if isinstance(data, list) and len(data) > 0:
            for rec in data:
                for col in rec:
                    if col[-len(DB_TABLE_INDEX):] == DB_TABLE_INDEX and col != DB_TABLE_INDEX:
                        tmpTable = col[0:-6]
                        if tmpTable not in joindata:
                            joindata[tmpTable]={}
                        if rec[col] in joindata[tmpTable]:
                            print('not select')
                            rec[col] = joindata[tmpTable][rec[col]]
                        else:
                            for arec in self.getTableData(tmpTable, param={DB_TABLE_INDEX:rec[col]} or []):
                                joindata[tmpTable][rec[col]] = arec
                                rec[col] = arec  
                        
        print(joindata)
        return data
        
    def select_custom(self, script, param):
        self.checkConn()
        self.cursor.execute(script, param)
        res = self.cursor.fetchall()
        return res
		
    def sql_custom(self, script):
        self.checkConn()
        self.cursor.execute(script, multi=True)