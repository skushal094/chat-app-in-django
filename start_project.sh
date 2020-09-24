# commands to run the project

# creating directories for logging
mkdir -p "logs"

# starting the redis server on docker image
DOCKER_STATUS=$(sudo docker ps -q  --filter ancestor="redis:5")

if [ -z "$DOCKER_STATUS" ]
then
	echo "Docker image for redis is not running"
	echo "Starting the docker redis container"
	echo "Redis container is started with id" "$(sudo docker run -p 6379:6379 -d redis:5)"
else
	echo "Docker container for redis is already running."
fi

# starting the development server
python manage.py runserver
