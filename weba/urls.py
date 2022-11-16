"""badminton URL Configuration

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
from recap_match import views

urlpatterns = [
    path('', views.login),
    path('login', views.login, name='login'),
    path('signin', views.signin, name='signin'),
    path('recap', views.recap, name='recap'),
    path('delete_player', views.delete_player, name='delete_player'),
    path('delete_eleve/<id_eleve>', views.delete_eleve, name='delete_eleve'),
    path('recap_updating/<id_eleve>', views.recap_updating, name='recap_updating'),
    path('load_matchs/<id_eleve>', views.load_matchs, name='load_matchs'),
    path('load_infos_match/<id_eleve>/<id_match>', views.load_infos_match, name='load_infos_match'),
    path('load_echanges_match/<id_eleve>/<id_match>', views.load_echanges_match, name='load_echanges_match'),
]
