#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, Tuple, Dict, Any
import numpy as np
import threading

class ParallVideoCapture:
    """并行视频捕获类
    
    该类提供了一个线程安全的视频捕获实现，支持视频的播放、暂停、跳转等功能。
    使用独立线程进行视频帧的读取，避免阻塞主线程。
    
    Attributes:
        video_path (str): 视频文件路径
        auto_reload (bool): 是否在视频播放结束时自动重新加载
    """
    
    def __init__(self, video_path: str, auto_reload: bool = True) -> None:
        """初始化视频捕获器
        
        Args:
            video_path: 视频文件路径
            auto_reload: 是否在视频播放结束时自动重新加载，默认为True
        """
        ...
    
    def start(self) -> bool:
        """启动视频捕获线程
        
        Returns:
            bool: 启动是否成功
        """
        ...
        
    def stop(self) -> None:
        """停止视频捕获线程并释放资源"""
        ...
        
    def pause(self) -> None:
        """暂停视频捕获"""
        ...
        
    def resume(self) -> None:
        """恢复视频捕获"""
        ...
        
    def seek(self, frame_number: int) -> bool:
        """跳转到指定帧
        
        Args:
            frame_number: 目标帧号
            
        Returns:
            bool: 跳转是否成功
        """
        ...
        
    def get_frame(self, wait_for_frame: bool = False, timeout: float = 0.1) -> Optional[np.ndarray]:
        """获取当前帧
        
        Args:
            wait_for_frame: 是否等待新帧，默认为False
            timeout: 等待超时时间（秒），默认为0.1秒
            
        Returns:
            Optional[np.ndarray]: 当前帧，如果没有可用帧则返回None
        """
        ...
        
    def get_frame_with_number(self) -> Tuple[Optional[int], Optional[np.ndarray]]:
        """获取当前帧及其帧号
        
        Returns:
            Tuple[Optional[int], Optional[np.ndarray]]: (帧号, 帧数据)，如果没有可用帧则返回(None, None)
        """
        ...
        
    def get_video_info(self) -> Dict[str, Any]:
        """获取视频信息
        
        Returns:
            Dict[str, Any]: 包含视频信息的字典，包括宽度、高度、帧率、总帧数等
        """
        ...
        
    def is_running(self) -> bool:
        """检查视频捕获是否正在运行
        
        Returns:
            bool: 是否正在运行
        """
        ...
        
    def is_paused(self) -> bool:
        """检查视频捕获是否已暂停
        
        Returns:
            bool: 是否已暂停
        """
        ... 