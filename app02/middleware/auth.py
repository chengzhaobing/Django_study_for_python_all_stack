from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin





class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0. 排除那些不需要登录就能访问的页面
        # request.path_info----获取当前用户请求的url
                                # 需要排除的网址
        if request.path_info in ["/", "/login/", "/img/code/"]:
            return

        # 1. 读取当前访问的用户的Session信息，如果能读到，说明已经登录过，可以继续向后走
        info  = request.session.get('info')
        # print(info)
        # 2. 如果没有登陆过
        if not info:
            return redirect("/login/")

        return


# class M1(MiddlewareMixin):
#     """ 中间件1 """
#
#     def process_request(self, request):
#         print("M1.process_request")
#
#
#     def process_response(self, request, response):
#         print("M1.process_response")
#
#         return response



# class M2(MiddlewareMixin):
#     """ 中间件2 """
#
#     def process_request(self, request):
#         print("M2.process_request")
#
#
#     def process_response(self, request, response):
#         print("M2.process_response")
#
#         return response