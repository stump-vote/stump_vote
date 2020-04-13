from rest_framework import routers
from api import views
from django.urls import path, include

router_v0 = routers.SimpleRouter()
router_v0.register(r'samples', views.SampleViewSet, 'sample')
router_v0.register(r'candidates', views.BoulderCandidatesViewSet, 'candidate')
router_v0.register(r'demonewsitems', views.NewsfeedDemoItemViewSet, 'demonewsitem')

urlpatterns = [
    path('v0/', include(router_v0.urls)),
    path('v0/somedata/', views.SomeDataView.as_view(), name='somedata'),
    # path('v0/frontend/', views.ZackDataView.as_view(), name='frontend'),
]
