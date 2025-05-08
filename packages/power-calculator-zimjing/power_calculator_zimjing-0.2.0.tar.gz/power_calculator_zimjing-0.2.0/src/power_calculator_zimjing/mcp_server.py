"""
MCP服务器实现
提供乘方计算相关的工具调用功能
"""

from typing import Dict, Any, Callable
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PowerCalculatorServer:
    """乘方计算服务器类"""
    
    def __init__(self):
        """初始化服务器"""
        self.tools: Dict[str, Callable] = {}
        self._register_default_tools()
        
    def _register_default_tools(self):
        """注册默认工具"""
        self.register_tool("calculate_power", self._calculate_power)
        self.register_tool("get_tool_info", self._get_tool_info)
        
    def register_tool(self, name: str, func: Callable) -> None:
        """
        注册工具函数
        
        Args:
            name: 工具名称
            func: 工具函数
        """
        self.tools[name] = func
        logger.info(f"注册工具: {name}")
        
    def call_tool(self, name: str, **kwargs) -> Any:
        """
        调用工具函数
        
        Args:
            name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            工具执行结果
        """
        if name not in self.tools:
            raise ValueError(f"工具 {name} 未注册")
        return self.tools[name](**kwargs)
    
    def _calculate_power(self, base: float, exponent: float) -> float:
        """
        计算乘方
        
        Args:
            base: 底数
            exponent: 指数
            
        Returns:
            计算结果
        """
        logger.info(f"计算乘方: {base}^{exponent}")
        return base ** exponent
    
    def _get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """
        获取工具信息
        
        Args:
            tool_name: 工具名称
            
        Returns:
            工具信息字典
        """
        if tool_name not in self.tools:
            raise ValueError(f"工具 {tool_name} 未注册")
        return {
            "name": tool_name,
            "doc": self.tools[tool_name].__doc__,
            "signature": str(self.tools[tool_name].__signature__)
        }

# 创建全局服务器实例
server = PowerCalculatorServer()

def register_tool(name: str) -> Callable:
    """
    工具注册装饰器
    
    Args:
        name: 工具名称
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        server.register_tool(name, func)
        return func
    return decorator 