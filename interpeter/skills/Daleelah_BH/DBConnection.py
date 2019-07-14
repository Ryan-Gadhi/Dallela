from sqlalchemy import create_engine
import pandas as pd
import pandas.io.sql as psql
import socket
# NoSQL data base
try:
    from couchbase.cluster import Cluster
    from couchbase.cluster import PasswordAuthenticator
except:
    pass
 
class PWDBConnection:
    def __init__(self):
        # SQL
        #self.engine = create_engine('postgresql://postgres:Well226898@10.96.177.109:5433/dashboard1')
        self.engine = create_engine('postgresql://postgres:Well226898@10.96.177.109:5433/PWdata')
        self.enginesettings = create_engine('postgresql://postgres:Well226898@10.96.177.109:5433/PWsettings')
        self.enginegen2 = create_engine('postgresql://postgres:hrdh1222@10.96.177.78:5432/pwdata')
        ##conninfo = "dbname='pwdata' user='postgres' host='10.96.177.78' password='hrdh1222' port='5432'"
 
        try:
            # NoSQL
            self.cluster = Cluster('couchbase://10.96.177.33:8091')
            self.authenticator = PasswordAuthenticator('nosqldata', 'nosqldata2018')
            self.cluster.authenticate(self.authenticator)
            self.tbucket = 'updated_daily_report'
            self.cb = self.cluster.open_bucket(self.tbucket)
        except:
            pass
 
    def sqldb(self):
        return self.engine
 
    def nosqldb(self):
        return self.tbucket, self.cb
 
    def read_sql_ck(self, query, orderindex):
        chunk_size = 100000
        offset = 0
        dflist = []
        while True:
            sql = query+" order by %s limit %d offset %d" % (orderindex, chunk_size, offset)
            dflist.append(pd.read_sql_query(sql, self.engine))
            offset += chunk_size
            if len(dflist[-1]) < chunk_size:
                break
        fulldf = pd.concat(dflist)
        return fulldf
 
    def write_sql_ck(self, df, table, table_status='replace', chunk_size=10000):
        i = 0
        j = chunk_size
        maxs = df.shape[0]
        end=False
        while True:
            if j >= maxs:
                j = maxs
                end=True
            if i == 0:
                df.iloc[i:j,:].to_sql(table, self.engine, if_exists=table_status)
            else:
                df.iloc[i:j,:].to_sql(table, self.engine, if_exists='append')
            i = j
            j += chunk_size
            if end:
                break
        return

pwd = PWDBConnection()
sqlRes = pd.read_sql_query("select count(*) from interns_view where \"Company\"='SUW' ", pwd.engine)
print(type(sqlRes))
