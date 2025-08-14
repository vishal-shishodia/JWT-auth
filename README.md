# Django Auth (JWT + Middleware)

## Tech Stack
Python3.10
Django==5.2.5
djangorestframework==3.16.1
Postgresql

## Setup
git clone <repo>
cd <project-name>
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

## to input dummy user data into the database
python manage.py seed_users


## Auth header
Authorization: Bearer <access-token>

## Design Decision
Custom User Model - Requires users to provide a valid email, password, and other essential details during registration.
Middleware - Middleware is configured to restrict access to routes such as api/admin and other role-specific endpoints if request from other role type user.
JWT Token - Access token life - 60 mins
            Refresh toke life - 1 day

User Flow - 
    Currently following roles are considered - 
        Admin, Legal, PM, Sales

On sign up - 
  -Users must provide email, password, and role.
  -Optional details include first name, last name, and mobile number.

User details - 
    Users can view and update their own profile information.

## API testing
1. Register a user - /api/register
2. login - /api/login
3. Get a profile - /api/profile
            this will return the profile data for the logged in user
4. Update the user profile - /api/profile PUT
            this will update the profile data for the logged in user
5. Get the data of all the user if Admin - api/admin/users
            this will return the profile details of all the user
