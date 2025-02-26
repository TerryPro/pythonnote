# 代码示例模块 API 管理

## 概述

本模块实现了代码示例的管理功能，包括分类管理和示例管理。为了更好地组织代码和提高可维护性，我们将所有与后端API交互的代码集中到 `example_api.js` 文件中管理。

## API 文件结构

`example_api.js` 文件封装了所有与代码示例相关的API调用，主要包括以下功能：

1. 分类管理：
   - 获取所有分类
   - 创建新分类
   - 更新分类

2. 示例管理：
   - 获取指定分类下的所有示例
   - 创建新示例
   - 更新示例
   - 删除示例
   - 从单元格保存示例

## API 函数列表

### 分类管理

- `fetchCategories()`: 获取所有代码示例分类
- `createCategory(categoryData)`: 创建新的代码示例分类
- `updateCategory(categoryId, categoryData)`: 更新代码示例分类

### 示例管理

- `fetchExamplesByCategory(categoryId)`: 获取指定分类下的所有代码示例
- `createExample(exampleData)`: 创建新的代码示例
- `updateExample(exampleId, exampleData)`: 更新代码示例
- `deleteExample(exampleId)`: 删除代码示例
- `saveFromCell(data)`: 从单元格保存代码示例

## 使用方法

在组件中使用这些API函数非常简单，只需导入所需的函数并调用即可：

```javascript
import { fetchCategories, createExample } from './example_api'

// 获取所有分类
const loadCategories = async () => {
  try {
    const categories = await fetchCategories()
    // 处理返回的分类数据
  } catch (error) {
    // 错误处理
  }
}

// 创建新示例
const saveExample = async () => {
  try {
    const result = await createExample({
      title: '示例标题',
      description: '示例描述',
      code: 'print("Hello, World!")',
      tags: ['基础语法'],
      category_id: 'category_id'
    })
    // 处理返回结果
  } catch (error) {
    // 错误处理
  }
}
```

## 错误处理

所有API函数都包含了基本的错误处理逻辑，会在控制台输出错误信息，并将错误向上抛出，以便调用者可以进行更具体的错误处理。

## 维护与扩展

如果需要添加新的API调用，只需在 `example_api.js` 文件中添加相应的函数，并确保遵循相同的错误处理模式。这样可以保持代码的一致性和可维护性。 