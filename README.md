# Probably printing worker
This worker is created with association to [kevincornellius/probably-printing](https://github.com/kevincornellius/probably-printing).

This worker uses CUPS to print files, as such, it only supports unix based system (Though you might be able to use WSL for this in some cases).

### Easier Usage
Copy .env.example to .env and populate it as required. Then simply run:
```sh
./runner.sh
```
This will install required dependencies and prompt you to create a virtual environment if you didn't have one yet. After which, the app is started. You can even pass arguments to this script, which will then be forwarded to the main.py app.

### Installing a printer
You can do this via a shell or the webUI. However, it is easier to manage CUPS via the built-in webUI. So make sure to add your linux user to the lpadmin group with `sudo usermod -aG lpadmin <your-username-here>` (without the square brackets).
Then you can visit the webUI at [http://localhost:631/](http://localhost:631/).


To add a new printer, go to the 'Administration' tab, enter your username and password for the user you have previously added to the lpadmin group here. Then under Printers section, click `Add Printer`, select your printer, click Continue and follow the instructions.


**This worker runs on all available printers on default and supports scheduling between them**. To only run on some subset of the available printers, pass the names of that subset of printers in a comma seperated values like this `./runner.sh --printers printer1,printer2,printer3`. To get the names, run `./runner.sh --list-printers`, which should produce an output similiar to below:
```
Available printers:
  - PDF: idle | Location:  | Model: Generic CUPS-PDF Printer (w/ options)
```
The printer name is the first string before the column, in this case its `PDF`.
To run the worker only on this printer, simply run `./runner.sh --printers PDF`.


### Note for usage
In case of unintentional or intentional malicious job submissions, you can head to the [Jobs tab](http://localhost:631/jobs/) and cancel the job manually from there.

---



### Install dependencies
```sh
sudo apt-get update
sudo apt-get install libcups2-dev libcairo2 pango1.0-tools libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-dejavu
sudo apt-get install cups cups-pdf
```
By default this will install the pdf driver for cups, i.e. printing to a file. This is useful for testing purposes, and if you are a developer, you can change the output path of this printer with `sudo nano /etc/cups/cups-pdf.conf`.

### Installing python dependencies
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
