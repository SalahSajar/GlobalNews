from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.images import get_image_dimensions
from django.db import IntegrityError

import environ

import concurrent
from concurrent.futures import ThreadPoolExecutor

from datetime import date, timedelta, datetime
from .models import User, Topic, SavedArticle

import requests

import base64
import random
import json
import math

from gnews import GNews

google_news = GNews()

env = environ.Env()

environ.Env.read_env()

MEDIASTACK__APIKEY = env("MEDIASTACK__APIKEY")
NEWSAPI_ORG__APIKEY = env("NEWSAPI_ORG__APIKEY")
THENEWSAPI__APIKEY = env("THENEWSAPI__APIKEY")
RAPIDAPI__KEY = env("RAPIDAPI__KEY")


# Global Micro-Functionalities Handlers
def article_timeSincePublish__HANDLER(article_publishDate):
    now = datetime.now()
    formatedDate = None

    formatedDate = datetime.strptime(article_publishDate.replace(
        "T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")

    datesGap = now - formatedDate

    if datesGap.days:
        if datesGap.days >= 30:
            if math.floor(datesGap.days/30) == 1:
                return f"1 Month"
            else:
                return f"{math.floor(datesGap.days/30)} Months"
        else:
            if datesGap.days == 1:
                return f"1 Day"
            else:
                return f"{datesGap.days} Days"
    else:
        mins = math.floor(datesGap.seconds/60)

        if mins < 60:
            return f"{mins} Mins"
        else:
            hours = math.floor(mins/60)

            if hours == 1:
                return "1 Hour"
            else:
                return f"{hours} Hours, {mins%60} Mins"
    return ""


def fetch_articles__HANDLER(params, baseUrl, query, page, type):
    currentPage = 1

    try:
        if page:
            page_index = int(page)

            if page_index > 1:
                currentPage = page_index

            if page_index > 5:
                currentPage = 5
        else:
            currentPage = 1
    except ValueError:
        currentPage = 1

    if type == "topic_search":
        params["offset"] = currentPage * 20

        res = requests.get(baseUrl, params=params)

    else:
        params["page"] = currentPage

        res = requests.get(baseUrl, params=params)

    articles = None
    data = None

    if res.status_code == 200:
        totalPages = 0
        data = res.json()

        if type == "topic_search":
            if len(data["data"]):
                for article in data["data"]:
                    article["published_at"] = article["published_at"][:(
                        len(article["published_at"])-6)]

                    article["sincePublishTime"] = article_timeSincePublish__HANDLER(
                        article["published_at"])

                articles = data["data"]
                if data["pagination"]["total"] > 100:
                    totalPages = 5
                else:
                    totalPages = math.ceil(data["pagination"]["total"]/20)

                return {
                    "articles": articles,
                    "query": query,
                    "totalPages": totalPages,
                    "currentPage": currentPage
                }
            else:
                return {
                    "message": "News articles not found, ",
                    "articles": articles,
                    "query": query,
                    "totalPages": 0,
                    "currentPage": 0
                }
        else:
            if len(data["articles"]):
                for article in data["articles"]:
                    article["sincePublishTime"] = article_timeSincePublish__HANDLER(
                        article["publishedAt"])
                articles = data["articles"]

            if data["totalResults"] > 100:
                totalPages = 5
            else:
                totalPages = math.ceil(data["totalResults"]/20)

            if data["status"] == "error":
                return {
                    "message": "Something Is not right, Please be nice and don't try anything weird.",
                    "articles": articles,
                    "query": query,
                    "totalPages": 0,
                    "currentPage": 0
                }
            else:
                return {
                    "articles": articles,
                    "query": query,
                    "totalPages": totalPages,
                    "currentPage": currentPage
                }

    return {
        "message": "Something is went wrong, Please try again later.",
        "articles": articles,
        "query": query,
        "totalPages": 0,
        "currentPage": 0
    }

##################################################

# HOME PAGE VIEW COMPONENT


def index(req):
    news_articles_by_category = {
        "general": None,
        "categories": [],
        "topics": None
    }

    topics = ["general"]

    allTopics = ["sports", "science", "business",
                 "technology", "Entertainment", "health"]
    random3topics = random.sample(allTopics, 3)

    topics += random3topics

    base_url = 'https://newsdata2.p.rapidapi.com/news'

    threads = 7

    def get_character_info(topic):
        if topic == "general":
            # original top headlines endpoint
            # res = requests.get(
            #     f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_ORG__APIKEY}&pageSize=7")
            # ----------------------------------------------------------------------

            # using everything endpoint as alternative
            lastDaysDate = date.today() - timedelta(days=1)
            res = requests.get(
                f"https://newsapi.org/v2/everything?q=a&apiKey={NEWSAPI_ORG__APIKEY}&pageSize=7&sortBy=popularity&from={lastDaysDate}")
            # ----------------------------------------------------------------------

            return {
                "topic": "general",
                "results": res.json()
            }

        querystring = {"country": "us", "category": topic, "language": "en"}

        headers = {
            "X-RapidAPI-Key": RAPIDAPI__KEY,
            "X-RapidAPI-Host": "newsdata2.p.rapidapi.com"
        }

        r = requests.get(f'{base_url}', querystring, headers=headers)
        return {
            "topic": topic,
            "results": r.json()
        }

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(
            get_character_info, topic) for topic in topics}

        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
                if data["topic"] == "general":
                    trendingArticles = None

                    if data["results"]["totalResults"] > 0 and len(data["results"]["articles"]) > 0:
                        for article in data["results"]["articles"]:
                            article["sincePublishTime"] = article_timeSincePublish__HANDLER(
                                article["publishedAt"])
                        trendingArticles = data["results"]["articles"]

                    news_articles_by_category["general"] = trendingArticles
                else:
                    for article in data["results"]["results"]:
                        article["sincePublishTime"] = article_timeSincePublish__HANDLER(
                            article["pubDate"])

                    news_articles_by_category["categories"].append(data)

            except Exception as e:
                print('Looks like something went wrong:', e)

    if req.user.is_authenticated:
        currentUser = User.objects.get(
            username=req.user.username, password=req.user.password)
        currentUser_followedTopics = currentUser.followed_topics.all()

        random3FollowedTopics__STR = None

        if len(currentUser_followedTopics):
            if len(currentUser_followedTopics) > 3:
                FollowedTopics__SET = set(
                    currentUser_followedTopic.topic for currentUser_followedTopic in currentUser_followedTopics)

                random3FollowedTopics = random.sample(FollowedTopics__SET, 3)

                random3FollowedTopics__STR = ",".join(random3FollowedTopics)

            else:
                random3FollowedTopics = set(
                    currentUser_followedTopic.topic for currentUser_followedTopic in currentUser_followedTopics)

                random3FollowedTopics__STR = ",".join(random3FollowedTopics)

        return render(req, "globalNews/index.html", {
            "random3FollowedTopics": random3FollowedTopics__STR,
            "news_articles_by_category": news_articles_by_category,
            "topics": topics,
            "currentUser_followedTopics": currentUser_followedTopics
        })

    return render(req, "globalNews/index.html", {
        "news_articles_by_category": news_articles_by_category,
        "topics": topics
    })
