"""
HTML解析模块，负责解析HTML文档并构建DOM树
"""
import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class HTMLParser:
    """HTML解析器，用于解析HTML内容并提供DOM访问"""
    
    def __init__(self):
        """初始化解析器"""
        self.document = None
        self.url = None
        self.source_code = None
        self.line_positions = []
    
    def parse_html(self, html_content, url=None):
        """
        解析HTML内容
        
        参数:
            html_content: HTML字符串
            url: 可选的URL，用于报告中
            
        返回:
            BeautifulSoup对象
        """
        self.source_code = html_content
        self.url = url
        
        # 计算行位置，用于后续定位元素
        self._calculate_line_positions()
        
        # 使用html.parser解析器，保留原始HTML结构
        self.document = BeautifulSoup(html_content, 'html.parser')
        
        return self.document
    
    def parse_file(self, file_path):
        """
        解析HTML文件
        
        参数:
            file_path: HTML文件路径
            
        返回:
            BeautifulSoup对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return self.parse_html(html_content, url=f"file://{os.path.abspath(file_path)}")
    
    def parse_url(self, url):
        """
        解析URL指向的网页
        
        参数:
            url: 网页URL
            
        返回:
            BeautifulSoup对象
        """
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败则抛出异常
        
        return self.parse_html(response.text, url=url)
    
    def get_element_position(self, element):
        """
        获取元素在源代码中的位置
        
        参数:
            element: BeautifulSoup元素
            
        返回:
            (行号, 列号)元组
        """
        if not self.source_code or not element:
            return (0, 0)
        
        # 获取元素在源代码中的位置
        element_str = str(element)
        start_pos = self.source_code.find(element_str)
        
        if start_pos == -1:
            return (0, 0)
        
        # 二分查找确定行号
        line = self._find_line_number(start_pos)
        column = start_pos - self.line_positions[line - 1] + 1 if line > 0 else start_pos + 1
        
        return (line, column)
    
    def get_element_path(self, element):
        """
        获取元素的XPath路径
        
        参数:
            element: BeautifulSoup元素
            
        返回:
            XPath字符串
        """
        if not element:
            return ""
        
        path_parts = []
        current = element
        
        while current and current.name:
            # 计算同名兄弟元素中的索引
            siblings = current.find_previous_siblings(current.name)
            index = len(list(siblings)) + 1
            
            if index > 1:
                path_parts.append(f"{current.name}[{index}]")
            else:
                path_parts.append(current.name)
            
            current = current.parent
        
        return "/" + "/".join(reversed(path_parts))
    
    def get_element_html(self, element, max_length=100):
        """
        获取元素的HTML代码
        
        参数:
            element: BeautifulSoup元素
            max_length: 最大长度
            
        返回:
            HTML字符串
        """
        if not element:
            return ""
        
        html = str(element)
        if len(html) > max_length:
            html = html[:max_length] + "..."
        
        return html
    
    def _calculate_line_positions(self):
        """计算源代码中每行的起始位置"""
        if not self.source_code:
            return
        
        self.line_positions = [0]
        pos = 0
        
        for line in self.source_code.splitlines():
            pos += len(line) + 1  # +1 for newline character
            self.line_positions.append(pos)
    
    def _find_line_number(self, position):
        """二分查找确定位置对应的行号"""
        if not self.line_positions:
            return 0
        
        left, right = 0, len(self.line_positions) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if self.line_positions[mid] <= position:
                if mid == len(self.line_positions) - 1 or self.line_positions[mid + 1] > position:
                    return mid + 1
                left = mid + 1
            else:
                right = mid - 1
        
        return 0
