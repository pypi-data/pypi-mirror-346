#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
条件节点模块

该模块提供了行为树常用的条件节点实现。
包括值比较、布尔值判断和自定义条件等多种条件判断节点。
"""

from typing import Dict, List, Optional, Any, Callable
from psbtree.core import NodeStatus, TreeNode

from psbtree.nodes.action_node import ConditionNode


class IsValueNode(ConditionNode):
    """值判断节点类
    
    该类实现了判断输入值是否等于指定值的条件节点。
    当输入值等于指定值时返回成功状态，否则返回失败状态。
    
    Attributes:
        name: 节点名称
        value: 比较值
        config: 节点配置
    """
    
    def __init__(self, name: str, value: Any, config: Optional[Dict] = None) -> None:
        """初始化值判断节点
        
        Args:
            name: 节点名称
            value: 比较值
            config: 节点配置，默认为None
        """
        ...
    
    def tick(self) -> NodeStatus:
        """执行节点逻辑
        
        Returns:
            NodeStatus: 节点执行状态
        """
        ...
    
    @staticmethod
    def providedPorts() -> List[Dict[str, str]]:
        """获取节点提供的端口列表
        
        Returns:
            List[Dict[str, str]]: 端口定义列表
        """
        ...


class IsGreaterThanNode(ConditionNode):
    """大于判断节点类
    
    该类实现了判断输入值是否大于指定阈值的条件节点。
    当输入值大于阈值时返回成功状态，否则返回失败状态。
    
    Attributes:
        name: 节点名称
        threshold: 阈值
        config: 节点配置
    """
    
    def __init__(self, name: str, threshold: Any, config: Optional[Dict] = None) -> None:
        """初始化大于判断节点
        
        Args:
            name: 节点名称
            threshold: 阈值
            config: 节点配置，默认为None
        """
        ...
    
    def tick(self) -> NodeStatus:
        """执行节点逻辑
        
        Returns:
            NodeStatus: 节点执行状态
        """
        ...
    
    @staticmethod
    def providedPorts() -> List[Dict[str, str]]:
        """获取节点提供的端口列表
        
        Returns:
            List[Dict[str, str]]: 端口定义列表
        """
        ...


class IsLessThanNode(ConditionNode):
    """小于判断节点类
    
    该类实现了判断输入值是否小于指定阈值的条件节点。
    当输入值小于阈值时返回成功状态，否则返回失败状态。
    
    Attributes:
        name: 节点名称
        threshold: 阈值
        config: 节点配置
    """
    
    def __init__(self, name: str, threshold: Any, config: Optional[Dict] = None) -> None:
        """初始化小于判断节点
        
        Args:
            name: 节点名称
            threshold: 阈值
            config: 节点配置，默认为None
        """
        ...
    
    def tick(self) -> NodeStatus:
        """执行节点逻辑
        
        Returns:
            NodeStatus: 节点执行状态
        """
        ...
    
    @staticmethod
    def providedPorts() -> List[Dict[str, str]]:
        """获取节点提供的端口列表
        
        Returns:
            List[Dict[str, str]]: 端口定义列表
        """
        ...


class IsTrueNode(ConditionNode):
    """真值判断节点类
    
    该类实现了判断输入值是否为True的条件节点。
    当输入值为True时返回成功状态，否则返回失败状态。
    
    Attributes:
        name: 节点名称
        config: 节点配置
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None) -> None:
        """初始化真值判断节点
        
        Args:
            name: 节点名称
            config: 节点配置，默认为None
        """
        ...
    
    def tick(self) -> NodeStatus:
        """执行节点逻辑
        
        Returns:
            NodeStatus: 节点执行状态
        """
        ...
    
    @staticmethod
    def providedPorts() -> List[Dict[str, str]]:
        """获取节点提供的端口列表
        
        Returns:
            List[Dict[str, str]]: 端口定义列表
        """
        ...


class IsFalseNode(ConditionNode):
    """假值判断节点类
    
    该类实现了判断输入值是否为False的条件节点。
    当输入值为False时返回成功状态，否则返回失败状态。
    
    Attributes:
        name: 节点名称
        config: 节点配置
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None) -> None:
        """初始化假值判断节点
        
        Args:
            name: 节点名称
            config: 节点配置，默认为None
        """
        ...
    
    def tick(self) -> NodeStatus:
        """执行节点逻辑
        
        Returns:
            NodeStatus: 节点执行状态
        """
        ...
    
    @staticmethod
    def providedPorts() -> List[Dict[str, str]]:
        """获取节点提供的端口列表
        
        Returns:
            List[Dict[str, str]]: 端口定义列表
        """
        ...


class CustomConditionNode(ConditionNode):
    """自定义条件节点类
    
    该类实现了使用自定义函数作为条件的条件节点。
    当自定义函数返回True时返回成功状态，否则返回失败状态。
    
    Attributes:
        name: 节点名称
        condition_func: 条件判断函数
        config: 节点配置
    """
    
    def __init__(self, name: str, condition_func: Callable[[Any], bool], config: Optional[Dict] = None) -> None:
        """初始化自定义条件节点
        
        Args:
            name: 节点名称
            condition_func: 条件判断函数，接收一个参数并返回布尔值
            config: 节点配置，默认为None
        """
        ...
    
    def tick(self) -> NodeStatus:
        """执行节点逻辑
        
        Returns:
            NodeStatus: 节点执行状态
        """
        ...
    
    @staticmethod
    def providedPorts() -> List[Dict[str, str]]:
        """获取节点提供的端口列表
        
        Returns:
            List[Dict[str, str]]: 端口定义列表
        """
        ... 