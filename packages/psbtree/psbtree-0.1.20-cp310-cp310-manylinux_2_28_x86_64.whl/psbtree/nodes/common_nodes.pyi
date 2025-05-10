#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通用节点模块

该模块提供了一系列通用的行为树节点，可以在不同的行为树中重复使用。
包括休眠、日志、黑板操作、条件判断、计数器和定时器等常用功能。
"""

import time
from typing import Any, Dict, List, Optional, Callable
from loguru import logger

from psbtree.core import NodeStatus, TreeNode
from psbtree.nodes.action_node import SimpleActionNode

class SleepNode(SimpleActionNode):
    """休眠节点
    
    该节点会在执行时休眠指定的时间，然后返回成功状态。
    可用于在行为树中引入延时。
    
    Attributes:
        ports: 节点端口列表，包含休眠时间输入
    """
    
    ports: List[Dict[str, str]]
    
    @staticmethod
    def tick(node: TreeNode) -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...


class LogNode(SimpleActionNode):
    """日志节点
    
    该节点会在执行时记录一条日志消息，然后返回成功状态。
    支持不同级别的日志记录。
    
    Attributes:
        ports: 节点端口列表，包含日志消息输入
    """
    
    ports: List[Dict[str, str]]
    
    @staticmethod
    def tick(node: TreeNode) -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...


class SetBlackboardNode(SimpleActionNode):
    """设置黑板数据节点
    
    该节点会在执行时设置行为树黑板中的数据，然后返回成功状态。
    可用于在行为树中传递数据。
    
    Attributes:
        ports: 节点端口列表，包含键值对输入
    """
    
    ports: List[Dict[str, str]]
    
    @staticmethod
    def tick(node: TreeNode) -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...


class GetBlackboardNode(SimpleActionNode):
    """获取黑板数据节点
    
    该节点会在执行时从行为树黑板中获取数据，然后返回成功状态。
    可用于在行为树中读取数据。
    
    Attributes:
        ports: 节点端口列表，包含键输入和值输出
    """
    
    ports: List[Dict[str, str]]
    
    @staticmethod
    def tick(node: TreeNode) -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...


class ConditionNode(SimpleActionNode):
    """条件节点
    
    该节点会根据条件返回成功或失败状态。
    可用于在行为树中实现条件判断。
    
    Attributes:
        ports: 节点端口列表，包含条件输入
    """
    
    ports: List[Dict[str, str]]
    
    @staticmethod
    def tick(node: TreeNode) -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...


class CounterNode(SimpleActionNode):
    """计数器节点
    
    该节点会维护一个计数器，每次执行时计数器加1，达到指定值后重置并返回成功状态。
    可用于在行为树中实现循环计数。
    
    Attributes:
        ports: 节点端口列表，包含目标计数值输入
    """
    
    def __init__(self) -> None:
        """初始化计数器节点"""
        ...
    
    def tick(self, node: TreeNode) -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...


class TimerNode(SimpleActionNode):
    """定时器节点
    
    该节点会在指定的时间后返回成功状态。
    可用于在行为树中实现定时操作。
    
    Attributes:
        ports: 节点端口列表，包含时间间隔输入
    """
    
    def __init__(self) -> None:
        """初始化定时器节点"""
        ...
    
    def tick(self, node: TreeNode) -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ... 