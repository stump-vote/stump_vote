# create a local development build of the backend
stump_backend.up:
	docker-compose -f docker-compose.local.yml up --build -d
	docker-compose -f docker-compose.local.yml exec api python manage.py migrate

stump_backend.down:
	docker-compose -f docker-compose.local.yml down

stump_backend.createsuperuser:
	docker-compose -f docker-compose.local.yml exec api python manage.py createsuperuser
