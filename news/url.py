from django.urls import path
from .views import NewsList, NewsDetail, SearchList, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, CategoryView, subscribe_from_category, unsubscribe_from_category

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view()),
    path('search/', SearchList.as_view()),
    path('news/<int:pk>/', PostDetailView.as_view(), name='news_detail'),
    path('news/add/', PostCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='news_create'),
    path('news/delete/<int:pk>/',PostDeleteView.as_view(), name='news_delete'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>/', subscribe_from_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_from_category, name='unsubscribe'),

]