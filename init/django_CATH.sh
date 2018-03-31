rm django_CATH -rf

virtualenv django_CATH --python=python2.7

cd django_CATH 

source bin/activate

pip install Django==1.11.*

django-admin startproject rootsite

cat ../django_settings.py >> rootsite/rootsite/settings.py
cat ../django_urls.py >> rootsite/rootsite/urls.py


# sudo apt-get -qq update
sudo apt-get install -y libmysqlclient-dev

### Configure sql correspondingly using django_CATH.sql

#mkdir django
cd rootsite

### clone django_CATH from local
git clone $repos/cathdb/django_CATH tst;


cd tst 
pip install -r requirements.txt

cd ..

./manage.py migrate
#./manage.py loaddata --app tst cathB-0728-WithStat.json 

./manage.py runserver 0.0.0.0:8001

