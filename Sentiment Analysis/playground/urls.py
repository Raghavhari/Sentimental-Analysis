from django.urls import path
from . import views

#url config
urlpatterns = [
    path('',views.get_input),
    path('analyze/', views.analyze_sentiment, name='analyze_sentiment'),
]
