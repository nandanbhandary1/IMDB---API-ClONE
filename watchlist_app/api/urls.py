from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # path("list/", views.movie_list, name="movie-list"),
    # path("list/<int:pk>", views.movie_details),
    path("list/", views.WatchListAV.as_view(), name="movie-list"),
    path("list/<int:pk>", views.WatchDetailAV.as_view(), name="movie-detail"),
    path('list2/', views.WatchListGV.as_view(), name="watch-list"),
    
    path('', include(router.urls)),
    path("stream/", views.StreamPlatformListAV.as_view()),
    path("stream/<int:pk>", views.StreamPlatformDetail.as_view(),name="streamplatform-detail"),
    
    
    # path('review/', views.ReviewList.as_view(), name="review-list"),
    # path('review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),
    
    path('<int:pk>/review-create',views.ReviewCreate.as_view(), name="review-create"), # pk is movies id
    path('<int:pk>/reviews/',views.ReviewList.as_view(), name="review-list"), # All the review to a particular movie
    path('review/<int:pk>',views.ReviewDetail.as_view(), name='review-detail'), # Review of Able to get, put, delete a review 
    
    # path('reviews/<str:username>/', views.UserReview.as_view(), name='user-review-detail'),
    path('reviews/', views.UserReview.as_view(), name='user-review-detail') # filtering against query_params    
]
