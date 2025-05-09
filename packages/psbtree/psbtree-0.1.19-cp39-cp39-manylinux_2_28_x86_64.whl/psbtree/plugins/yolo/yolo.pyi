#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List, Optional
import numpy as np
from psbtree.plugins.yolo.infer import VisionInfer

class ModelType(Enum):
    """YOLO模型类型枚举
    
    定义了支持的YOLO模型类型，包括标准YOLO、YOLOE和YOLO-World。
    """
    YOLO = "yolo"  # 标准YOLO模型
    YOLOE = "yoloe"  # YOLOE模型
    YOLO_WORLD = "yolo_world"  # YOLO-World模型

class YoloThreadedInfer(VisionInfer):
    """YOLO线程化推理类
    
    该类提供了基于YOLO模型的线程化目标检测实现，支持多种YOLO模型变体。
    使用独立线程进行模型推理，避免阻塞主线程。
    
    Attributes:
        model_type (ModelType): 当前使用的YOLO模型类型
        names (List[str]): 类别名称列表
        task (str): 任务类型，如"detect"或"track"
    """
    
    def _init_algorithm(self, model_path: str, names: List[str], task: str = "detect", verbose: bool = False) -> None:
        """初始化YOLO模型
        
        Args:
            model_path: 模型文件路径
            names: 类别名称列表
            task: 任务类型，默认为"detect"
            verbose: 是否显示详细日志，默认为False
        """
        ...
        
    def _process(self, image: np.ndarray) -> List:
        """处理单帧图像
        
        Args:
            image: 输入图像
            
        Returns:
            List: 检测结果列表
        """
        ...
        
    def update_classes(self, names: List[str]) -> None:
        """更新模型类别
        
        Args:
            names: 新的类别名称列表
        """
        ... 