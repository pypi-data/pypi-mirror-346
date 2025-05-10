#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict
from psbtree.nodes import SimpleActionNode, TreeNode, NodeStatus
from psbtree.plugins.yolo.yolo import YoloThreadedInfer

class CreateThreadedYolo(SimpleActionNode):
    """创建线程化YOLO推理节点
    
    该节点用于创建并启动一个线程化的YOLO推理器。
    
    Attributes:
        ports: 节点端口定义，包含配置输入和YOLO推理器输出
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

class ThreadedYoloProcessing(SimpleActionNode):
    """线程化YOLO处理节点
    
    该节点用于将输入图像送入YOLO推理器进行处理。
    
    Attributes:
        ports: 节点端口定义，包含YOLO推理器输入和图像输入
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

class ThreadedYoloResponseFrame(SimpleActionNode):
    """线程化YOLO响应帧节点
    
    该节点用于获取YOLO推理器的处理结果并生成可视化帧。
    
    Attributes:
        ports: 节点端口定义，包含YOLO推理器输入和输出帧输出
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