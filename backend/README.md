# flask_quitz
flask app for quitz gaming

### For Backend
- install redis server using `sudo apt install redis-server`
- install sqlite db using `sudo apt install sqlite3 libsqlite3-dev`
- update settings.py `DB_PATH='your_valid_path_to_db'`
- create virtual environment using python3
- install requirements using `pip install -r requirements.txt` inside your virtual environment
- run the file as `bash run.sh` to run the project
- run the file as `bash celery.sh` to run background task
 
 
 ### For FrontEnd
 - Make sure you already have node and npm
 - go to frontend directory
 - run `yarn add` command
 - run `yarn start`