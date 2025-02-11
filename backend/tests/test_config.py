from app.core.config import settings
import os

def test_base_dir():
    """测试基础目录配置"""
    assert settings.BASE_DIR.exists()
    assert settings.BASE_DIR.is_dir()
    assert settings.BASE_DIR.name == "backend"

def test_export_dir():
    """测试导出目录配置"""
    settings.setup_directories()
    assert settings.EXPORT_DIR.exists()
    assert settings.EXPORT_DIR.is_dir()
    assert settings.EXPORT_DIR.name == "export"

def test_notebooks_dir():
    """测试笔记本目录配置"""
    settings.setup_directories()
    assert settings.NOTEBOOKS_DIR.exists()
    assert settings.NOTEBOOKS_DIR.is_dir()
    assert settings.NOTEBOOKS_DIR.name == "notebooks"

def test_data_dir():
    """测试数据目录配置"""
    settings.setup_directories()
    assert settings.DATA_DIR.exists()
    assert settings.DATA_DIR.is_dir()
    assert settings.DATA_DIR.name == "data"

def test_temp_dir():
    """测试临时目录配置"""
    settings.setup_directories()
    assert settings.TEMP_DIR.exists()
    assert settings.TEMP_DIR.is_dir()
    assert settings.TEMP_DIR.name == "temp" 