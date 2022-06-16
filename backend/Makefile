run:
	./manage.py runserver

clean:
	rm -rf __pycache__
	rm db.sqlite3
	./manage.py makemigrations accounts tweets
	./manage.py migrate
	./manage.py createsuperuser