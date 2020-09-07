# commands to run the project

# creating directories for logging
mkdir -p "logs"

# starting the redis server on docker image
sudo docker stop $(sudo docker ps -q  --filter ancestor="redis:5")
sudo docker run -p 6379:6379 -d redis:5

# starting the development server
python manage.py runserver
