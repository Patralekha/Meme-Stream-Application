export postgres_dbname="xmeme"
export postgres_user="postgres"
export postgres_password="root1234"
export postgres_host="127.0.0.1"


python3 manage.py makemigrations
python3 manage.py migrate

exec ./manage.py runserver 8080 &
exec ./manage.py runserver 8081
