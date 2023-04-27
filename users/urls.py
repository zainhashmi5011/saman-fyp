"""fyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.UserAuthView.as_view({
        "post": "signup"
    })),
    path('login/', views.UserAuthView.as_view({
        "post": "login"
    })),
    path('select-template/', views.TemplateView.as_view({
        "post": "select_template"
    })),
    path('profile/', views.ProfileView.as_view({
        "get": "get_profile",
        "patch": "update_profile"
    })),
    path('education/', views.EducationView.as_view({
        "post": "create_education",
        "get": "get_education",
    })),
    path('awards/', views.AwardsView.as_view({
        "post": "create_awards",
        "get": "get_awards",
    })),
    path('achievement/', views.AchievementView.as_view({
        "post": "create_achievement",
        "get": "get_achievement",
    })),
    path('job/', views.JobView.as_view({
        "post": "create_job",
        "get": "get_job",
    })),
    path('blog/', views.BlogView.as_view({
        "post": "create_blog",
        "get": "get_blog",
    })),

    path('funding/', views.FundingView.as_view({
        "post": "create_funding",
        "get": "get_funding",
    })),

    path('picture/', views.PicturesView.as_view({
        "post": "create_pictures",
        "get": "get_pictures",
    })),

    path('collaboration/', views.CollaborationView.as_view({
        "post": "create_collaboration",
        "get": "get_collaboration",
    })),
    path('academic/', views.AcedemicView.as_view({
        "post": "create_academic",
        "get": "get_academic",
    }))
]
