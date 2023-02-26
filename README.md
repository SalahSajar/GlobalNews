# GlobalNews

GlobalNews is mobile-responsive news web application where you can stay up to date with trending global news and news topics that interest you.

In GlobalNews you can create your account that allows you to save news articles for later and share your favorite news articles on social media, creating your account in GlobalNews also allows you to follow your favorite topics for easier access.

## Complexity & Distinctiveness

GlobalNews is a multi-pages web application structured to make it easy for the user to navigate through the website.

Logged in users are allowed to change their username, email, password and profile avatar under weight and size requirements, and give them a pleasant experience doing so and that by dealing with each possible situation.

GlobalNews uses 3 different External APIs to extract different news articles and structures each API's data for the targeted goal, and uses client-side and server-side rendering to fetch data, something we didn't see in any CS50w project.

## Files Structure

```
├── capstone/ -> core project
│   ├── asgi.py -> asgi interface configuration
│   ├── settings.py
│   └── urls.py -> global urls mapping
├── globalNews/ -> application folder
│   ├── static/
│   │   └── globalNews/
│   │       ├── assets/ -> where global icons and images are stored
│   │       ├── js/
│   │       │   └── main.js -> main javascript file for client-side interactions
│   │       └── scss/
│   │           ├── style.css -> compiled version of scss file
│   │           └── style.scss -> global styles scss file
│   ├── templates/
│   │   └── globalNews
│   │       └── account/ -> specific templates for logged in users
│   │           ├── following.html -> to view all followed topics by logged in user
│   │           ├── settings.html -> to change user account details
│   │           └── savedArticles.html -> to view all saved articles
│   │       └── auth/
│   │           ├── login.html login template
│   │           └── register.html register template
│   │       ├── index.html -> home template
│   │       ├── layout.html -> main web app layout
│   │       ├── local.html -> to search for news articles by countries
│   │       ├── search.html -> to search for news articles by keywords
│   │       └── topic.html -> to view news articles by categories
│   ├── templatetags/ -> custom template filters and tags
│   │       ├── searchForExistence.py -> to check if news article is saved by current logged in user
│   │       ├── split.html -> to split string by passed key
│   │       └── times.html -> to specify for-in looping times
│   ├── admin.py
│   ├── apps.py
│   ├── models.py -> web application database models
│   ├── urls.py -> web application endpoints
│   └── views.py -> web application endpoints views
├── manage.py
└── README.md -> readme file with the instructions
└── requirements.txt -> file that contains the project dependencies
```

## How to Run

```
1- First of all let's clone the repository:
git clone https://github.com/me50/SalahSajar.git

2- Open Project Folder

3- Install necessary python packages
pip install -r requirements.txt

4- apply the migrations
python manage.py makemigrations
python manage.py migrate

5- you're ready to start the application
python manage.py runserver

```
