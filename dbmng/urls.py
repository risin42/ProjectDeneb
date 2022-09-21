from django.urls import path, include

# from . import views
from rest_framework.routers import DefaultRouter
from .views import dbdataViewset, get_dbdata

route = DefaultRouter()
route.register("dbmng", dbdataViewset)

# dbmng_url = routers.SimpleRouter()
# dbmng_url.register(r'main', dbsViewset)
# dbmng_url.register(r'latest', get_dbs)

urlpatterns = [
    path("", include(route.urls)),
    path("latest/", get_dbdata),

]
# urlpatterns += dbmng_url.urls
