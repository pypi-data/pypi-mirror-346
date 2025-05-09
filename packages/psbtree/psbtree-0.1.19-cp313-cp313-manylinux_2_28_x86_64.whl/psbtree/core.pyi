#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
行为树核心模块

该模块提供了行为树的核心类和功能，包括：
1. 行为树数据结构
2. 节点状态定义
3. 端口管理
4. 节点类型注册
5. 行为树执行控制
"""

import pybind11
from typing import Any, Callable, Dict, List, Tuple, Union

class BTreeData:
    """行为树数据类
    
    用于存储行为树中的通用数据。
    
    Attributes:
        data: 存储的数据值
    """
    def __init__(self) -> None: ...
    data: Any

class PortInfo:
    """端口信息类
    
    用于描述行为树节点的端口信息。
    
    Methods:
        type: 获取端口类型
        description: 获取端口描述
    """
    def type(self) -> str: ...
    def description(self) -> str: ...

def InputPort(name: str, description: str = "") -> Tuple[str, PortInfo]:
    """创建输入端口
    
    Args:
        name: 端口名称
        description: 端口描述，默认为空字符串
        
    Returns:
        Tuple[str, PortInfo]: 端口名称和端口信息的元组
    """
    ...

class NodeStatus:
    """节点状态类
    
    定义了行为树节点的可能状态。
    
    Attributes:
        IDLE: 空闲状态
        RUNNING: 运行状态
        SUCCESS: 成功状态
        FAILURE: 失败状态
        SKIPPED: 跳过状态
    """
    IDLE: NodeStatus
    RUNNING: NodeStatus
    SUCCESS: NodeStatus
    FAILURE: NodeStatus
    SKIPPED: NodeStatus

def registerNodeType(factory: BehaviorTreeFactory, name: str, cls: pybind11.object) -> None:
    """注册节点类型
    
    Args:
        factory: 行为树工厂实例
        name: 节点类型名称
        cls: 节点类
    """
    ...

class SyncActionNode:
    """同步动作节点基类
    
    所有同步动作节点的基类。
    
    Args:
        name: 节点名称
        config: 节点配置
        
    Methods:
        tick: 执行节点
        providedPorts: 获取节点提供的端口列表
    """
    def __init__(self, name: str, config: NodeConfig) -> None: ...
    def tick(self) -> NodeStatus: ...
    @staticmethod
    def providedPorts() -> List[Dict[str, str]]: ...

class SimpleActionNode(SyncActionNode):
    """简单动作节点类
    
    继承自SyncActionNode，用于实现简单的动作节点。
    
    Args:
        name: 节点名称
        config: 节点配置
    """
    def __init__(self, name: str, config: NodeConfig) -> None: ...
    def tick(self) -> NodeStatus: ...

class Tree:
    """行为树类
    
    表示一个完整的行为树。
    
    Methods:
        tickOnce: 执行一次行为树
        SetRootBlackboardData: 设置根节点黑板数据
        GetRootBlackboardData: 获取根节点黑板数据
    """
    def __init__(self) -> None: ...
    def tickOnce(self) -> NodeStatus: ...
    def SetRootBlackboardData(self, key: str, value: Any) -> None: ...
    def GetRootBlackboardData(self, key: str) -> Any: ...

class TreeNode:
    """树节点类
    
    表示行为树中的一个节点。
    
    Methods:
        getInput: 获取输入值
        setOutput: 设置输出值
        getInputObject: 获取输入对象
        getInputInt: 获取整数输入
        getInputString: 获取字符串输入
    """
    def getInput(self, key: str) -> Any: ...
    def setOutput(self, key: str, value: Any) -> None: ...
    def getInputObject(self, key: str) -> Any: ...
    def getInputInt(self, key: str) -> int: ...
    def getInputString(self, key: str) -> str: ...

class NodeConfig:
    """节点配置类
    
    用于配置行为树节点的参数。
    """
    def __init__(self) -> None: ...

class BehaviorTreeFactory:
    """行为树工厂类
    
    用于创建和管理行为树。
    
    Methods:
        createTreeFromText: 从文本创建行为树
        registerSimpleAction: 注册简单动作节点
    """
    def __init__(self) -> None: ...
    def createTreeFromText(self, text: str) -> Tree: ...
    def registerSimpleAction(
        self,
        ID: str,
        tick_functor: Callable[[TreeNode], NodeStatus],
        ports_list: List[Dict[str, str]]
    ) -> None: ...

__version__: str  # 模块版本号