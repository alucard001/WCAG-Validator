#!/usr/bin/env python3
"""
WCAG验证器命令行接口
"""
import argparse
import sys
import os

from wcag_validator import validate_file, validate_url, validate_html, generate_report

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='WCAG 2.2 验证工具')
    parser.add_argument('source', help='HTML文件路径或URL')
    parser.add_argument('--level', choices=['A', 'AA', 'AAA'], default='AA',
                        help='WCAG合规级别 (默认: AA)')
    parser.add_argument('--format', choices=['json', 'html', 'markdown', 'console'],
                        default='console', help='输出格式 (默认: console)')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 判断输入是文件、URL还是HTML字符串
    if args.source.startswith(('http://', 'https://')):
        print(f"正在验证URL: {args.source}")
        report = validate_url(args.source, wcag_level=args.level)
    elif os.path.isfile(args.source):
        print(f"正在验证文件: {args.source}")
        report = validate_file(args.source, wcag_level=args.level)
    else:
        print("正在验证HTML字符串")
        with open(args.source, 'r', encoding='utf-8') as f:
            html_content = f.read()
        report = validate_html(html_content, wcag_level=args.level)
    
    # 生成报告
    output = generate_report(report, format=args.format)
    
    # 输出报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"报告已保存到: {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
