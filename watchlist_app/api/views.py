from django.shortcuts import get_object_or_404
from watchlist_app.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreteThrottle, ReviewListThrottle
import django_filters.rest_framework
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination




"""filter against curr user """
class UserReview(generics.ListAPIView): # Find Reviews for a particular user
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username) # foreign key__name only for foreign key
# in frontend they're gonna send the form take somei i/p, put the input in the link send the req and we are gonna send the response


    def get_queryset(self):
        username = self.request.query_params.get('username', None) # insted of mapping val map query param
        return Review.objects.filter(review_user__username=username)

"""model Viewset"""
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]




""" View Sets"""

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist, context={'request': request})
#         return Response(serializer.data)
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     def delete(self, request, pk):
#         Stream = StreamPlatform.objects.get(pk=pk)
#         Stream.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

""" Generic Views"""

class ReviewCreate(generics.CreateAPIView): # SUBMIT A NEW REVIEW TO A PARTICULAR MOVIE only post
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreteThrottle]
    # DRF generic views require a queryset Even though you’re not listing data It is used internally for consistency
    def get_queryset(self):
        return Review.objects.all()
    
# whenever a new object is created it comes here    
    def perform_create(self, serializer): # overwite create, whenever we try to create new obj, perform_create usually calls this behind the scene and pass our own requirement, perform_update and perform_destroy
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        # check whether the user has already set the review for the particular movie
        review_user = self.request.user
        review_queryset = Review.objects.filter(whatslist=movie, review_user=review_user) # “Has THIS user already reviewed THIS movie?”
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewe this movie broo!")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
            
        movie.number_rating += 1
        movie.save()
        
        serializer.save(whatslist=movie, review_user=review_user)
        


class ReviewList(generics.ListAPIView): # Non pk. GIVES U ALL THE REVIEWS OF A PARTIULAR MOVIE
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all() # It will give all the movie id
    serializer_class = ReviewSerializer
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ReviewListThrottle]
    # throttle_classes=[ScopedRateThrottle]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk'] # Select pk and kwargs bcz everything is inside that
        return Review.objects.filter(whatslist=pk) # watchlist is field name in model which holds id 
        
# self.kwargs = {'pk': 7}
# pk = self.kwargs['pk']  # pk = 7

    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):  # pk, GIVES U DETAIL OF SINGLE REVIEW AMONG ALL THE REVIEW
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [AdminOrReadOnly]
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


""" Mixins"""


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


"""APIVIEW"""

class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"Error": "Not found"}, status=status.HTTP_204_NO_CONTENT)
        serializer = StreamPlatformSerializer(stream, context={"request": request})  # context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"Error": "Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


""" Filter searching and ordering (only fot testing purpose)"""

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination
    # ordering = ['created']
    
    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['title', 'platform__name']
    
    
    # filter_backends = [filters.SearchFilter]
    # filter_fields = ['=title', 'platform__name']
    
    
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
   


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"Error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

                 
@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == "GET":
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = WatchListSerializer(data=request.data) # GET DATA FROM USER, USER IS SENDING SOME INFO STORE IT IN DB
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["GET","PUT", "DELETE"])
def movie_details(request, pk):
    if request.method == "GET":
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    if request.method == "PUT": # SOMEONE IS SENDING THE DATA
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
