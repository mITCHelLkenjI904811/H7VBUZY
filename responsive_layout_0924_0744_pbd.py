# 代码生成时间: 2025-09-24 07:44:16
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.events import NewRequest

# 定义一个视图函数，用于返回响应式布局的HTML页面
@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    # 从请求中获取视图名和响应式布局相关的参数
    view_name = request.matchdict.get('view_name', 'home')
    # 将视图名作为上下文传递给模板
    return {'view_name': view_name}

# 设置响应式布局的CSS样式
def includeme(config):
    # 设置视图配置
    config.add_route('home', '/')
    config.scan()

    # 添加CSS样式文件
    config.add_static_view(name='static', path='responsive_layout:static')
    config.add_directive('add_stylesheet', add_stylesheet)

    # 定义添加CSS样式的函数
    def add_stylesheet(config):
        # 添加响应式布局的CSS样式文件
        request = config.request
        response = request.response
        response.content_type = 'text/html'
        stylesheet = '<link rel="stylesheet" type="text/css" href="/static/responsive_layout.css" />'
        response.body = stylesheet + response.body

# 设置配置文件
config = Configurator()
config.include(includeme)

# 启动应用
if __name__ == '__main__':
    config.main(global_=True)