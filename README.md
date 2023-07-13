# Flask_social_media
## Requirement Features
```
* Create a social media website that has the following features:
    > user login,logout and registration system (using login_manager)
    > secure database record insertion
    > website has at least 5 pages (login,register,home,profile,friend requests)
    > user can do the following :
        > post new posts ( set privacy to friends only or Public or only me)
        > view other users' posts with 2 modes : friends only or All posts
        > view other users account and add them as friends
        > delete posts
        > update posts
        > update user's own info
```
## Demo Project
https://youtu.be/CREVECnXTY4

## Image Demo 

> profile page

![screencapture-127-0-0-1-5000-profile-2023-07-13-19_39_19](https://github.com/mahmoudramadan0040/Social-App/assets/95087747/f2311131-a426-4517-9e42-4625ca9f078c)

> login page

![Capture2](https://github.com/mahmoudramadan0040/Social-App/assets/95087747/fa5bfe06-e99a-488a-b343-69679ede0791)

> register page

![Capture3](https://github.com/mahmoudramadan0040/Social-App/assets/95087747/73ae8584-af77-447f-b63a-4e73913c5294)

> home without login

![Capture4](https://github.com/mahmoudramadan0040/Social-App/assets/95087747/010a208d-5cd7-4d29-87f2-179c533e150b)

> home after login

![Capture](https://github.com/mahmoudramadan0040/Social-App/assets/95087747/167e9475-d211-4278-90b3-0471acd8b41a)

> explore friends ( you can make friend request )

![Capture5](https://github.com/mahmoudramadan0040/Social-App/assets/95087747/d07c3e74-72a3-42fb-adcf-cef627327ef9)

> friend requests

![Capture6](https://github.com/mahmoudramadan0040/Social-App/assets/95087747/8010a5d7-efac-44b3-875e-468d48ca4cd0)

## How To run 
1- create virtual environment using this command 
```
     pip install virtualenv
     python<version> -m venv [virtual-environment-name]
```
2- then activate this environment using this command 
```
    . venv/Scripts/activate
```
3- install all requirement pakage using this command
```
     pip install -r requirements.txt
```
4- add .env file then add this inside
```
     FLASK_APP=start.py
     FLASK_DEBUG=1
```
5- change connect string that inside __init__ file in project to connect string your Db
```
     'postgresql://postgres:[password]@localhost:5432/[your-database-name ]'
```
6- run this file to create database 
```
    python run_db create_db
```
7- finally run this command to run project 
```
    flask run 
```
