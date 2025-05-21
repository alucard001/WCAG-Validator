"""
报告生成模块，负责生成详细的验证报告
"""
import json
import html
from datetime import datetime

class ReportGenerator:
    """报告生成器，用于生成各种格式的验证报告"""
    
    def __init__(self, validation_report):
        """
        初始化报告生成器
        
        参数:
            validation_report: ValidationReport对象
        """
        self.report = validation_report
    
    def to_dict(self):
        """
        转换为字典格式
        
        返回:
            报告字典
        """
        return {
            "url": self.report.url,
            "timestamp": datetime.now().isoformat(),
            "summary": self.report.summary,
            "issues": [self._issue_to_dict(issue) for issue in self.report.issues]
        }
    
    def to_json(self, indent=2):
        """
        转换为JSON格式
        
        参数:
            indent: JSON缩进
            
        返回:
            JSON字符串
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def to_html(self):
        """
        转换为HTML格式
        
        返回:
            HTML字符串
        """
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='zh-CN'>",
            "<head>",
            "    <meta charset='utf-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1'>",
            "    <title>WCAG 2.2 验证报告</title>",
            "    <style>",
            "        :root {",
            "            --primary-color: #2c3e50;",
            "            --secondary-color: #3498db;",
            "            --success-color: #2ecc71;",
            "            --warning-color: #f39c12;",
            "            --danger-color: #e74c3c;",
            "            --light-color: #f8f9fa;",
            "            --dark-color: #343a40;",
            "        }",
            "        body {",
            "            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;",
            "            line-height: 1.6;",
            "            color: var(--dark-color);",
            "            margin: 0;",
            "            padding: 0;",
            "            background-color: #f5f5f5;",
            "        }",
            "        .container {",
            "            max-width: 1200px;",
            "            margin: 0 auto;",
            "            padding: 20px;",
            "        }",
            "        header {",
            "            background-color: var(--primary-color);",
            "            color: white;",
            "            padding: 20px;",
            "            margin-bottom: 20px;",
            "            border-radius: 5px;",
            "        }",
            "        h1, h2, h3, h4 {",
            "            margin-top: 0;",
            "        }",
            "        .summary {",
            "            background-color: white;",
            "            padding: 20px;",
            "            border-radius: 5px;",
            "            box-shadow: 0 2px 5px rgba(0,0,0,0.1);",
            "            margin-bottom: 20px;",
            "        }",
            "        .summary-grid {",
            "            display: grid;",
            "            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));",
            "            gap: 15px;",
            "            margin-top: 15px;",
            "        }",
            "        .summary-item {",
            "            padding: 15px;",
            "            border-radius: 5px;",
            "            text-align: center;",
            "        }",
            "        .summary-item.total {",
            "            background-color: var(--primary-color);",
            "            color: white;",
            "        }",
            "        .summary-item.level-a {",
            "            background-color: var(--danger-color);",
            "            color: white;",
            "        }",
            "        .summary-item.level-aa {",
            "            background-color: var(--warning-color);",
            "            color: white;",
            "        }",
            "        .summary-item.level-aaa {",
            "            background-color: var(--secondary-color);",
            "            color: white;",
            "        }",
            "        .summary-item.passed {",
            "            background-color: var(--success-color);",
            "            color: white;",
            "        }",
            "        .summary-item.failed {",
            "            background-color: var(--danger-color);",
            "            color: white;",
            "        }",
            "        .issue {",
            "            background-color: white;",
            "            padding: 20px;",
            "            border-radius: 5px;",
            "            box-shadow: 0 2px 5px rgba(0,0,0,0.1);",
            "            margin-bottom: 20px;",
            "        }",
            "        .issue-header {",
            "            display: flex;",
            "            justify-content: space-between;",
            "            align-items: center;",
            "            margin-bottom: 15px;",
            "            padding-bottom: 10px;",
            "            border-bottom: 1px solid #eee;",
            "        }",
            "        .issue-title {",
            "            margin: 0;",
            "            font-size: 1.2rem;",
            "        }",
            "        .issue-badge {",
            "            padding: 5px 10px;",
            "            border-radius: 3px;",
            "            font-weight: bold;",
            "            font-size: 0.8rem;",
            "        }",
            "        .issue-badge.level-A {",
            "            background-color: var(--danger-color);",
            "            color: white;",
            "        }",
            "        .issue-badge.level-AA {",
            "            background-color: var(--warning-color);",
            "            color: white;",
            "        }",
            "        .issue-badge.level-AAA {",
            "            background-color: var(--secondary-color);",
            "            color: white;",
            "        }",
            "        .issue-description {",
            "            margin-bottom: 15px;",
            "        }",
            "        .issue-location {",
            "            font-family: monospace;",
            "            background-color: #f8f9fa;",
            "            padding: 5px 10px;",
            "            border-radius: 3px;",
            "            margin-bottom: 15px;",
            "        }",
            "        .code-block {",
            "            background-color: #f8f9fa;",
            "            padding: 15px;",
            "            border-radius: 5px;",
            "            overflow-x: auto;",
            "            font-family: monospace;",
            "            margin-bottom: 15px;",
            "            white-space: pre-wrap;",
            "            border-left: 4px solid var(--danger-color);",
            "        }",
            "        .fix-suggestions {",
            "            background-color: #e8f4f8;",
            "            padding: 15px;",
            "            border-radius: 5px;",
            "            margin-bottom: 15px;",
            "            border-left: 4px solid var(--secondary-color);",
            "        }",
            "        .fix-suggestions h4 {",
            "            margin-top: 0;",
            "            color: var(--secondary-color);",
            "        }",
            "        .fix-suggestions ul {",
            "            margin-bottom: 0;",
            "        }",
            "        .code-examples {",
            "            background-color: #f0f7f0;",
            "            padding: 15px;",
            "            border-radius: 5px;",
            "            margin-bottom: 15px;",
            "            border-left: 4px solid var(--success-color);",
            "        }",
            "        .code-examples h4 {",
            "            margin-top: 0;",
            "            color: var(--success-color);",
            "        }",
            "        .code-example {",
            "            background-color: white;",
            "            padding: 15px;",
            "            border-radius: 5px;",
            "            margin-bottom: 10px;",
            "            font-family: monospace;",
            "            white-space: pre-wrap;",
            "        }",
            "        .code-example:last-child {",
            "            margin-bottom: 0;",
            "        }",
            "        .code-example-description {",
            "            font-style: italic;",
            "            margin-top: 5px;",
            "            color: #666;",
            "        }",
            "        .wcag-reference {",
            "            margin-top: 15px;",
            "            font-size: 0.9rem;",
            "        }",
            "        .wcag-reference a {",
            "            color: var(--secondary-color);",
            "            text-decoration: none;",
            "        }",
            "        .wcag-reference a:hover {",
            "            text-decoration: underline;",
            "        }",
            "        footer {",
            "            text-align: center;",
            "            margin-top: 30px;",
            "            padding: 20px;",
            "            color: #666;",
            "            font-size: 0.9rem;",
            "        }",
            "        @media (max-width: 768px) {",
            "            .summary-grid {",
            "                grid-template-columns: repeat(2, 1fr);",
            "            }",
            "        }",
            "        @media (max-width: 480px) {",
            "            .summary-grid {",
            "                grid-template-columns: 1fr;",
            "            }",
            "            .issue-header {",
            "                flex-direction: column;",
            "                align-items: flex-start;",
            "            }",
            "            .issue-badge {",
            "                margin-top: 10px;",
            "            }",
            "        }",
            "    </style>",
            "</head>",
            "<body>",
            "    <div class='container'>",
            "        <header>",
            f"            <h1>WCAG 2.2 验证报告</h1>",
            f"            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        ]
        
        if self.report.url:
            html_parts.append(f"            <p>URL: {html.escape(self.report.url)}</p>")
        
        html_parts.extend([
            "        </header>",
            "",
            "        <div class='summary'>",
            "            <h2>摘要</h2>",
            "            <div class='summary-grid'>",
            f"                <div class='summary-item total'><h3>{self.report.summary['total_issues']}</h3><p>总问题数</p></div>",
            f"                <div class='summary-item level-a'><h3>{self.report.summary['level_A_issues']}</h3><p>A级问题</p></div>",
            f"                <div class='summary-item level-aa'><h3>{self.report.summary['level_AA_issues']}</h3><p>AA级问题</p></div>",
            f"                <div class='summary-item level-aaa'><h3>{self.report.summary['level_AAA_issues']}</h3><p>AAA级问题</p></div>",
            f"                <div class='summary-item passed'><h3>{self.report.summary['passed_rules']}</h3><p>通过规则</p></div>",
            f"                <div class='summary-item failed'><h3>{self.report.summary['failed_rules']}</h3><p>失败规则</p></div>",
            "            </div>",
            "        </div>"
        ])
        
        if self.report.issues:
            html_parts.append("        <h2>问题详情</h2>")
            
            for i, issue in enumerate(self.report.issues, 1):
                html_parts.extend([
                    "        <div class='issue'>",
                    "            <div class='issue-header'>",
                    f"                <h3 class='issue-title'>{i}. {html.escape(issue.rule.name)}</h3>",
                    f"                <span class='issue-badge level-{issue.rule.level}'>WCAG {issue.rule.wcag_criterion} (级别 {issue.rule.level})</span>",
                    "            </div>",
                    f"            <div class='issue-description'>{html.escape(issue.description)}</div>"
                ])
                
                if issue.location:
                    html_parts.append(f"            <div class='issue-location'>{html.escape(issue.location)}</div>")
                
                if issue.element_html:
                    html_parts.append(f"            <div class='code-block'>{html.escape(issue.element_html)}</div>")
                
                if issue.fix_suggestions:
                    html_parts.append("            <div class='fix-suggestions'>")
                    html_parts.append("                <h4>修复建议:</h4>")
                    html_parts.append("                <ul>")
                    for suggestion in issue.fix_suggestions:
                        html_parts.append(f"                    <li>{html.escape(suggestion)}</li>")
                    html_parts.append("                </ul>")
                    html_parts.append("            </div>")
                
                if issue.code_examples:
                    html_parts.append("            <div class='code-examples'>")
                    html_parts.append("                <h4>代码示例:</h4>")
                    for example in issue.code_examples:
                        html_parts.append(f"                <div class='code-example'>{html.escape(example['code'])}</div>")
                        if example.get('description'):
                            html_parts.append(f"                <div class='code-example-description'>{html.escape(example['description'])}</div>")
                    html_parts.append("            </div>")
                
                # 添加WCAG参考链接
                wcag_ref = self._get_wcag_reference(issue.rule.wcag_criterion)
                if wcag_ref:
                    html_parts.append(f"            <div class='wcag-reference'><a href='{wcag_ref}' target='_blank'>了解更多关于 WCAG {issue.rule.wcag_criterion} 的信息</a></div>")
                
                html_parts.append("        </div>")
        else:
            html_parts.extend([
                "        <div class='issue'>",
                "            <h3>恭喜！</h3>",
                "            <p>未发现无障碍问题。</p>",
                "        </div>"
            ])
        
        html_parts.extend([
            "        <footer>",
            "            <p>由 WCAG 2.2 验证器生成</p>",
            "        </footer>",
            "    </div>",
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html_parts)
    
    def to_markdown(self):
        """
        转换为Markdown格式
        
        返回:
            Markdown字符串
        """
        md_parts = [
            "# WCAG 2.2 验证报告",
            "",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        if self.report.url:
            md_parts.append(f"URL: {self.report.url}")
        
        md_parts.extend([
            "",
            "## 摘要",
            "",
            f"- **总问题数:** {self.report.summary['total_issues']}",
            f"- **A级问题:** {self.report.summary['level_A_issues']}",
            f"- **AA级问题:** {self.report.summary['level_AA_issues']}",
            f"- **AAA级问题:** {self.report.summary['level_AAA_issues']}",
            f"- **通过规则:** {self.report.summary['passed_rules']}",
            f"- **失败规则:** {self.report.summary['failed_rules']}",
            ""
        ])
        
        if self.report.issues:
            md_parts.append("## 问题详情")
            md_parts.append("")
            
            for i, issue in enumerate(self.report.issues, 1):
                md_parts.extend([
                    f"### {i}. {issue.rule.name}",
                    "",
                    f"**WCAG标准:** {issue.rule.wcag_criterion} (级别 {issue.rule.level})",
                    "",
                    f"**问题描述:** {issue.description}",
                    ""
                ])
                
                if issue.location:
                    md_parts.append(f"**位置:** `{issue.location}`")
                    md_parts.append("")
                
                if issue.element_html:
                    md_parts.append("**问题代码:**")
                    md_parts.append("```html")
                    md_parts.append(issue.element_html)
                    md_parts.append("```")
                    md_parts.append("")
                
                if issue.fix_suggestions:
                    md_parts.append("**修复建议:**")
                    md_parts.append("")
                    for suggestion in issue.fix_suggestions:
                        md_parts.append(f"- {suggestion}")
                    md_parts.append("")
                
                if issue.code_examples:
                    md_parts.append("**代码示例:**")
                    md_parts.append("")
                    for example in issue.code_examples:
                        md_parts.append("```html")
                        md_parts.append(example['code'])
                        md_parts.append("```")
                        if example.get('description'):
                            md_parts.append(f"*{example['description']}*")
                        md_parts.append("")
                
                # 添加WCAG参考链接
                wcag_ref = self._get_wcag_reference(issue.rule.wcag_criterion)
                if wcag_ref:
                    md_parts.append(f"[了解更多关于 WCAG {issue.rule.wcag_criterion} 的信息]({wcag_ref})")
                    md_parts.append("")
                
                md_parts.append("---")
                md_parts.append("")
        else:
            md_parts.extend([
                "## 结果",
                "",
                "恭喜！未发现无障碍问题。",
                ""
            ])
        
        md_parts.append("*由 WCAG 2.2 验证器生成*")
        
        return "\n".join(md_parts)
    
    def to_console(self):
        """
        转换为控制台格式
        
        返回:
            控制台输出字符串
        """
        console_parts = [
            "=" * 80,
            "WCAG 2.2 验证报告",
            "=" * 80,
            "",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        if self.report.url:
            console_parts.append(f"URL: {self.report.url}")
        
        console_parts.extend([
            "",
            "摘要:",
            f"- 总问题数: {self.report.summary['total_issues']}",
            f"- A级问题: {self.report.summary['level_A_issues']}",
            f"- AA级问题: {self.report.summary['level_AA_issues']}",
            f"- AAA级问题: {self.report.summary['level_AAA_issues']}",
            f"- 通过规则: {self.report.summary['passed_rules']}",
            f"- 失败规则: {self.report.summary['failed_rules']}",
            ""
        ])
        
        if self.report.issues:
            console_parts.append("问题详情:")
            console_parts.append("-" * 80)
            
            for i, issue in enumerate(self.report.issues, 1):
                console_parts.extend([
                    f"{i}. {issue.rule.name}",
                    f"   WCAG标准: {issue.rule.wcag_criterion} (级别 {issue.rule.level})",
                    f"   问题描述: {issue.description}"
                ])
                
                if issue.location:
                    console_parts.append(f"   位置: {issue.location}")
                
                if issue.element_html:
                    console_parts.append("   问题代码:")
                    for line in issue.element_html.split("\n"):
                        console_parts.append(f"      {line}")
                
                if issue.fix_suggestions:
                    console_parts.append("   修复建议:")
                    for suggestion in issue.fix_suggestions:
                        console_parts.append(f"   - {suggestion}")
                
                if issue.code_examples:
                    console_parts.append("   代码示例:")
                    for example in issue.code_examples:
                        for line in example['code'].split("\n"):
                            console_parts.append(f"      {line}")
                        if example.get('description'):
                            console_parts.append(f"      ({example['description']})")
                
                console_parts.append("")
        else:
            console_parts.extend([
                "结果:",
                "恭喜！未发现无障碍问题。",
                ""
            ])
        
        console_parts.append("由 WCAG 2.2 验证器生成")
        
        return "\n".join(console_parts)
    
    def _issue_to_dict(self, issue):
        """
        将Issue对象转换为字典
        
        参数:
            issue: Issue对象
            
        返回:
            字典
        """
        return {
            "rule_id": issue.rule.id,
            "rule_name": issue.rule.name,
            "wcag_criterion": issue.rule.wcag_criterion,
            "level": issue.rule.level,
            "description": issue.description,
            "impact": issue.impact,
            "location": issue.location,
            "element_html": issue.element_html,
            "fix_suggestions": issue.fix_suggestions,
            "code_examples": issue.code_examples
        }
    
    def _get_wcag_reference(self, criterion):
        """
        获取WCAG参考链接
        
        参数:
            criterion: WCAG标准编号
            
        返回:
            参考链接
        """
        # 提取主要部分，如1.1.1
        parts = criterion.split('.')
        if len(parts) >= 3:
            principle, guideline, criterion = parts[:3]
            return f"https://www.w3.org/WAI/WCAG22/Understanding/{principle}-{guideline}-{criterion}.html"
        
        return ""
