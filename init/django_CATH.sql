-- GRANT ALL PRIVILEGES ON * . * TO 'django'@'localhost';

create database django character set utf8;
grant all privileges on django.* to 'django'@'localhost' identified by 'Django_passw0rd';

create database mtest_django character set utf8;
grant all privileges on mtest_django.* to 'django'@'localhost' identified by 'Django_passw0rd';

create database test_django character set utf8;
grant all privileges on test_django.* to 'django'@'localhost' identified by 'Django_passw0rd';
