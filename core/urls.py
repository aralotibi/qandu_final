from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^school/create/$', login_required(SchoolCreateView.as_view()) , name='school_create'),
    url(r'^school/$', login_required(SchoolListView.as_view()) , name='school_list'),
    url(r'^school/(?P<pk>\d+)/$', login_required(SchoolDetailView.as_view()) , name='school_detail'),
    url(r'^school/update/(?P<pk>\d+)/$', login_required(SchoolUpdateView.as_view()) , name='school_update'),
    url(r'^school/delete/(?P<pk>\d+)/$', login_required(SchoolDeleteView.as_view()) , name='school_delete'),
    url(r'^school/(?P<pk>\d+)/review/create/$', login_required(ReviewCreateView.as_view()) , name='review_create'),
    url(r'^school/(?P<school_pk>\d+)/review/update/(?P<review_pk>\d+)/$', login_required(ReviewUpdateView.as_view()) , name='review_update'),
    url(r'^school/(?P<school_pk>\d+)/review/delete/(?P<review_pk>\d+)/$', login_required(ReviewDeleteView.as_view()) , name='review_delete'),
    url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
    url(r'^user/(?P<slug>\w+)/$', login_required(UserDetailView.as_view()), name='user_detail'),
    url(r'^user/update/(?P<slug>\w+)/$', login_required(UserUpdateView.as_view()),  name='user_update'),
    url(r'^user/delete/(?P<slug>\w+)/$', login_required(UserDeleteView.as_view()), name='user_delete'),
    url(r'^search/$', login_required(SearchSchoolListView.as_view()), name='search'),

)