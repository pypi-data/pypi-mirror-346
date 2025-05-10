#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
线程引擎模块

该模块提供了基于线程的行为树执行引擎。
支持多棵行为树在独立线程中并行执行，每棵树都有自己的执行状态和黑板数据。
"""

import threading
from typing import Any, Dict, List, Optional, Type, Callable, Tuple

from psbtree.core import NodeStatus, TreeNode
from psbtree.nodes.action_node import SimpleActionNode
from psbtree.engine.sequential_engine import SequentialEngine

class ThreadEngine:
    """线程B树引擎类
    
    该类实现了基于线程的B树操作，每个行为树在独立的线程中执行。
    支持动态注册行为节点、创建和管理多棵行为树、控制树执行、访问黑板数据等功能。
    
    Attributes:
        _trees: 存储所有行为树的字典，键为树ID，值为SequentialEngine实例
        _tree_threads: 存储所有树执行线程的字典，键为树ID，值为Thread实例
        _tree_stop_events: 存储所有树停止事件的字典，键为树ID，值为Event实例
    """
    
    def __init__(self) -> None:
        """初始化线程引擎
        
        创建空的树字典、线程字典和停止事件字典。
        """
        ...
    
    def register_action_behavior(self, action_id: str, tick_functor: Callable[[TreeNode], NodeStatus], 
                              ports_list: List[Dict[str, str]]) -> None:
        """注册行为节点
        
        注册一个行为节点，指定其ID、执行函数和端口列表。
        
        Args:
            action_id: 行为节点ID
            tick_functor: 节点执行函数
            ports_list: 端口定义列表
        """
        ...
    
    def register_action_class(self, action_class: Type[SimpleActionNode], action_id: Optional[str] = None) -> None:
        """注册行为节点类
        
        注册一个行为节点类，可以指定自定义ID。
        
        Args:
            action_class: 行为节点类
            action_id: 自定义行为节点ID，默认为None
        """
        ...
    
    def create_tree_from_text(self, xml_text: str, tree_id: Optional[str] = None) -> str:
        """从XML文本创建行为树
        
        解析XML文本并创建行为树。
        
        Args:
            xml_text: XML格式的行为树定义文本
            tree_id: 自定义树ID，默认为None
            
        Returns:
            str: 创建的树ID
        """
        ...
    
    def create_tree_from_file(self, file_path: str, tree_id: Optional[str] = None) -> str:
        """从XML文件创建行为树
        
        读取并解析XML文件，创建行为树。
        
        Args:
            file_path: XML文件路径
            tree_id: 自定义树ID，默认为None
            
        Returns:
            str: 创建的树ID
        """
        ...
    
    def get_tree_ids(self) -> List[str]:
        """获取所有树ID
        
        Returns:
            List[str]: 所有已创建的行为树ID列表
        """
        ...
    
    def tick_once(self, tree_id: str) -> NodeStatus:
        """执行一次行为树
        
        执行指定行为树的一个tick周期。
        
        Args:
            tree_id: 行为树ID
            
        Returns:
            NodeStatus: 执行结果状态
        """
        ...
    
    def tick_until_failure(self, tree_id: str) -> int:
        """执行行为树直到失败
        
        持续执行行为树，直到返回失败状态。
        
        Args:
            tree_id: 行为树ID
            
        Returns:
            int: 执行的tick次数
        """
        ...
    
    def tick_until_success(self, tree_id: str) -> int:
        """执行行为树直到成功
        
        持续执行行为树，直到返回成功状态。
        
        Args:
            tree_id: 行为树ID
            
        Returns:
            int: 执行的tick次数
        """
        ...
    
    def tick_n_times(self, tree_id: str, n: int) -> List[NodeStatus]:
        """执行行为树指定次数
        
        执行指定行为树n个tick周期。
        
        Args:
            tree_id: 行为树ID
            n: 执行次数
            
        Returns:
            List[NodeStatus]: 每次执行的结果状态列表
        """
        ...
    
    def get_tree_status(self, tree_id: str) -> Dict[str, Any]:
        """获取行为树状态
        
        获取指定行为树的当前状态信息。
        
        Args:
            tree_id: 行为树ID
            
        Returns:
            Dict[str, Any]: 树状态信息字典
        """
        ...
    
    def get_blackboard_data(self, tree_id: str, key: str) -> Any:
        """获取黑板数据
        
        从指定行为树的黑板中获取数据。
        
        Args:
            tree_id: 行为树ID
            key: 数据键名
            
        Returns:
            Any: 黑板数据值
        """
        ...
    
    def set_blackboard_data(self, tree_id: str, key: str, value: Any) -> None:
        """设置黑板数据
        
        向指定行为树的黑板中写入数据。
        
        Args:
            tree_id: 行为树ID
            key: 数据键名
            value: 数据值
        """
        ...
    
    def get_all_blackboard_data(self, tree_id: str) -> Dict[str, Any]:
        """获取所有黑板数据
        
        获取指定行为树黑板中的所有数据。
        
        Args:
            tree_id: 行为树ID
            
        Returns:
            Dict[str, Any]: 黑板数据字典
        """
        ...
    
    def reset_tree(self, tree_id: str) -> None:
        """重置行为树
        
        重置指定行为树的状态。
        
        Args:
            tree_id: 行为树ID
        """
        ...
    
    def stop_tree(self, tree_id: str) -> None:
        """停止行为树
        
        停止指定行为树的执行。
        
        Args:
            tree_id: 行为树ID
        """
        ...
    
    def stop_all_trees(self) -> None:
        """停止所有行为树
        
        停止所有正在执行的行为树。
        """
        ...
    
    def __del__(self) -> None:
        """析构函数
        
        停止所有行为树并清理资源。
        """
        ... 