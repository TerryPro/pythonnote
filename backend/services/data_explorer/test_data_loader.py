import pandas as pd
import os
import sys

# 添加父目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from data_loader import DataLoader, DataLoadError

def test_basic_functionality():
    """测试基本的DataFrame加载功能"""
    # 创建测试数据
    test_data = {
        '姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '分数': [85.5, 92.0, 88.5]
    }
    df = pd.DataFrame(test_data)
    
    # 初始化DataLoader
    loader = DataLoader()
    
    # 测试加载DataFrame
    preview = loader.load_dataframe(df)
    
    # 打印预览信息
    print("\n=== DataFrame加载测试 ===")
    print("=== 数据基本信息 ===")
    print(preview['info'])
    print("\n=== 数据预览 ===")
    print(preview['head'])
    print("\n=== 数据统计 ===")
    print(preview['summary'])

def test_csv_loading():
    """测试CSV文件加载功能"""
    loader = DataLoader()
    
    try:
        # 测试加载CSV文件
        csv_path = os.path.join(current_dir, 'test_data.csv')
        preview = loader.load_csv(csv_path)
        
        print("\n=== CSV加载测试 ===")
        print("=== 文件信息 ===")
        print(preview['file_info'])
        print("\n=== 数据基本信息 ===")
        print(preview['info'])
        print("\n=== 数据预览 ===")
        print(preview['head'])
        print("\n=== 数据统计 ===")
        print(preview['summary'])
        
    except DataLoadError as e:
        print(f"加载CSV文件失败: {str(e)}")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

def create_test_excel():
    """创建测试用的Excel文件"""
    # 创建测试数据
    df1 = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '分数': [85.5, 92.0, 88.5, 90.0, 87.5],
        '城市': ['北京', '上海', '广州', '深圳', '杭州']
    })
    
    df2 = pd.DataFrame({
        '科目': ['语文', '数学', '英语', '物理', '化学'],
        '平均分': [80, 85, 88, 82, 86],
        '及格率': [0.9, 0.85, 0.92, 0.88, 0.87]
    })
    
    # 创建Excel文件
    excel_path = os.path.join(current_dir, 'test_data.xlsx')
    with pd.ExcelWriter(excel_path) as writer:
        df1.to_excel(writer, sheet_name='学生信息', index=False)
        df2.to_excel(writer, sheet_name='成绩统计', index=False)
    
    return excel_path

def test_excel_loading():
    """测试Excel文件加载功能"""
    loader = DataLoader()
    
    try:
        # 创建测试Excel文件
        excel_path = create_test_excel()
        
        # 测试加载第一个工作表
        print("\n=== Excel加载测试（第一个工作表）===")
        preview1 = loader.load_excel(excel_path)
        print("=== 文件信息 ===")
        print(preview1['file_info'])
        print("\n=== 数据基本信息 ===")
        print(preview1['info'])
        print("\n=== 数据预览 ===")
        print(preview1['head'])
        
        # 测试加载第二个工作表
        print("\n=== Excel加载测试（第二个工作表）===")
        preview2 = loader.load_excel(excel_path, sheet_name='成绩统计')
        print("=== 文件信息 ===")
        print(preview2['file_info'])
        print("\n=== 数据基本信息 ===")
        print(preview2['info'])
        print("\n=== 数据预览 ===")
        print(preview2['head'])
        
    except DataLoadError as e:
        print(f"加载Excel文件失败: {str(e)}")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

def test_error_handling():
    """测试错误处理"""
    loader = DataLoader()
    
    print("\n=== 错误处理测试 ===")
    
    # 测试加载不存在的文件
    try:
        loader.load_csv('not_exists.csv')
    except DataLoadError as e:
        print(f"预期的错误 - 文件不存在: {str(e)}")
    
    # 测试加载空DataFrame
    try:
        loader.load_dataframe(pd.DataFrame())
    except DataLoadError as e:
        print(f"预期的错误 - 空DataFrame: {str(e)}")
    
    # 测试加载不支持的文件格式
    try:
        loader.load_excel('test_data.txt')
    except DataLoadError as e:
        print(f"预期的错误 - 不支持的文件格式: {str(e)}")
    
    # 测试加载不存在的工作表
    try:
        excel_path = create_test_excel()
        loader.load_excel(excel_path, sheet_name='不存在的工作表')
    except DataLoadError as e:
        print(f"预期的错误 - 工作表不存在: {str(e)}")

if __name__ == '__main__':
    test_basic_functionality()
    test_csv_loading()
    test_excel_loading()
    test_error_handling() 