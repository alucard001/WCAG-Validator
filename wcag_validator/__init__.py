"""
WCAG验证器主模块，提供对外接口
"""
from .core.validator import WCAGValidator
from .core.report import ReportGenerator

def validate_html(html_content, wcag_level='AA', url=None):
    """
    验证HTML内容
    
    参数:
        html_content: HTML字符串
        wcag_level: 验证级别 ('A', 'AA', 'AAA')
        url: 可选的URL，用于报告中
        
    返回:
        ValidationReport对象
    """
    validator = WCAGValidator(wcag_level=wcag_level)
    return validator.validate_html(html_content, url)

def validate_file(file_path, wcag_level='AA'):
    """
    验证HTML文件
    
    参数:
        file_path: HTML文件路径
        wcag_level: 验证级别 ('A', 'AA', 'AAA')
        
    返回:
        ValidationReport对象
    """
    validator = WCAGValidator(wcag_level=wcag_level)
    return validator.validate_file(file_path)

def validate_url(url, wcag_level='AA'):
    """
    验证URL指向的网页
    
    参数:
        url: 网页URL
        wcag_level: 验证级别 ('A', 'AA', 'AAA')
        
    返回:
        ValidationReport对象
    """
    validator = WCAGValidator(wcag_level=wcag_level)
    return validator.validate_url(url)

def generate_report(report, format='html'):
    """
    生成报告
    
    参数:
        report: ValidationReport对象
        format: 报告格式 ('html', 'markdown', 'json', 'console')
        
    返回:
        报告字符串
    """
    generator = ReportGenerator(report)
    
    if format.lower() == 'html':
        return generator.to_html()
    elif format.lower() == 'markdown':
        return generator.to_markdown()
    elif format.lower() == 'json':
        return generator.to_json()
    elif format.lower() == 'console':
        return generator.to_console()
    else:
        raise ValueError(f"不支持的报告格式: {format}")
