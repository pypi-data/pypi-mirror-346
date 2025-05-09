#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import queue
from typing import Any, Optional
import numpy as np

class VisionInfer:
    """视觉推理基类
    
    该类提供了视觉推理的基础框架，支持线程化的图像处理。
    使用队列进行图像缓冲，避免内存堆积。
    
    Attributes:
        _input_queue (queue.Queue): 输入图像队列
        _result (Any): 最新的处理结果
        _result_lock (threading.Lock): 结果锁
        _stop_event (threading.Event): 停止事件
        _thread (threading.Thread): 处理线程
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """初始化视觉推理器
        
        Args:
            *args: 可变位置参数
            **kwargs: 可变关键字参数
        """
        ...
        
    def _init_algorithm(self, *args: Any, **kwargs: Any) -> None:
        """初始化具体算法
        
        子类需要重写此方法以实现具体的算法初始化。
        
        Args:
            *args: 可变位置参数
            **kwargs: 可变关键字参数
        """
        ...
        
    def process(self, image: np.ndarray) -> None:
        """处理输入图像
        
        非阻塞方式处理图像，最新帧优先。
        
        Args:
            image: 输入图像
        """
        ...
        
    def get_result(self) -> Optional[Any]:
        """获取最新处理结果
        
        Returns:
            Optional[Any]: 处理结果，如果没有结果则返回None
        """
        ...
        
    def _process_thread(self) -> None:
        """处理线程主循环
        
        持续从队列中获取图像并进行处理。
        """
        ...
        
    def _process(self, image: np.ndarray) -> Any:
        """处理单帧图像
        
        子类需要重写此方法以实现具体的图像处理逻辑。
        
        Args:
            image: 输入图像
            
        Returns:
            Any: 处理结果
        """
        ...
        
    def stop(self) -> None:
        """停止处理线程并释放资源"""
        ... 