##################################################

# SEARCH NEWS ARTICLES BY KEYWORD VIEW COMPONENT


def search_view(req):
    search_query = req.GET.get("q")
    page_param = req.GET.get("page")

    if not search_query:
        return HttpResponseRedirect(reverse("index"))

    last3DaysDate = date.today() - timedelta(days=3)

    requestParams = {
        "apiKey": NEWSAPI_ORG__APIKEY,
        "pageSize": 20,
        "q": search_query,
        "from": last3DaysDate,
        "language": "en",
    }

    results__OBJ = fetch_articles__HANDLER(
        requestParams, "https://newsapi.org/v2/everything", search_query, page_param, "keyword_search")

    if req.user.is_authenticated:

        currentUser = User.objects.get(
            username=req.user.username, password=req.user.password)

        currentUser_followed_topics_queryset = currentUser.followed_topics.all()
        currentUser_saved_article_queryset = currentUser.user_saved_articles.all()

        return render(req, "globalNews/search.html", {
            "results__OBJ": results__OBJ,
            "currentUser_saved_articles": currentUser_saved_article_queryset,
            "currentUser_followed_topics": currentUser_followed_topics_queryset
        })

    return render(req, "globalNews/search.html", {
        "results__OBJ": results__OBJ,
        "currentUser_saved_articles": None
    })
##################################################

# SEARCH TOPIC NEWS ARTICLES VIEW COMPONENT


