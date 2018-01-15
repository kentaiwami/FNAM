from FiNote_API.utility import *
from rest_framework import viewsets
from FiNote_API.v1.movie_serializer import *
from rest_framework.response import Response
from django.db.models import F
from collections import Counter
import datetime
from FiNote_API.thread import *

# [0]: GetSearchMovieTitleResultsViewSet
# [1]: GetOriginalTitleViewSet
# test_flag = [False, False]


class GetMoviesViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        if not 'user_id' in request.GET:
            raise serializers.ValidationError('user_idが含まれていません')

        user_id = request.GET.get('user_id')

        try:
            user = AuthUser.objects.get(pk=user_id)
        except:
            raise serializers.ValidationError('該当データが見つかりませんでした')

        movie_user_list = Movie_User.objects.filter(user=user).order_by('-created_at')

        results = []

        for movie_user_obj in movie_user_list:
            hoge = Movie_User_Onomatopoeia.objects.filter(movie_user=movie_user_obj)
            onomatopoeia_name_list = [movie_user_onomatopoeia.onomatopoeia.name for movie_user_onomatopoeia in hoge]

            results.append({
                'title': movie_user_obj.movie.title,
                'id': movie_user_obj.movie.tmdb_id,
                'add': movie_user_obj.created_at,
                'poster': movie_user_obj.movie.poster,
                'dvd': movie_user_obj.dvd,
                'fav': movie_user_obj.fav,
                'onomatopoeia': onomatopoeia_name_list
            })

        return Response({'results': results})


class UpdateDVDFAVViewSet(viewsets.ViewSet):
    serializer_class = UpdateDVDFAVSerializer

    @staticmethod
    def create(request):

        data = request.data
        serializer = UpdateDVDFAVSerializer(data=data)

        if not (serializer.is_valid() and request.method == 'POST'):
            raise serializers.ValidationError(serializer.errors)

        try:
            user = AuthUser.objects.get(username=data['username'])
            movie = Movie.objects.get(tmdb_id=data['tmdb_id'])
            movie_user = Movie_User.objects.get(movie=movie, user=user)
        except:
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        if not user.check_password(data['password'].encode('utf-8')):
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        movie_user.dvd = data['dvd']
        movie_user.fav = data['fav']
        movie_user.save()

        return Response({'dvd': data['dvd'], 'fav': data['fav']})


class AddMovieViewSet(viewsets.ViewSet):
    serializer_class = AddMovieSerializer

    @staticmethod
    def create(request):

        data = request.data
        serializer = AddMovieSerializer(data=data)

        if not (serializer.is_valid() and request.method == 'POST'):
            raise serializers.ValidationError(serializer.errors)

        try:
            user = AuthUser.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        if not user.check_password(data['password'].encode('utf-8')):
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        # ジャンルの登録とオブジェクトの取得
        genre_obj_list = get_or_create_genre(data['genre'])

        # オノマトペの登録とオブジェクトの取得
        onomatopoeia_obj_list = []
        for onomatopoeia in data['onomatopoeia']:
            obj, created = Onomatopoeia.objects.get_or_create(
                name=onomatopoeia,
                defaults={'name': onomatopoeia}
            )

            onomatopoeia_obj_list.append(obj)

        # 映画オブジェクトの新規追加 or 取得
        movie_obj, created_movie = Movie.objects.get_or_create(
            tmdb_id=data['tmdb_id'],
            defaults={'title': data['title'],
                      'tmdb_id': data['tmdb_id'],
                      'overview': data['overview'],
                      'poster': data['poster']}
        )

        # 追加した映画にジャンルがなければ新規追加
        for genre_obj in genre_obj_list:
            if not movie_obj.genre.all().filter(name=genre_obj.name).exists():
                movie_obj.genre.add(genre_obj)

        # 追加した映画にオノマトペがあればカウント更新
        # なければ新規追加
        for onomatopoeia_obj in onomatopoeia_obj_list:
            if movie_obj.onomatopoeia.all().filter(name=onomatopoeia_obj.name).exists():
                Movie_Onomatopoeia.objects.filter(
                    movie=movie_obj, onomatopoeia=onomatopoeia_obj
                ).update(count=F('count') + 1)
            else:
                Movie_Onomatopoeia(movie=movie_obj, onomatopoeia=onomatopoeia_obj).save()

        movie_obj.save()

        # 追加した映画にユーザを新規追加
        movie_user, created_movie_user = Movie_User.objects.get_or_create(
            movie=movie_obj, user=user,
            defaults={'movie': movie_obj, 'user': user, 'dvd': data['dvd'], 'fav': data['fav']}
        )

        # movie user onomatopoeiaの保存
        if created_movie_user:
            for onomatopoeia_obj in onomatopoeia_obj_list:
                Movie_User_Onomatopoeia(movie_user=movie_user, onomatopoeia=onomatopoeia_obj).save()

        return Response({'msg': 'success'})


