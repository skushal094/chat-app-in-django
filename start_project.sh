# commands to run the project

sudo docker stop $(sudo docker ps -q  --filter ancestor="redis:5")
sudo docker run -p 6379:6379 -d redis:5
python manage.py runserver
