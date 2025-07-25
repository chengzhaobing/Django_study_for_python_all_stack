
"""

自定义分页组件
使用方法：

from app02.utils.pagination import Pagination #导入pagination.py

1. 在视图函数中的调用方法：
    def user_list(request):
        # 1. 根据自己的情况筛选数据
        queryset = models.User.objects.all()

        # 2. 实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
        "queryset": page_object.page_queryset,
        "page_string":page_object.html(),
        }
        return render(request, "user_list.html", context)

2. 在html模板文件中

    ｛% for obj in queryset %｝
        {{ obj.xx }}
        ...
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>

    还可以修改页面的默认一页显示的条数，在实例化中，传入page_size = 20条数就行
   page_object = Paginator(request, queryset，page_size = 20)
"""

class Pagination(object):

    def __init__(self, request, queryset, page_size = 10, page_param="page", static_page = 5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size:每页显示多少条数据
        :param page_gram:在URL中传递的获取分页的参数，eg: /user/list/?page=25
        :param static_page:显示当前页的 前后几页
        """

        import copy # 原本不允许直接修改获取到的对象，只有深拷贝一份去修改
        query_dict = copy.deepcopy(request.GET) # print(type(query_dict))打印类型查看原码的库
        query_dict._mutable = True              # 输出：<class 'django.http.request.QueryDict>
        self.query_dict = query_dict            # from django.http.request import  QueryDict 导入他的原码库 ，ctrl即可查看相关原码
        self.page_param = page_param
        # 搜索后（筛选后）再分页，保留分页条件--筛选后的分页，是在筛选的结果进行分页，下面的应用如下
        # 对于 自定义的跳转页 携带 筛选条件 实现不了--通过ajax、js之类的
        # self.query_dict.setlist(self.page_param, [1])
        # self.query_dict.urlencode()

        page = request.GET.get(page_param,"1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.static_page = static_page

    def html(self):
        # 计算出前5页后5页
        if self.total_page_count <= 2 * self.static_page + 1:
            # 数据库的数据比较少，没有达到11页那么就固定1-11页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库数据较多
            if self.page <= self.static_page:
                # 当前页<5
                # 规范左侧页码为负值----当前页小于5时，左侧页码不应该动态变化
                start_page = 1
                end_page = 2 * self.static_page + 1
            else:
                if (self.page + self.static_page) > self.total_page_count:
                    # 当前页 + 5 > 总页数
                    # 规范右侧页码没有数据但有页码
                    start_page = self.total_page_count - 2 * self.static_page
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.static_page
                    end_page = self.page + self.static_page

        from django.utils.safestring import mark_safe  # 导入编译包，安全包--安全编译

        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        # print(self.query_dict.urlencode())

        # 首页
        prev = '<li class="page-item"><a class="page-link" href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 上一页

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li class="page-item"><a class="page-link" href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li class="page-item"><a class="page-link" href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            # 突出显示当前页
            if i == self.page:  # active 当前页
                ele = '<li class="page-item active"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li class="page-item"><a class="page-link" href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li class="page-item"><a class="page-link" href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        prev = '<li class="page-item"><a class="page-link" href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 搜索页
        search_string = """
              <li class="page-item">
                  <form class="d-flex" method="get">
                      <input name="page" style="width: 80px;height: 38px;position: relative;float: left;display: inline-block" class="form-control me-2"
                                         type="search" placeholder="页码" aria-label="Search">
                      <button style="height: 38px;width: 70px;" class="btn btn-outline-success" type="submit">跳转</button>
                  </form>
              </li>
          """
        page_str_list.append(search_string)
        # 产生的问题是没有编译----编译使用导入的安全包，进行编译
        page_string = mark_safe("".join(page_str_list))
        return page_string