def topic_view(req, topic):
    page_param = req.GET.get("page")

    if not topic:
        return HttpResponseRedirect(reverse("index"))

    # Original news articles topic
    # requestParams = {
    #     "apiKey": NEWSAPI_ORG__APIKEY,
    #     "pageSize": 20,
    #     "category": topic,
    #     "country": "us"
    # }

    # if topic == "world":
    #     requestParams["category"] = "general"

    # results__OBJ = fetch_articles__HANDLER(
    #     requestParams, "https://newsapi.org/v2/top-headlines", topic, page_param, "topic_search")
    # ----------------------------------------------------------------------------------------------------

    # Alternative news articles topic Solution
    todayDate = date.today()
    lastDaysDate = date.today() - timedelta(days=1)

    requestParams = {
        "access_key": MEDIASTACK__APIKEY,
        "categories": topic,
        "countries": "us",
        "date": f"{lastDaysDate},{todayDate}",
        "languages": "en",
        "limit": 20,
        "sort": "popularity"
    }

    if topic == "world":
        requestParams["categories"] = "general"

    results__OBJ = fetch_articles__HANDLER(
        requestParams, "http://api.mediastack.com/v1/news", topic, page_param, "topic_search")
    # ----------------------------------------------------------------------------------------------------

    if req.user.is_authenticated:
        currentUser = User.objects.get(
            username=req.user.username, password=req.user.password)

        currentUser_saved_article_queryset = currentUser.user_saved_articles.all()

        return render(req, "globalNews/topic.html", {
            "results__OBJ": results__OBJ,
            "currentUser_saved_articles": currentUser_saved_article_queryset
        })

    return render(req, "globalNews/topic.html", {
        "results__OBJ": results__OBJ,
        "currentUser_saved_articles": None
    })
##################################################


# SEARCH LOCAL NEWS ARTICLES VIEW COMPONENT
def local_view(req):
    page_param = req.GET.get("page")
    reset_param = req.GET.get("reset")

    if reset_param == "true":
        try:
            del req.session['user_country_name']
            return HttpResponseRedirect(reverse("local"))
        except:
            return HttpResponseRedirect(reverse("local"))

    if req.method == "GET":
        try:
            user_country_name = req.session['user_country_name']

            last2DaysDate = date.today() - timedelta(days=2)

            requestParams = {
                "apiKey": NEWSAPI_ORG__APIKEY,
                "sortBy": "popularity",
                "pageSize": 20,
                "q": user_country_name,
                "from": last2DaysDate,
                "language": "en",
            }

            results__OBJ = fetch_articles__HANDLER(
                requestParams, "https://newsapi.org/v2/everything", user_country_name, page_param, "local_news_articles")

            if req.user.is_authenticated:
                currentUser = User.objects.get(
                    username=req.user.username, password=req.user.password)

                currentUser_saved_article_queryset = currentUser.user_saved_articles.all()
                currentUser_followed_topics_queryset = currentUser.followed_topics.all()

                return render(req, "globalNews/local.html", {
                    "geolocation": user_country_name,
                    "local_news_articles": results__OBJ,
                    "currentUser_saved_articles": currentUser_saved_article_queryset,
                    "currentUser_followed_topics": currentUser_followed_topics_queryset
                })

            return render(req, "globalNews/local.html", {
                "geolocation": user_country_name,
                "local_news_articles": results__OBJ
            })

        except:
            return render(req, "globalNews/local.html", {
                "geolocation": None,
                "local_news_articles": None,
            })
    else:
        AVAILABLE_COUNTRIES_LIST = google_news.countries[0]
        country_name = req.POST["country"]

        if country_name:
            if country_name in AVAILABLE_COUNTRIES_LIST:
                req.session["user_country_name"] = country_name

                return HttpResponseRedirect(reverse('local'))
            else:
                return render(req, "globalNews/local.html", {
                    "message": "The country You choosen is not Available",
                    "geolocation": None,
                    "local_news_articles": None
                })
        else:
            return render(req, "globalNews/local.html", {
                "message": "Please choose your targeted country",
                "geolocation": None,
                "local_news_articles": None
            })
##################################################


# Logged In User Account view
@login_required(login_url="login")
def savedArticles_view(req):
    currentUser = User.objects.get(
        username=req.user.username, password=req.user.password)

    currentUser_SavedArticles = currentUser.user_saved_articles.all()

    for currentUser_SavedArticle in currentUser_SavedArticles:
        currentUser_SavedArticle.sincePublishTime = article_timeSincePublish__HANDLER(
            str(currentUser_SavedArticle.publishDate))

    return render(req, "globalNews/account/savedArticles.html", {
        "savedArticles": currentUser_SavedArticles
    })
##################################################


