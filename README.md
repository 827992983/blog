# Yue Blog
>This is a opensource blog publishing and management platform with pthon-django-1.8.18. It support PC and mobile devices. 
>You can deploy it on apache or nginx.
### Install
1. clone source to a Linux machine.

2. install apache and python-django runtime environment.

3. configure apache 
```
<VirtualHost *:8080>

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	WSGIScriptAlias / /var/www/blog/blog/wsgi.py
	Alias /static /var/www/blog/static
	<Directory "/var/www/blog/blog/">
		<Files "wsgi.py">
			Require all granted
		</Files>
	</Directory>

	<Directory "/var/www/blog/static">
		Require all granted
	</Directory>
</VirtualHost>
```
4. init sqlite3 database

  edit initdb.py and modify init username and password.
```
python manage.py shell
import initdb
```
### interview
```
blog home： http://xxx.xxx.xxx.xxx:port/
blog management: http://xxx.xxx.xxx.xxx:port/admin
```