from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("local", views.local_view, name="local"),
    path("search", views.search_view, name="search"),
    path("topic/<str:topic>", views.topic_view, name="topic"),
    path("library", views.following_view, name="following"),
    path("savedArticles", views.savedArticles_view, name="savedArticles"),
    path("settings", views.settings_view, name="settings"),


    # Authentication Endpoint
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),


    # API Endpoints
    path("availableCountries", views.availableCountries__endpoint,
         name="availableCountries"),
    path("save_newsArticle", views.saveNewsArticle__endpoint, name="saveNewsArticle"),
    path("unsaveNewsArticle", views.unsaveNewsArticle__endpoint,
         name="unsaveNewsArticle"),
    path("followTopic/<str:topic>",
         views.followTopic__endpoint, name="followTopic"),
    path("followedTopic/<str:topic>",
         views.followedTopicArticles__endpoint, name="followedTopicArticles"),
]
