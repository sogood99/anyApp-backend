init:
	make migrate
	./manage.py createsuperuser

migrate:
	./manage.py makemigrations accounts tweets
	./manage.py migrate

run:
	./manage.py runserver

clean:
	rm -rf __pycache__
	rm -rf migrations
	rm -rf ./media/image/tweet/*
	mv ./media/image/userBkgImg/default.jpg media/image/default.jpg 
	rm -rf ./media/image/userBkgImg/*
	mv media/image/default.jpg ./media/image/userBkgImg/default.jpg
	mv ./media/image/userIcon/default.jpg media/image/default.jpg 
	rm -rf ./media/image/userIcon/*
	mv media/image/default.jpg ./media/image/userIcon/default.jpg
	rm -f db.sqlite3
	make init