class UpdateOnomatopoeiaViewSet(viewsets.ViewSet):
    serializer_class = UpdateOnomatopoeiaSerializer

    @staticmethod
    def create(request):

        data = request.data
        serializer = UpdateOnomatopoeiaSerializer(data=data)

        if not (serializer.is_valid() and request.method == 'POST'):
            raise serializers.ValidationError(serializer.errors)

        try:
            user = AuthUser.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        if not user.check_password(data['password'].encode('utf-8')):
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        movie_obj = Movie.objects.get(tmdb_id=data['tmdb_id'])

        # movie user onomatopoeiaの該当するレコードを削除
        movie_user = Movie_User.objects.get(user=user, movie=movie_obj)
        Movie_User_Onomatopoeia.objects.filter(movie_user=movie_user).delete()

        for onomatopoeia_name in data['onomatopoeia']:
            # オノマトペがなければ新規作成
            onomatopoeia_obj, created = Onomatopoeia.objects.get_or_create(
                name=onomatopoeia_name,
                defaults={'name': onomatopoeia_name}
            )

            if not movie_obj.onomatopoeia.all().filter(name=onomatopoeia_obj.name).exists():
                Movie_Onomatopoeia(movie=movie_obj, onomatopoeia=onomatopoeia_obj).save()

            # オノマトペカウントオブジェクトの新規追加 or 取得
            onomatopoeia_count_obj, created_oc = Movie_Onomatopoeia.objects.get_or_create(
                onomatopoeia=onomatopoeia_obj,
                movie=movie_obj,
                defaults={'count': 1, 'onomatopoeia': onomatopoeia_obj, 'movie': movie_obj}
            )

            # オノマトペカウントオブジェクトの更新
            if not created_oc:
                onomatopoeia_count_obj.count += 1
                onomatopoeia_count_obj.save()

            # movie user onomatopoeiaの保存
            Movie_User_Onomatopoeia(movie_user=movie_user, onomatopoeia=onomatopoeia_obj).save()

        return Response({'msg': 'success'})


class DeleteMovieViewSet(viewsets.ViewSet):
    serializer_class = DeleteMovieSerializer

    @staticmethod
    def create(request):

        data = request.data
        serializer = DeleteMovieSerializer(data=data)

        if not (serializer.is_valid() and request.method == 'POST'):
            return serializers.ValidationError(serializer.errors)

        try:
            user = AuthUser.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        if not user.check_password(data['password'].encode('utf-8')):
            raise serializers.ValidationError('該当するデータが見つかりませんでした')

        movie_obj = Movie.objects.get(tmdb_id=data['tmdb_id'])
        Movie_User.objects.get(movie=movie_obj, user=user).delete()

        return Response({'msg': 'success'})


class GetRecentlyMovieViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        today = datetime.date.today() + datetime.timedelta(days=1)
        one_week_ago = today - datetime.timedelta(days=7)

        queryset = Movie_User_Onomatopoeia.objects.filter(created_at__range=(one_week_ago, today))

        # movie_userごとに集計
        movie_user_onomatopoeia_cnt = Counter()
        for movie_user_onomatopoeia in queryset:
            movie_user_onomatopoeia_cnt[movie_user_onomatopoeia.movie_user] += 1

        # 映画ごとに集計
        movie_cnt = Counter()
        for movie_user in movie_user_onomatopoeia_cnt:
            movie_cnt[movie_user.movie] += 1

        results = []
        for movie in movie_cnt.most_common(50):
            results.append({
                'title': movie[0].title,
                'overview': movie[0].overview,
                'poster': movie[0].poster
            })

        return Response({'results': results})


class GetMovieByAgeViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        today = datetime.date.today() + datetime.timedelta(days=1)
        one_week_ago = today - datetime.timedelta(days=7)

        queryset = Movie_User_Onomatopoeia.objects.filter(created_at__range=(one_week_ago, today))

        # movie_userごとに集計
        movie_user_onomatopoeia_cnt = Counter()
        for movie_user_onomatopoeia in queryset:
            movie_user_onomatopoeia_cnt[movie_user_onomatopoeia.movie_user] += 1

        # 映画ごとに、追加したユーザの年代別でカウント
        movie_user_count = MovieUserCount()
        for movie_user_obj in movie_user_onomatopoeia_cnt:
            movie_user_count.count(movie_user_obj.user, movie_user_obj.movie)

        res_dict = {
            '10': [],
            '20': [],
            '30': [],
            '40': [],
            '50': [],
        }

        # 10〜50代の登録数でソート
        for res_key in res_dict:
            sorted_dict = movie_user_count.sort(res_key)

            for movie, count_dict in zip(sorted_dict.keys(), sorted_dict.values()):
                # 対象の年代(res_key)で登録している数が0件の場合はスキップ
                if count_dict[res_key] == 0:
                    continue

                res_dict[res_key].append({
                    "count": count_dict[res_key],
                    "overview": movie.overview,
                    "poster": movie.poster,
                    "title": movie.title
                })

        return Response({'results': res_dict})


class GetMovieOnomatopoeiaViewSet(viewsets.ViewSet):
    serializer_class = GetMovieOnomatopoeiaSerializer

    @staticmethod
    def create(request):
        data = request.data
        serializer = GetMovieOnomatopoeiaSerializer(data=data)

        if not(serializer.is_valid() and request.method == 'POST'):
            raise serializers.ValidationError(serializer.errors)

        res = []

        thread_list = []
        for tmdb_id in data['tmdb_ids']:
            thread = GetMovieReactionThread(tmdb_id)
            thread_list.append(thread)
            thread.start()

        # 全てのスレッドが完了するまで待機(ブロック)
        for thread in thread_list:
            thread.join()

        for thread in thread_list:
            thread_result = thread.getResult()
            if thread_result:
                res.append(thread_result)

        return Response({'results': res})


