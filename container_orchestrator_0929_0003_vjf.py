# 代码生成时间: 2025-09-29 00:03:14
from pyramid.config import Configurator
from pyramid.response import Response
import docker

# 定义一个错误处理函数
def handle_error(context, exc_info):
    return Response(
        f"An error occurred: {exc_info[1]}",
        status=500,
        content_type='text/plain',
        charset='utf-8'
    )

# 定义一个视图函数，用于启动容器
def start_container(request):
    """Starts a container using Docker."""
    try:
        client = docker.from_env()
        container_name = request.params.get('container_name')
        image_name = request.params.get('image_name')
        # 启动容器
        client.containers.run(image=image_name, name=container_name)
        return Response(f"Container {container_name} started successfully.")
    except docker.errors.APIError as e:
        return Response(f"Failed to start container: {e}", status=500)
    except Exception as e:
        return Response(f"An unexpected error occurred: {e}", status=500)

# 定义一个视图函数，用于停止容器
def stop_container(request):
    """Stops a container using Docker."""
    try:
        client = docker.from_env()
        container_name = request.params.get('container_name')
        # 停止容器
        container = client.containers.get(container_name)
        container.stop()
        return Response(f"Container {container_name} stopped successfully.")
    except docker.errors.APIError as e:
        return Response(f"Failed to stop container: {e}", status=500)
    except Exception as e:
        return Response(f"An unexpected error occurred: {e}", status=500)

# 设置路由和视图
def main(global_config, **settings):
    """Main function to set up the Pyramid configurator."""
    with Configurator(settings=settings) as config:
        config.include('pyramid_handlers')
        config.add_route('start_container', '/start_container')
        config.add_view(start_container, route_name='start_container')
        config.add_route('stop_container', '/stop_container')
        config.add_view(stop_container, route_name='stop_container')
        # 设置错误处理
        config.scan()
        config.set_errorview(handle_error)

if __name__ == '__main__':
    # 运行应用程序
    main({})