# Logged In User Account view
@login_required(login_url="login")
def settings_view(req):
    currentUser = User.objects.get(
        username=req.user.username, password=req.user.password)

    if req.method == "POST":
        try:
            max_size = (1024*1024)*3
            user_avatar = req.FILES["avatar"]

            w, h = get_image_dimensions(user_avatar)
            user_avatar_size = user_avatar.size

            if user_avatar_size > max_size:
                return render(req, "globalNews/account/settings.html", {
                    "currentUser": currentUser,
                    "error": "the image you tried to upload is bigger than 3mb.",
                })
            else:
                currentUser_avatar__BASE64 = base64.b64encode(
                    user_avatar.read()).decode()

                currentUser.profile_pic = currentUser_avatar__BASE64
                currentUser.save()

                req.user.profile_pic = currentUser_avatar__BASE64

        except Exception as e:
            print('Looks like something went wrong:', e)

        user_email = req.POST["email"]
        user_username = req.POST["username"]
        user_oldPassword = req.POST["oldPassword"]
        user_newPassword = req.POST["newPassword"]
        user_confirmPassword = req.POST["confirmPassword"]

        if user_email and user_email != currentUser.email:
            currentUser.update(email=user_email)

        if user_username and user_username != currentUser.username:
            currentUser.username = user_username

        if user_oldPassword:
            if check_password(user_oldPassword, currentUser.password):
                if user_newPassword and user_confirmPassword:
                    if user_newPassword == user_confirmPassword:
                        currentUser.password = make_password(user_newPassword)
                    else:
                        return render(req, "globalNews/account/settings.html", {
                            "currentUser": currentUser,
                            "error": "New Password and Password Confirmation fields don't match.",
                        })
            else:
                return render(req, "globalNews/account/settings.html", {
                    "currentUser": currentUser,
                    "error": "Old Password you entered is Incorrect."
                })
        if not user_oldPassword and (user_confirmPassword or user_newPassword):
            return render(req, "globalNews/account/settings.html", {
                "currentUser": currentUser,
                "error": "Please to change your Password you Should enter your Current Password."
            })

        if req.user.username != user_username or req.user.email != user_email or user_oldPassword or user_newPassword or user_confirmPassword:
            currentUser.save()
            return HttpResponseRedirect(reverse("login"))

    return render(req, "globalNews/account/settings.html", {
        "currentUser": currentUser,
    })
##################################################


def logout_view(req):
    logout(req)
    return HttpResponseRedirect(reverse("index"))


