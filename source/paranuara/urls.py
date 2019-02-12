"""takehome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from paranuara.views import CompanyEmployeesView, PeopleCompareView, PeopleFavoriteFoodView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^v1/company/(?P<company_id>\d+)/employees/$', CompanyEmployeesView.as_view(), name='v1.company-employees'),
    url(r'^v1/people/(?P<people_id>\d+)/compare/(?P<other_people_id>\d+)/$', PeopleCompareView.as_view(), name='v1.people-compare'),
    url(r'^v1/people/(?P<people_id>\d+)/favorite-food/$', PeopleFavoriteFoodView.as_view(), name='v1.people-favorite-food'),
]
