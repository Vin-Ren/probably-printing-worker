# Probably printing worker
This worker is created with association to [kevincornellius/probably-printing](https://github.com/kevincornellius/probably-printing).

Install dependencies:
```sh
sudo apt-get update
sudo apt-get install libcups2-dev libcairo2 pango1.0-tools libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-dejavu
sudo apt-get install cups cups-pdf

# Installing python dependencies
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