def login_view(req):
    if req.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]

        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(req, "globalNews/auth/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(req, "globalNews/auth/login.html")


def register_view(req):
    if req.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if req.method == "POST":
        email = req.POST["email"]
        username = req.POST["username"]

        password = req.POST["password"]
        confirmation = req.POST["confirmation"]

        if password != confirmation:
            return render(req, "globalNews/auth/register.html", {
                "message": "Passwords must Match"
            })
        else:
            try:
                registeredUser = User.objects.create_user(
                    username, email, password)
                registeredUser.save()

                login(req, registeredUser)
                return HttpResponseRedirect(reverse("index"))

            except IntegrityError:
                return render(req, "globalNews/auth/register.html", {
                    "message": "username already taken."
                })
    else:
        return render(req, "globalNews/auth/register.html")

########################################################################


# current logged user followed topics
@login_required(login_url="login")
def following_view(req):
    currentUser = User.objects.get(
        username=req.user.username, password=req.user.password)
    currentUser_followedTopics = currentUser.followed_topics.all()

    try:
        selectedTopic = req.GET["topic"]

        currentUser_followedTopics__LIST = list(
            currentUser_followedTopic.topic for currentUser_followedTopic in currentUser_followedTopics)

        if not selectedTopic.lower() in currentUser_followedTopics__LIST:
            return HttpResponseRedirect(reverse("following"))

        last3DaysDate = date.today() - timedelta(days=3)

        requestParams = {
            "apiKey": NEWSAPI_ORG__APIKEY,
            "pageSize": 20,
            "q": selectedTopic,
            "from": last3DaysDate,
            "language": "en",
        }

        selectedTopic_newsArticles = fetch_articles__HANDLER(
            requestParams, "https://newsapi.org/v2/everything", selectedTopic, 1, "keyword_search")

        if req.user.is_authenticated:
            currentUser_savedArticles = currentUser.user_saved_articles.all()

            return render(req, "globalNews/account/following.html", {
                "selectedTopic_newsArticles": selectedTopic_newsArticles["articles"],
                "savedArticles": currentUser_savedArticles,
                "selected_topic": selectedTopic,
                "followed_topics": currentUser_followedTopics
            })

        return render(req, "globalNews/account/following.html", {
            "selectedTopic_newsArticles": selectedTopic_newsArticles["articles"],
            "followed_topics": currentUser_followedTopics,
            "selected_topic": selectedTopic,
        })
    except Exception as err:
        print(err)
        return render(req, "globalNews/account/following.html", {
            "followed_topics": currentUser_followedTopics,
            "selectedTopic_newsArticles": [],
            "selected_topic": None,
        })
########################################################################


# API ENDPOINTS -- SECTION

# fetching all available countries -- ENDPOINT
def availableCountries__endpoint(req):
    if req.method == "GET":
        AVAILABLE_COUNTRIES_LIST = google_news.countries[0]

        return HttpResponse(json.dumps(AVAILABLE_COUNTRIES_LIST))
# -----------------------------------------------------------------

# Follow & Unfollow a topic -- ENDPOINT


@login_required
def followTopic__endpoint(req, topic):
    currentUser = User.objects.get(
        username=req.user.username, password=req.user.password)

    if req.method == "POST":
        try:
            followedTopic = Topic.objects.get(topic=topic.lower())
            followedTopic.delete()

            return JsonResponse({
                "type": "unfollow",
                "status": "success",
            })
        except:
            followTopic = Topic.objects.create(
                topic=topic.lower(), follower=currentUser)
            followTopic.save()

            return JsonResponse({
                "type": "follow",
                "status": "success",
            })
# -----------------------------------------------------------------

# save article -- ENDPOINT


@login_required
def saveNewsArticle__endpoint(req):
    currentUser = User.objects.get(
        username=req.user.username, email=req.user.email)

    if req.method == "POST":
        body = json.loads(req.body)

        title = body["title"]
        description = body["description"]
        articleUrl = body["articleUrl"]
        thumbnailUrl = body["thumbnail"]
        publishDate = datetime.strptime(body["PublishmentDate"].replace(
            "T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
        source = body["source"]

        try:
            existing_saved_news_article = SavedArticle.objects.get(
                saver=currentUser, title=title, source=source)
            existing_saved_news_article.delete()

            return JsonResponse({
                "type": "unsaved",
                "status": "success",
                "message": "The request has been resolved successfully"
            })
        except:
            sa = SavedArticle.objects.create(saver=currentUser, title=title, description=description,
                                             articleUrl=articleUrl, thumbnailUrl=thumbnailUrl, publishDate=publishDate, source=source)
            sa.save()

            return JsonResponse({
                "type": "saved",
                "status": "success",
                "message": "The request has been resolved successfully"
            })


@ login_required
def unsaveNewsArticle__endpoint(req):
    currentUser = User.objects.get(
        username=req.user.username, email=req.user.email)

    if req.method == "POST":
        body = json.loads(req.body)

        title = body["title"]
        source = body["source"]

        try:
            existing_saved_news_article = SavedArticle.objects.get(
                saver=currentUser, title=title, source=source)
            existing_saved_news_article.delete()

            return JsonResponse({
                "status": "success",
                "message": "this news article is unsaved successfully."
            })
        except:
            return JsonResponse({
                "status": "error",
                "message": "this news article is already unsaved"
            })

# -----------------------------------------------------------------


@login_required
def followedTopicArticles__endpoint(req, topic):
    base_url = "https://api.thenewsapi.com/v1/news/top"

    date10daysBefore = date.today() - timedelta(days=10)

    params = {
        "api_token": THENEWSAPI__APIKEY,
        "language": "en",
        "search": topic,
        "limit": 4,
        "published_after": date10daysBefore,
        "search_fields": "title,description,keywords",
        "sort": "relevance_score"
    }

    res = requests.get(base_url, params=params)

    if res.status_code == 200:
        data = res.json()

        if data["data"]:
            followedTopic_newsArticles = data["data"]

            for followedTopic_newsArticle in followedTopic_newsArticles:
                formatted_PubDate = datetime.strptime(
                    followedTopic_newsArticle["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

                followedTopic_newsArticle["sincePubTime"] = article_timeSincePublish__HANDLER(
                    str(formatted_PubDate))

            return JsonResponse({
                "status": "success",
                "topic": topic,
                "articles": followedTopic_newsArticles
            })
        else:
            return JsonResponse({
                "status": "error",
                "articles": []
            })
