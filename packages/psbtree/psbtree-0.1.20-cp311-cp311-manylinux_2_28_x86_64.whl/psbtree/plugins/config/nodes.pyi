#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from psbtree.nodes import SimpleActionNode, TreeNode, NodeStatus

class LoadConfigFile(SimpleActionNode):
    """加载配置文件节点
    
    该节点用于从YAML文件中加载配置信息。
    
    Attributes:
        ports: 节点端口定义，包含文件路径输入和配置输出
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

class LoadConfigString(SimpleActionNode):
    """加载配置字符串节点
    
    该节点用于从YAML格式的字符串中加载配置信息。
    
    Attributes:
        ports: 节点端口定义，包含配置字符串输入和配置输出
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