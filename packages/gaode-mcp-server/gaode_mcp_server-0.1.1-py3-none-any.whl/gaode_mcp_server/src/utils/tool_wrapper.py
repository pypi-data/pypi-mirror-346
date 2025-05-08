import time
from ..amap import AMapAPIError

def tool_wrapper(action_name):
    def decorator(func):
        def wrapper(*args, request_context=None, **kwargs):
            start = time.time()
            try:
                if request_context:
                    request_context.session.send_log_message(
                        level="info",
                        data=f"开始{action_name}: args={args}, kwargs={kwargs}"
                    )
                result = func(*args, request_context=request_context, **kwargs)
                if request_context:
                    request_context.session.send_log_message(
                        level="info",
                        data=f"{action_name}成功: {result}"
                    )
                return result
            except AMapAPIError as e:
                if request_context:
                    request_context.session.send_log_message(
                        level="error",
                        data=f"高德API错误: {e}"
                    )
                return {"error": str(e)}
            except Exception as e:
                if request_context:
                    request_context.session.send_log_message(
                        level="error",
                        data=f"系统异常: {e}"
                    )
                return {"error": f"系统异常: {e}"}
            finally:
                if request_context:
                    duration = time.time() - start
                    request_context.session.send_log_message(
                        level="info",
                        data=f"{action_name}耗时: {duration:.3f}秒"
                    )
        return wrapper
    return decorator
