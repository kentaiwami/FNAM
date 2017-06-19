from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'v1/signup', SignUpViewSet, 'signup')
router.register(r'v1/sign_in_with_token', SignInWithTokenViewSet, 'sign_in_with_token')
router.register(r'v1/sign_in_no_token', SignInNoTokenViewSet, 'sign_in_no_token')
router.register(r'v1/change_password', ChangePasswordViewSet, 'change_password')
router.register(r'v1/change_email', ChangeEmailViewSet, 'change_email')
router.register(r'v1/change_sex', ChangeSexViewSet, 'change_sex')
router.register(r'v1/set_profile_img', SetProfileImgViewSet, 'set_profile_img')
router.register(r'v1/movie_add', MovieAddViewSet, 'movie_add')
router.register(r'v1/onomatopoeia_update', OnomatopoeiaUpdateViewSet, 'onomatopoeia_update')
router.register(r'v1/status_update', StatusUpdateViewSet, 'status_update')
router.register(r'v1/delete_backup', DeleteBackupViewSet, 'delete_backup')
router.register(r'v1/users', UserViewSet, 'users')
router.register(r'v1/genres', GenreViewSet, 'genres')
router.register(r'v1/onomatopoeia', OnomatopoeiaViewSet, 'onomatopoeia')
router.register(r'v1/movies', MovieViewSet, 'movies')
router.register(r'v1/onomatopoeia_count', OnomatopoeiaCountViewSet, 'onomatopoeia_count')
router.register(r'v1/get_recently_movie', GetRecentlyMovieViewSet, 'get_recently_movie')
router.register(r'v1/get_movie_by_age', GetMovieByAgeViewSet, 'get_movie_by_age')
router.register(r'v1/get_movie_reaction', GetMovieReactionViewSet, 'get_movie_reaction')
router.register(r'v1/get_movie_by_onomatopoeia', GetMovieByOnomatopoeiaViewSet, 'get_movie_by_onomatopoeia')
router.register(r'v1/get_movie_by_id', GetMovieByIDViewSet, 'get_movie_by_id')
