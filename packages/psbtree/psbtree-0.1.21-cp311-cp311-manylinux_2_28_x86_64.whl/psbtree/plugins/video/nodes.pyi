#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from psbtree.nodes import SimpleActionNode, TreeNode, NodeStatus
from psbtree.plugins.video.capture import ParallVideoCapture

class CreateThreadedVideoCapture(SimpleActionNode):
    """创建线程化视频捕获节点
    
    该节点用于创建并启动一个线程化的视频捕获器，支持视频的异步读取。
    
    Attributes:
        ports: 节点端口定义，包含配置输入和视频捕获器输出
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

class ReadThreadedFrame(SimpleActionNode):
    """读取线程化视频帧节点
    
    该节点用于从线程化视频捕获器中读取当前帧。
    
    Attributes:
        ports: 节点端口定义，包含视频捕获器输入和帧输出
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

class CreateVideoCapture(SimpleActionNode):
    """创建视频捕获节点
    
    该节点用于创建并启动一个基本的视频捕获器。
    
    Attributes:
        ports: 节点端口定义，包含视频路径输入和视频捕获器输出
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

class ReadFrame(SimpleActionNode):
    """读取视频帧节点
    
    该节点用于从视频捕获器中读取当前帧。
    
    Attributes:
        ports: 节点端口定义，包含视频捕获器输入和帧输出
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