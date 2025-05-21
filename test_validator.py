#!/usr/bin/env python3
"""
WCAG验证器测试脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wcag_validator import validate_file, generate_report

def main():
    """主函数"""
    # 验证测试样例
    test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_sample.html')
    
    print(f"正在验证文件: {test_file}")
    report = validate_file(test_file, wcag_level='AA')
    
    # 生成HTML报告
    html_report = generate_report(report, format='html')
    html_report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_report.html')
    with open(html_report_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    print(f"HTML报告已生成: {html_report_path}")
    
    # 生成Markdown报告
    md_report = generate_report(report, format='markdown')
    md_report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_report.md')
    with open(md_report_path, 'w', encoding='utf-8') as f:
        f.write(md_report)
    print(f"Markdown报告已生成: {md_report_path}")
    
    # 打印控制台报告
    console_report = generate_report(report, format='console')
    print("\n" + "=" * 80)
    print(console_report)

if __name__ == "__main__":
    main()
