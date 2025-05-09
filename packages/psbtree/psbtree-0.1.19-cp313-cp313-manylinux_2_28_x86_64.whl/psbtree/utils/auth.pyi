#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
授权验证工具模块

该模块提供了用于函数授权验证的装饰器。
用于确保只有经过授权的用户才能执行特定的函数。
"""

from functools import wraps
from typing import Callable, TypeVar, Any
from psbtree import check_authorization

T = TypeVar('T')

def require_authorization(func: Callable[..., T]) -> Callable[..., T]:
    """授权验证装饰器
    
    用于装饰需要授权验证的函数。在执行被装饰的函数之前，
    会先检查当前用户是否有权限执行该函数。
    
    Args:
        func: 需要授权验证的函数
        
    Returns:
        Callable[..., T]: 包装后的函数，在执行原函数前会进行授权检查
        
    Raises:
        PermissionError: 如果用户没有执行该函数的权限
    """
    ... 