# class GetMovieByOnomatopoeiaViewSet(viewsets.ViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = GetMovieByOnomatopoeiaSerializer
#
#     @staticmethod
#     def create(request):
#         """
#         When GetMovieByOnomatopoeia api access, run this method.
#         This method gets movies that include target onomatopoeia.
#         :param request: Target onomatopoeia.
#         :return: Hit movies information(title, overview and poster_path).
#         """
#
#         serializer = GetMovieByOnomatopoeiaSerializer(data=request.data)
#
#         if serializer.is_valid() and request.method == 'POST':
#             # リクエスト文字を含むオノマトペを取得
#             onomatopoeia_name = request.data['onomatopoeia_name']
#             onomatopoeia_list = Onomatopoeia.objects.filter(name__contains=onomatopoeia_name)
#
#             # 上記で取得したオノマトペを含む映画を取得
#             movie_list = []
#             for onomatopoeia in onomatopoeia_list:
#                 movies = Movie.objects.filter(onomatopoeia=onomatopoeia)
#                 movie_list += list(movies)
#
#             # 映画の情報をdictとして生成
#             res = []
#             for movie in movie_list:
#                 res.append({"title": movie.title,
#                             "overview": movie.overview,
#                             "poster_path": movie.poster_path})
#
#             return Response(res)
#         else:
#             raise ValidationError('必要なパラメータが含まれていません')
#
#
#
#
# class GetSearchMovieTitleResultsViewSet(viewsets.ViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = GetSearchMovieTitleResultsSerializer
#
#     @staticmethod
#     def create(request):
#         """
#         When GetSearchMovieTitleResults api access, run this method.
#         This method gets search results in yahoo movie website.
#         :param request: Search movie title and page number.
#         :return: Movie's title, movie's id and total results count.
#         """
#
#         serializer = GetSearchMovieTitleResultsSerializer(data=request.data)
#
#         if serializer.is_valid() and request.method == 'POST':
#             res = []
#
#             context = ssl._create_unverified_context()
#             url, param = get_url_param(test_flag[0], 'search', request.data)
#             html = urllib.request.urlopen(url + '?' + urllib.parse.urlencode(param), context=context)
#             soup = BeautifulSoup(html, "html.parser")
#
#             # 検索結果の合計件数を抽出
#             srchform_div = soup.find(id='srchform')
#             srchform_div_label = srchform_div.find(class_='label')
#
#             # 検索結果が0の場合はこの時点で結果を返す
#             if srchform_div_label is None:
#                 return Response({'total': 0, 'results': []})
#
#             small_list = srchform_div_label.find_all('small')
#             del small_list[0]
#
#             match = re.findall(r'[0-9]+', small_list[0].string)
#             total_resutls_count = int(match[0])
#
#             # 映画のタイトルとIDを抽出
#             lst = soup.find(id='lst')
#             li_tag_list = lst.find_all('li', class_='col')
#
#             title_id_list = []
#             for li_tag in li_tag_list:
#                 title = li_tag.find('h3', class_='text-xsmall text-overflow').attrs['title']
#                 id = li_tag.attrs['data-cinema-id']
#                 title_id_list.append({'title': title, 'id': id})
#
#             res.append({'total': total_resutls_count})
#             res.append({'results': title_id_list})
#
#             return Response({'total': total_resutls_count, 'results': title_id_list})
#
#         else:
#             raise ValidationError('正しいパラメータ値ではありません')
#
#
# class GetOriginalTitleViewSet(viewsets.ViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = GetOriginalTitleSerializer
#
#     @staticmethod
#     def create(request):
#         """
#         When GetOriginalTitle api access, run this method.
#         This method gets original movie title in yahoo movie website.
#         :param request: Search movie title and id number.
#         :return: Movie's original title.
#         """
#
#         serializer = GetOriginalTitleSerializer(data=request.data)
#
#         if serializer.is_valid() and request.method == 'POST':
#             original_title = ''
#
#             context = ssl._create_unverified_context()
#             url, param = get_url_param(test_flag[1], 'origin', request.data)
#             html = urllib.request.urlopen(url + '?' + urllib.parse.urlencode(param), context=context)
#             soup = BeautifulSoup(html, "html.parser")
#
#             mvinf = soup.find(id='mvinf')
#             tr_tag_list = mvinf.find_all('tr')
#
#             # 製作国が日本以外なら保存した原題を返す
#             for tr_tag in tr_tag_list:
#                 th_tag = tr_tag.find('th')
#
#                 if th_tag.string == '原題':
#                     original_title = tr_tag.find('td').string
#                     continue
#
#                 if th_tag.string == '製作国':
#                     if tr_tag.find('li').string != '日本':
#                         return Response(original_title)
#                     break
#
#             return Response('')
#         else:
#             raise ValidationError('正しいパラメータ値ではありません')
#
#
# class GetOnomatopoeiaCountByMovieIDViewSet(viewsets.ViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = GetOnomatopoeiaCountByMovieIDSerializer
#
#     @staticmethod
#     def create(request):
#         """
#         When GetOnomatopoeiaCountByMovieID api access, run this method.
#         This method gets onomatopoeia count in movie.
#         :param request: Target movie id and onomatopoeia names.
#         :return: Onomatopoeia name and count.
#         """
#
#         serializer = GetOnomatopoeiaCountByMovieIDSerializer(data=request.data)
#
#         if serializer.is_valid() and request.method == 'POST':
#             onomatopoeia_name_list = conversion_str_to_list(request.data['onomatopoeia_name_list'], 'str')
#             movie = Movie.objects.get(tmdb_id=request.data['tmdb_id'])
#
#             # 200よりリクエストされたオノマトペが少なければ最後までslice、それ以外なら20で割った分だけslice
#             if len(onomatopoeia_name_list) < 200:
#                 s = 0
#                 e = len(onomatopoeia_name_list)
#
#             else:
#                 s = 0
#                 e = int(len(onomatopoeia_name_list) / 20)  # MySQLの同時接続数が20のため
#
#             sliced = onomatopoeia_name_list[s:e]
#             thread_list = []
#
#             while len(sliced) != 0:
#                 thread = GetOnomatopoeiaCountByMovieIDThread(movie, sliced)
#                 thread_list.append(thread)
#                 thread.start()
#
#                 # スライス箇所の更新
#                 s = e
#                 e += e
#                 sliced = onomatopoeia_name_list[s:e]
#
#             # 全てのスレッドが完了するまで待機(ブロック)
#             for thread in thread_list:
#                 thread.join()
#
#             res = []
#             for thread in thread_list:
#                 if len(thread.getResult()) != 0:
#                     res.extend(thread.getResult())
#
#             return Response(res)
#
#         else:
#             raise ValidationError('正しいパラメータ値ではありません')
