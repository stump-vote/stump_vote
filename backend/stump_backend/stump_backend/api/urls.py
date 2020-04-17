from rest_framework import routers
from api import views
from django.urls import path, include
from knox.views import LogoutView, LogoutAllView

router_v0 = routers.SimpleRouter()
router_v0.register(r'samples', views.SampleViewSet, 'sample')
router_v0.register(r'candidates', views.BoulderCandidatesViewSet, 'candidate')
router_v0.register(r'demonewsitems', views.NewsfeedDemoItemViewSet, 'demonewsitem')

urlpatterns = [
    path('v0/', include(router_v0.urls)),
    path('v0/somedata/', views.SomeDataView.as_view(), name='somedata'),
    # path('v0/frontend/', views.ZackDataView.as_view(), name='frontend'),
    path('user/', views.UserAPIView.as_view(), name='user_api_view'),
    path('login/', views.LoginView.as_view(), name='knox_login'),   # Override
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', LogoutAllView.as_view(), name='knox_logoutall')
]
