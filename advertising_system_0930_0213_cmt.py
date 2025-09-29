# 代码生成时间: 2025-09-30 02:13:29
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError

# 定义广告模型
class Ad:
    def __init__(self, id, name, budget, impressions):
        self.id = id
        self.name = name
        self.budget = budget
        self.impressions = impressions

    def __str__(self):
        return f"Ad(id={self.id}, name='{self.name}', budget={self.budget}, impressions={self.impressions})"

# 广告存储（这里使用内存中的字典作为存储）
ads_storage = {}

# 添加广告的视图函数
@view_config(route_name='add_ad', renderer='json')
def add_ad(request):
    # 从请求中获取广告数据
    try:
        data = request.json_body
        ad_id = data['id']
        name = data['name']
        budget = data['budget']
        impressions = data['impressions']
    except (KeyError, TypeError, ValueError):
        raise HTTPBadRequest('Invalid data provided')

    # 创建广告对象
    new_ad = Ad(ad_id, name, budget, impressions)
    # 存储广告对象
    ads_storage[ad_id] = new_ad
    return {'status': 'success', 'ad': str(new_ad)}

# 获取所有广告的视图函数
@view_config(route_name='get_ads', renderer='json')
def get_ads(request):
    return {'ads': [str(ad) for ad in ads_storage.values()]}

# 删除广告的视图函数
@view_config(route_name='delete_ad', renderer='json')
def delete_ad(request):
    try:
        ad_id = int(request.matchdict['id'])
        if ad_id in ads_storage:
            del ads_storage[ad_id]
            return {'status': 'success', 'message': f'Ad {ad_id} deleted'}
        else:
            raise KeyError
    except (KeyError, ValueError):
        raise HTTPInternalServerError('Ad not found')

# 配置Pyramid应用
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    
    # 添加路由和视图函数
    config.add_route('add_ad', '/add_ad')
    config.add_view(add_ad, route_name='add_ad')
    config.add_route('get_ads', '/get_ads')
    config.add_view(get_ads, route_name='get_ads')
    config.add_route('delete_ad', '/delete_ad/{id}')
    config.add_view(delete_ad, route_name='delete_ad')
    
    return config.make_wsgi_app()

# 运行应用（仅供测试使用）
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()