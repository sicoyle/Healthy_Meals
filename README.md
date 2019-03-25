# CS 4398 Semester Project

## To launch the server:
Create a virtual environment
```
virtualenv -p python3 venv
```
Activate the virtual environment
```
source venv/bin/activate
```
Install dependencies to virtual environment
```
source requirements.txt
```
NOTE: You must use at least Python 3 and have *virtualenv* installed. To install *virtualenv*:
```
pip install virtualenv
```
If using for the first time, clear the database
```
./create_database.sh
```

Launch the server and go to localhost:5000 in your web browser
```
python main.py
```
