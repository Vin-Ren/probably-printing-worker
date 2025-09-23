# Probably printing worker
This worker is created with association to [kevincornellius/probably-printing](https://github.com/kevincornellius/probably-printing).

### Easier Usage
Simply run:
```sh
./runner.sh
```
This will prompt you to create a virtual environment if you didn't have one yet. After which, the app is started. You can even pass arguments to this script, which will then be forwarded to the main.py app.

### Install dependencies
```sh
sudo apt-get update
sudo apt-get install libcups2-dev libcairo2 pango1.0-tools libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-dejavu
sudo apt-get install cups cups-pdf
```
By default this will install the pdf driver for cups, i.e. printing to a file. This is useful for testing purposes, and if you are a developer, you can change the output path of this printer with `sudo nano /etc/cups/cups-pdf.conf`.

# Installing python dependencies
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```


### Usage:
**Recommended**: Populate .env with your configurations, example is provided in [.env.example](./.env.example)
If not, you need to supply the args everytime you run the worker/client.

Then to run the worker:
```sh
python3 main.py
```

To do some local testing, simply run another script alongside the worker:
```sh
python3 local_client.py
```

---
Happy printing!
