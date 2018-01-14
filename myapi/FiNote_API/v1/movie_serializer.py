from rest_framework import serializers
from FiNote_API.models import *


class UpdateDVDFAVSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False, allow_null=False, required=True)
    password = serializers.CharField(max_length=256, allow_blank=False, required=True)
    tmdb_id = serializers.IntegerField(allow_null=False, required=True)
    dvd = serializers.BooleanField(required=True)
    fav = serializers.BooleanField(required=True)


class AddMovieSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False, allow_null=False, required=True)
    password = serializers.CharField(max_length=256, allow_blank=False, required=True)
    title = serializers.CharField(allow_blank=False, allow_null=False, required=True)
    overview = serializers.CharField(allow_blank=False, allow_null=False, required=True)
    tmdb_id = serializers.IntegerField(allow_null=False, required=True)
    poster = serializers.CharField(max_length=512, allow_blank=False, required=True)
    genre = serializers.ListField(allow_null=False, required=True)
    onomatopoeia = serializers.ListField(allow_null=False, required=True)
    dvd = serializers.BooleanField(required=True)
    fav = serializers.BooleanField(required=True)


class UpdateOnomatopoeiaSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False, allow_null=False, required=True)
    password = serializers.CharField(max_length=256, allow_blank=False, required=True)
    tmdb_id = serializers.IntegerField(allow_null=False, required=True)
    onomatopoeia = serializers.ListField(allow_null=False, required=True)


class DeleteMovieSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False, allow_null=False, required=True)
    password = serializers.CharField(max_length=256, allow_blank=False, required=True)
    tmdb_id = serializers.IntegerField(allow_null=False, required=True)



#
#
# class GetUsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AuthUser
#         fields = ('username',)
#
#
# class GetGenresSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = ('name',)
#
#
# class GetOnomatopoeiaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Onomatopoeia
#         fields = ('name',)
#
#
# class GetMoviesSerializer(serializers.ModelSerializer):
#     genre = GetGenresSerializer(many=True)
#     user = GetUsersSerializer(many=True)
#     onomatopoeia = GetOnomatopoeiaSerializer(many=True)
#
#     class Meta:
#         model = Movie
#         fields = ('title', 'tmdb_id', 'genre', 'user', 'onomatopoeia')
#
#
# class GetOnomatopoeiaCountSerializer(serializers.ModelSerializer):
#     onomatopoeia = GetOnomatopoeiaSerializer(many=False)
#     movie = GetMoviesSerializer(many=False)
#
#     class Meta:
#         model = OnomatopoeiaCount
#         fields = ('count', 'onomatopoeia', 'movie')
#
#

#
#
# class GetMovieByAgeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = ('title', 'overview', 'poster_path')
#
#
# class GetMovieReactionSerializer(serializers.Serializer):
#     tmdb_id_list = serializers.CharField(allow_null=False, required=True)
#
#
# class GetMovieByOnomatopoeiaSerializer(serializers.Serializer):
#     onomatopoeia_name = serializers.CharField(max_length=100, allow_null=False, required=True, allow_blank=False)
#
#

#
#
# class GetSearchMovieTitleResultsSerializer(serializers.Serializer):
#     movie_title = serializers.CharField(allow_null=False, required=True)
#     page_number = serializers.IntegerField(allow_null=False, required=True)
#
#
# class GetOriginalTitleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(allow_null=False, required=True)
#
#
# class GetOnomatopoeiaCountByMovieIDSerializer(serializers.Serializer):
#     tmdb_id = serializers.CharField(allow_null=False, required=True)
#     onomatopoeia_name_list = serializers.CharField(allow_null=False, required=True)
