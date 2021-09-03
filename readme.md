**Step one**   
Download source  
https://github.com/israelomotayo/flask-practice  

**Step two**  
create venv  
`python -m venv venv`

**Step three**  
Activate venv windows: `venv\Scripts\activate`  
Mac: `source venv/bin/activate`  

**Step four**  
Install requirements: `pip install -r requirements.txt`  

**Step five**  
run flask: `flask run`  

**Install Database plugins**  
`pip install flask-sqlalchemy `  
`pip install flask-migrate `  

Initializing the database  
`flask db init`

Updating changes  
`flask db migrate`  
`flask db upgrade` 