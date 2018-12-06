Steps to run :
1. pip install -r requirements.txt
2. Set Environmental Variables as:
    export FLASK_CONFIG=development
    export FLASK_APP=run.py
    export SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password123@localhost/test
    export SECRET_KEY=2b20f139aadd936dd71ae7bd2a9e46ca62a6473e3c09d153
    export MAIL_USERNAME=<your email>
    export MAIL_PASSWORD=<your password>
    
3. flask db init
   flask db migrate
   flask db upgrade
4. Finally run app on port 5000: 
    flask run
    

