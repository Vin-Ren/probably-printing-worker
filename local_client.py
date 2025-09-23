from http import client
import os
from dotenv import load_dotenv
import redis

class Client:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def add_task(self, task_data):
        self.redis_client.rpush('task_queue', task_data)
    
    def run(self):
        while True:
            task = input("Enter task data (or 'exit' to quit): ")
            if task.lower() == 'exit':
                break
            self.add_task(task)
            print(f"Task added: {task}")


if __name__ == "__main__":
    import argparse
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Printing Worker")
    
    parser.add_argument('--redis-url', type=str, default=os.getenv("REDIS_URL", "redis://localhost:6379/0"), help='Redis connection URL')
    
    args = parser.parse_args()

    r = redis.from_url(args.redis_url, decode_responses=True, encoding="utf-8")
    
    client = Client(r)
    client.run()
