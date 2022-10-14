To acces this projects live;
Start by installing the dependencies in requirements.txt
By running pip install -r requirements.txt after creating a virtual env.
make connection to the suitable database on any chosen server
Or use mysqlite for local testing by changing the default database at the settings
Run python manage.py makemigrations to be sure all database tables are initiated


make sure the migrations of the database table is completed succesfully
By running python manage.py migrate

A live copy of this project is here at;
http://BookAppTest.pythonanywhere.com with mySQL database at backend
