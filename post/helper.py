from django.core.cache import cache

from common import rds
from post.models import Post


def page_cache(timeout):
    def wrapper1(views_fun):
        def wrapper2(request):
            key = "PageCache-%s-%s" % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            if response is None:
                response = views_fun(request)
                cache.set(key, response, timeout)
            return response
        return wrapper2
    return wrapper1


def page_count(views_page):
    def wrapper(request):
        post_id = request.GET.get("post_id")
        print(post_id)
        rds.zincrby("ReadRank1", post_id)#阅读计数
        # print(rds.zrevrange(b'ReadRank', 0, -1, withscores=True))
        # print(rds.zcount("Read_Rank"))
        return views_page(request)
    return wrapper


def get_top_n(num):
    '''取出Top N 的帖子及阅读计数'''
    ori_data = rds.zrevrange(b'ReadRank1', 0, num-1, withscores=True)
    print(ori_data)

    cleaned_rank = [[int(post_id), int(count)] for post_id, count in ori_data]
    #
    # # 思路一
    # for item in cleaned_rank:
    #     item[0] = Post.objects.get(id=item[0])
    # rank_data = cleaned_rank
    #
    # # 思路二
    # post_id_list = [post_id for post_id, _ in cleaned_rank]
    # posts = Post.objects.filter(id__in=post_id_list) #批量去除posts
    # posts = sorted(posts, key=lambda post:post_id_list.index(post.id))
    #
    # rank_data = []
    # for post, (_, count) in zip(posts, cleaned_rank):
    #     rank_data.append([post, count])
    #
    # 思路三
    post_id_list = [post_id for post_id, _ in cleaned_rank]
    post_dict = Post.objects.in_bulk(post_id_list)
    for item in cleaned_rank:
        post_id = item[0]
        item[0] = post_dict[post_id]
    rank_data = cleaned_rank



    return rank_data