bogus_glasses
=============

This should install the program on a fresh ubuntu 14 install and start it running on port 80. First install system packages. The second line are optional packages... they may have different names on your distro and if so don't worry about it. Starting as root:

```
apt-get update
apt-get install git python-dev nginx uwsgi python-pip uwsgi-plugin-python node-less -y
apt-get install libjpeg-dev zlib1g-dev -y
```

The only one I'm worried about is node-less, which is used to compile the css. If this won't install then hit me up and I'll commit a compiled version of the css to the repository.

Make a django user, then cd to his home. The second line gives django sudo powers.

```
adduser django #you'll be prompted for shit here
usermod -aG sudo django
su django
cd
```

Next clone the repository

```
git clone https://github.com/chriscauley/eye_pi.git
cd eye_pi
```

Install all python packages. 

`sudo pip install -r scripts/requirements.txt`

Now syncdb. You'll be asked to make a superuser and you should. If not you can make one later with `python manage.py createsuperuser`. Also collect static files

```
python manage.py syncdb
python manage.py collectstatic
```

Find out what directory you are in, this will be needed in a million places after this:

`pwd`

It should be /home/django/eye_pi/, if not you'll see references to that which you'll need to change.

```
sudo rm /etc/nginx/sites-enabled/default 
sudo ln -s /home/django/eye_pi/scripts/nginx.conf /etc/nginx/sites-enabled/
```

Next add this line to /etc/rc.local above `exit 0`

`su django -c 'bash /home/django/eye_pi/scripts/uwsgi.sh' &`

And that should be it! Restart your pi and it should be running nginx which points to a uwsgi instance which is running eye_pi.
