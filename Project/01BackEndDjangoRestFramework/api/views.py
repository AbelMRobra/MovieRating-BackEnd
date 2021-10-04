from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.models import Movie, Rating
from api.serializaers import MovieSerializers, RatingSerializers, UserSerializers

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializers

class MovieViewSet(viewsets.ModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=["POST"])
    def rate_movie(self, request, pk=None):
        if "stars" in request.data:

            movie = Movie.objects.get(id = pk)
            stars = request.data["stars"]
            user = request.user
            #user = User.objects.get(id = 1)

            try:
                rating = Rating.objects.get(user = user, movie = movie)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializers(rating, many=False)
                response = {'massege': 'Rating updated', 'result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            except:

                rating = Rating.objects.create(user = user, movie = movie, stars = stars)
                rating.save()
                serializer = RatingSerializers(rating, many=False)
                response = {'massege': 'Rating created', 'result':serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)

            

        else:

            response = {'massege': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):

        response = {'massege': 'You cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):

        response = {'massege': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)