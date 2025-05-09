#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
行为树包

该包提供了行为树的核心功能，包括：
1. 行为树节点定义和管理
2. 行为树执行引擎
3. 授权验证机制
4. 工具函数和辅助类

主要组件：
- core: 核心类和接口
- nodes: 节点实现
- engine: 执行引擎
- utils: 工具函数
- plugins: 插件系统

使用示例：
```python
from psbtree import BehaviorTreeFactory, Tree

# 创建行为树工厂
factory = BehaviorTreeFactory()

# 从XML文本创建行为树
tree = factory.createTreeFromText(xml_text)

# 执行行为树
status = tree.tickOnce()
```
"""