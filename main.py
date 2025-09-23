from datetime import datetime
import secrets
import requests
import os
import redis
import json
import cups
from dotenv import load_dotenv
import tempfile
from cpp_to_pdf import cpp_to_pdf


class Worker:
    def __init__(self, redis_client: redis.Redis, enabled_printers=""):
        self.redis_client = redis_client
        self.conn = cups.Connection()
        self.config = {}
        self.enabled_printers = [e.strip() for e in enabled_printers.split(",")] if enabled_printers else []
        self.job_context = {}

    def cout(self, msg):
        if (self.job_context):
            print(f"[{self.job_context.get('id', 'unknown')} - {datetime.now().isoformat()}] {msg}")
        else:
            print(f"[{datetime.now().isoformat()}] {msg}")
    
    def run(self):
        self.cout("Worker started, waiting for tasks...")
        while True:
            task = self.redis_client.blpop('task_queue', timeout=0)
            try:
                # Blocking pop from a Redis list named 'task_queue'
                if task:
                    _, task_data = task
                    self.process_task(json.loads(task_data))
                    self.redis_client.lrem('task_queue', 1, task_data)
            except json.JSONDecodeError as e:
                self.cout(f"Failed to decode task data: {e}.\nData: {task}\nRefuse to requeue.")
            except KeyboardInterrupt:
                return
            except Exception as e:
                self.cout(f"Error processing task {task}: {e}. Requeueing.")
                if task:
                    _, task_data = task
                    self.redis_client.rpush('task_queue', task_data)

    def fetch_config(self):
        self.config = self.redis_client.hgetall('config')
    
    def download_code(self, url, dest):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(dest, 'w') as f:
                f.write(response.text)
            return True
        except Exception as e:
            self.cout(f"Failed to download code from {url}: {e}")
            return False

    def convert_to_pdf(self, filename, teamname, output_pdf=None):
        cpp_to_pdf(filename, teamname, output_pdf, css_string=self.config.get("css_string"), job_context=self.job_context)
    
    def print_from_pdf(self, pdf_path):
        # Placeholder for printing logic
        idle_printers = [k for k,v in self.conn.getPrinters().items() if v["printer-state"] == 3 and (not self.enabled_printers or k in self.enabled_printers)]
        if (not idle_printers):
            raise RuntimeError("No idle printers available.")

        self.cout(f"Printing PDF: {pdf_path} with printer {idle_printers[0]}")
        job_id = self.conn.printFile(idle_printers[0], pdf_path, self.job_context.get("id", secrets.token_hex(8)), {})
        self.cout(f"Print job submitted to printer {idle_printers[0]} with ID: {job_id}")

    def process_task(self, task):
        # Data format: {"id": "Some_ID", "filename": "code.cpp", "teamname": "Team A", "code_url": "http://example.com/code.cpp"}
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                task_id = task.get("id", "unknown")
                filename = task.get("filename", "code.cpp")
                teamname = task.get("teamname", "Unknown Team")
                code_url = task.get("code_url")
                output_code = os.path.join(tmpdirname, filename) if filename else None
                output_pdf = os.path.join(tmpdirname, f"{task_id}.pdf")
                
                self.job_context = {"id": task_id, "teamname": teamname, "filename": filename}

                self.cout(f"Processing task {task_id} for team {teamname}")
                self.download_code(code_url, output_code)
                self.cout(f"Code downloaded to {output_code}")
                self.convert_to_pdf(output_code, teamname, output_pdf)
                self.cout(f"PDF generated at {output_pdf}")
                self.print_from_pdf(output_pdf)
                self.cout(f"Task completed")
                return True
        except Exception as e:
            self.cout(f"Error processing task {task}: {e}")
        finally:
            self.job_context = {}
        return False

if __name__ == "__main__":
    import argparse
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Printing Worker")
    
    parser.add_argument('--host', type=str, default=os.getenv("REDIS_HOST", "localhost"), help='Redis host')
    parser.add_argument('--port', type=int, default=os.getenv("REDIS_PORT", 6379), help='Redis port')
    parser.add_argument('--db', type=int, default=os.getenv("REDIS_DB", 0), help='Redis DB')
    parser.add_argument('--password', type=str, default=os.getenv("REDIS_PASSWORD", ""), help='Redis password')
    parser.add_argument('--printers', type=str, default=os.getenv("ENABLED_PRINTERS", ""), help='Comma-separated list of enabled printers')
    
    args = parser.parse_args()

    r = redis.Redis(host=args.host, port=args.port, db=args.db, password=args.password, decode_responses=True, encoding="utf-8")
    worker = Worker(r)
    worker.run()
