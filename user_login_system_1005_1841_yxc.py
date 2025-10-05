# 代码生成时间: 2025-10-05 18:41:49
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.security import Allow, Authenticated, remember, forget
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.events import NewRequest

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# 设置数据库连接
engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

# Pyramid安全装饰器
def check_csrf(request):
    return 'csrf_token' in request.params

@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    session = Session()
    username = request.params.get('username')
    password = request.params.get('password')
    user = session.query(User).filter_by(username=username).first()
    
    if user and user.password == password:
        headers = remember(request, username)
        return HTTPFound(location=request.route_url('home'))
    else:
        request.session.flash('Invalid username or password')
        return {'error': 'Invalid username or password'}

@view_config(route_name='home', require_csrf=True)
@view_config(route_name='logout', require_csrf=True)
def home(request):
    if not request.authenticated_userid:
        return HTTPFound(location=request.route_url('login'))
    return {'username': request.authenticated_userid}

# 主函数
def main(global_config, **settings):
    """创建 Pyramid WSGI 应用程序。"""
    config = Configurator(settings=settings)
    config.include('.pyramid routemap')
    config.include('.pyramid assetmap')
    config.include('.pyramid renderers')
    config.add_route('login', '/login')
    config.add_route('home', '/')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
