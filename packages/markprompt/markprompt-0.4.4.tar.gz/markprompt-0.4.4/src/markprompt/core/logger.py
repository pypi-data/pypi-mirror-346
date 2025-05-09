"""
日志格式化工具。
"""
import logging
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

# 创建全局控制台实例
console = Console()


def format_tool_calls(tool_calls: List[Any]) -> str:
    """格式化工具调用信息"""
    if not tool_calls:
        return ""

    result = []
    for tool_call in tool_calls:
        if hasattr(tool_call, "function"):
            function_info = tool_call.function
            result.append(f"- {function_info.name}({function_info.arguments})")
        elif isinstance(tool_call, dict) and "function" in tool_call:
            function_info = tool_call["function"]
            name = function_info.get("name", "unknown")
            arguments = function_info.get("arguments", "{}")
            result.append(f"- {name}({arguments})")

    return "\n".join(result)


class DynamicLogger:
    def __init__(self, title: str = "ASSISTANT"):
        self.console = Console()
        self.live = None
        self.title = title
        self.panel_content = Text()

    def __enter__(self):
        self.live = Live(self._render_panel(), console=self.console, refresh_per_second=4)
        self.live.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.live.__exit__(exc_type, exc_val, exc_tb)

    def _render_panel(self):
        return Panel(
            self.panel_content,
            title=self.title,
            title_align="left",
            border_style="green",
            padding=(1, 2)
        )

    def log(self, message: str):
        self.panel_content.append(f"{message}")
        self.live.update(self._render_panel())

    def stop_loading(self):
        pass


class MessageLogger:
    """
    专门用于处理和格式化消息的日志记录器。
    支持各种消息类型的格式化和显示。
    """

    ROLE_STYLES = {
        'system': 'magenta',
        'user': 'blue',
        'assistant': 'green',
        'tools': 'yellow',
        'tool': 'yellow',
        'unknown': 'yellow'
    }

    def __init__(self, logger_name: Optional[str] = None):
        """初始化消息日志记录器"""
        self.logger = setup_logger(logger_name or __name__)
        self.console = Console()
        self.is_verbose = True  # 默认为开启状态，会根据调用方法中的verbose参数覆盖

    def _create_panel(self, title: str, content: str, style: str = "blue") -> Panel:
        """创建一个格式化的面板"""
        return Panel(
            content,
            title=title,
            title_align="left",
            border_style=style,
            padding=(1, 2)
        )

    def _format_content(self, content: Any) -> str:
        """格式化消息内容，支持字符串或内容对象列表"""
        # 如果是字符串，直接返回
        if isinstance(content, str):
            return content
            
        # 如果是列表，处理不同类型的内容对象
        if isinstance(content, list):
            formatted_contents = []
            
            for item in content:
                if not isinstance(item, dict):
                    formatted_contents.append(str(item))
                    continue
                    
                item_type = item.get("type")
                
                if item_type == "text":
                    formatted_contents.append(item.get("text", ""))
                    
                elif item_type == "image_url":
                    image_url_obj = item.get("image_url", {})
                    url = image_url_obj.get("url", "")
                    
                    # 如果是http链接，显示完整URL；如果是base64数据，只显示前30个字符
                    if url.startswith(("http://", "https://")):
                        formatted_contents.append(f"[图片链接] {url}")
                    else:  # 假设是base64
                        truncated_url = url[:30] + "..." if len(url) > 30 else url
                        formatted_contents.append(f"[图片数据] {truncated_url}")
                else:
                    # 处理其他未知类型
                    formatted_contents.append(str(item))
            
            # 每个元素之间添加2个换行符
            return "\n\n".join(formatted_contents)
            
        # 其他情况，转换为字符串
        return str(content)

    def log_message(self, message: Dict[str, Any], verbose: bool = True):
        """记录单个消息
        
        Args:
            message: 要记录的消息
            verbose: 是否输出消息。如果为False，则不会输出任何内容
        """
        if not verbose:
            return
            
        try:
            # 获取消息角色和内容
            role = message.get("role", "unknown")
            content = message.get("content", "")
            
            # 格式化内容
            formatted_content = self._format_content(content)

            # 确定面板标题和样式
            title = role.upper()
            style = self.ROLE_STYLES.get(role, "white")

            # 创建并打印面板
            panel = self._create_panel(title, formatted_content, style)
            self.console.print(panel)
        except Exception as e:
            self.logger.error(f"Error logging message: {str(e)}")

    def log_messages(self, messages: List[Dict[str, Any]], verbose: bool = True):
        """记录多个消息
        
        Args:
            messages: 要记录的消息列表
            verbose: 是否输出消息。如果为False，则不会输出任何内容
        """
        if not verbose:
            return
            
        for message in messages:
            self.log_message(message, verbose=verbose)


def setup_logger(name: str = None) -> logging.Logger:
    """设置日志记录器。"""
    logger = logging.getLogger(name)

    # 如果已经有处理器，不重复添加
    if logger.handlers:
        return logger

    # 使用 RichHandler 替换标准的 StreamHandler
    handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=False,
        show_path=False,
        enable_link_path=False
    )

    # 设置格式为只显示消息内容
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


# 创建全局消息日志记录器实例
message_logger = MessageLogger("message_logger")
