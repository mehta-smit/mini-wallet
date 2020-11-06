# mini-wallet
A virtual wallet developed using the Django Rest API Framework.

## Setup mini-wallet
### Required steps to run services

#### Git clone repo
> - [x] ```git clone https://github.com/mehta-smit/mini-wallet.git ~/mini-wallet```
> - [x] ```cd ~/mini-wallet```

#### Create Virtualenv
> - [x] ```virtualenv ~/virt/mini-wallet -p python3```

#### Activate Virtualenv
> - [x] ```source ~/virt/mini-wallet/bin/activate```

#### Install Required PIP Packages
> - [x] ```pip install -U -r requirements.txt```


## Setup DB
#### Setup Database using Django ORM
> - [x] ```cd ~/mini-wallet/mini_wallet```
> - [x] ```python manage.py makemigrations.py```
> - [x] ```python manage.py migrate```
> - [x] ```python manage.py sqlmigrate wallet 0001```
> - [x] ```python manage.py migrate```

### Start Service
> - [x] ```python manage.py runserver```


### Create A superuser for Django Admin Panel
#### To access the DB Tables and manipulate it's data from Admin Panel.
> - [x] ```python manage.py createsuperuser```

 
##### As you can see now wallet.sqlite3 file is created for our DB Operations.
##### Time to spare this.!!

## Import Postman Collection Using Below Link.
https://www.getpostman.com/collections/805c23fa94f778885969


