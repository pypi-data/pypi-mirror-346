#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
行为树节点模块

该模块提供了行为树节点的基类和实现。
包含了动作节点、条件节点、装饰器节点和控制节点的基本定义。
"""

from typing import Dict, List, Optional, Any, Type, Callable, Protocol, runtime_checkable
from psbtree.core import BehaviorTreeFactory, SyncActionNode, NodeStatus, \
    registerNodeType, NodeConfig, TreeNode, InputPort, BTreeData


@runtime_checkable
class ActionNodeProtocol(Protocol):
    """动作节点协议
    
    定义了所有行为树节点必须实现的接口。
    使用Protocol和runtime_checkable确保运行时类型检查。
    
    Attributes:
        ports: 节点端口列表，定义节点的输入输出接口
    """
    
    ports: List[Dict[str, str]]
    
    @staticmethod
    def tick(node: 'TreeNode') -> 'NodeStatus':
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...


class SimpleActionNode:
    """简单动作节点基类
    
    该类是所有行为树节点的基类，提供了基本的节点功能。
    所有行为树节点类型（动作节点、条件节点、装饰器节点、控制节点）都继承自此类。
    
    Attributes:
        ports: 节点端口列表，用于定义节点的输入输出接口
    """
    ports: List[Dict[str, str]]
    
    @staticmethod
    def tick(node: 'TreeNode') -> 'NodeStatus':
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
        Returns:
            NodeStatus: 节点执行状态
        """
        ...
    
    @classmethod
    def providedPorts(cls) -> List[Dict[str, str]]:
        """获取节点提供的端口列表
        
        Returns:
            List[Dict[str, str]]: 端口定义列表
        """
        ...


class ActionNode(SimpleActionNode):
    """动作节点类
    
    该类实现了基本的动作节点功能。
    动作节点是行为树中的叶子节点，执行具体的动作。
    
    Attributes:
        name: 节点名称
        config: 节点配置
    """
    
    def __init__(self, name: str, config: Optional[NodeConfig] = None) -> None:
        """初始化动作节点
        
        Args:
            name: 节点名称
            config: 节点配置，默认为None
        """
        ...
    
    @staticmethod
    def tick(node: 'TreeNode') -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
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


class ConditionNode(SimpleActionNode):
    """条件节点类
    
    该类实现了基本的条件节点功能。
    条件节点用于检查条件是否满足，返回成功或失败状态。
    
    Attributes:
        name: 节点名称
        config: 节点配置
    """
    
    def __init__(self, name: str, config: Optional[NodeConfig] = None) -> None:
        """初始化条件节点
        
        Args:
            name: 节点名称
            config: 节点配置，默认为None
        """
        ...
    
    @staticmethod
    def tick(node: 'TreeNode') -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
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


class DecoratorNode(SimpleActionNode):
    """装饰器节点类
    
    该类实现了基本的装饰器节点功能。
    装饰器节点用于修改子节点的行为。
    
    Attributes:
        name: 节点名称
        config: 节点配置
    """
    
    def __init__(self, name: str, config: Optional[NodeConfig] = None) -> None:
        """初始化装饰器节点
        
        Args:
            name: 节点名称
            config: 节点配置，默认为None
        """
        ...
    
    @staticmethod
    def tick(node: 'TreeNode') -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
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


class ControlNode(SimpleActionNode):
    """控制节点类
    
    该类实现了基本的控制节点功能。
    控制节点用于控制子节点的执行顺序和方式。
    
    Attributes:
        name: 节点名称
        config: 节点配置
    """
    
    def __init__(self, name: str, config: Optional[NodeConfig] = None) -> None:
        """初始化控制节点
        
        Args:
            name: 节点名称
            config: 节点配置，默认为None
        """
        ...
    
    @staticmethod
    def tick(node: 'TreeNode') -> NodeStatus:
        """执行节点逻辑
        
        Args:
            node: 行为树节点实例
            
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


def register_node(factory: BehaviorTreeFactory, node_class: Type[SimpleActionNode], node_name: str) -> None:
    """注册节点类型
    
    将节点类型注册到行为树工厂中。
    
    Args:
        factory: 行为树工厂实例
        node_class: 节点类
        node_name: 节点名称
    """
    ... 