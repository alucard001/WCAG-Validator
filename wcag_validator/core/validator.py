"""
验证器主类，负责协调验证流程和生成报告
"""
from .parser import HTMLParser
from ..rules.base import RuleRegistry

class ValidationReport:
    """验证报告类"""
    
    def __init__(self, url=None):
        self.url = url
        self.issues = []  # 问题列表
        self.passed_rules = []  # 通过的规则
        self.failed_rules = []  # 失败的规则
        self.summary = {
            "total_issues": 0,
            "level_A_issues": 0,
            "level_AA_issues": 0,
            "level_AAA_issues": 0,
            "passed_rules": 0,
            "failed_rules": 0
        }
    
    def add_issue(self, issue):
        """添加问题"""
        self.issues.append(issue)
        self.summary["total_issues"] += 1
        
        # 更新按级别统计
        if issue.rule.level == "A":
            self.summary["level_A_issues"] += 1
        elif issue.rule.level == "AA":
            self.summary["level_AA_issues"] += 1
        elif issue.rule.level == "AAA":
            self.summary["level_AAA_issues"] += 1
        
        # 更新失败规则列表
        if issue.rule not in self.failed_rules:
            self.failed_rules.append(issue.rule)
            self.summary["failed_rules"] = len(self.failed_rules)
    
    def add_passed_rule(self, rule):
        """添加通过的规则"""
        if rule not in self.passed_rules:
            self.passed_rules.append(rule)
            self.summary["passed_rules"] = len(self.passed_rules)
    
    def get_issues_by_criterion(self, criterion):
        """按WCAG标准获取问题"""
        return [issue for issue in self.issues if issue.rule.wcag_criterion == criterion]
    
    def get_issues_by_level(self, level):
        """按级别获取问题"""
        return [issue for issue in self.issues if issue.rule.level == level]
    
    def to_dict(self):
        """转换为字典"""
        return {
            "url": self.url,
            "summary": self.summary,
            "issues": [issue.to_dict() for issue in self.issues]
        }
    
    def to_json(self):
        """转换为JSON"""
        import json
        return json.dumps(self.to_dict(), indent=2)
    
    def to_html(self):
        """转换为HTML报告"""
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <meta charset='utf-8'>",
            "    <title>WCAG 2.2 验证报告</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
            "        h1 { color: #333; }",
            "        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }",
            "        .issue { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }",
            "        .issue h3 { margin-top: 0; }",
            "        .issue-A { border-left: 5px solid #e74c3c; }",
            "        .issue-AA { border-left: 5px solid #f39c12; }",
            "        .issue-AAA { border-left: 5px solid #3498db; }",
            "        .code { background: #f8f8f8; padding: 10px; border-radius: 3px; font-family: monospace; white-space: pre-wrap; }",
            "        .fix { background: #e8f8e8; padding: 10px; border-radius: 3px; margin-top: 10px; }",
            "    </style>",
            "</head>",
            "<body>",
            f"    <h1>WCAG 2.2 验证报告</h1>"
        ]
        
        if self.url:
            html.append(f"    <p>URL: {self.url}</p>")
        
        # 摘要
        html.extend([
            "    <div class='summary'>",
            "        <h2>摘要</h2>",
            f"        <p>发现 {self.summary['total_issues']} 个问题</p>",
            f"        <p>A级问题: {self.summary['level_A_issues']}</p>",
            f"        <p>AA级问题: {self.summary['level_AA_issues']}</p>",
            f"        <p>AAA级问题: {self.summary['level_AAA_issues']}</p>",
            f"        <p>通过规则: {self.summary['passed_rules']}</p>",
            f"        <p>失败规则: {self.summary['failed_rules']}</p>",
            "    </div>"
        ])
        
        # 问题列表
        if self.issues:
            html.append("    <h2>问题详情</h2>")
            
            for issue in self.issues:
                html.extend([
                    f"    <div class='issue issue-{issue.rule.level}'>",
                    f"        <h3>{issue.rule.name}</h3>",
                    f"        <p><strong>WCAG标准:</strong> {issue.rule.wcag_criterion} (级别 {issue.rule.level})</p>",
                    f"        <p><strong>问题描述:</strong> {issue.description}</p>"
                ])
                
                if issue.element_html:
                    html.append(f"        <div class='code'>{issue.element_html}</div>")
                
                if issue.location:
                    html.append(f"        <p><strong>位置:</strong> {issue.location}</p>")
                
                if issue.fix_suggestions:
                    html.append("        <div class='fix'>")
                    html.append("            <p><strong>修复建议:</strong></p>")
                    html.append("            <ul>")
                    for suggestion in issue.fix_suggestions:
                        html.append(f"                <li>{suggestion}</li>")
                    html.append("            </ul>")
                    html.append("        </div>")
                
                if issue.code_examples:
                    html.append("        <div class='fix'>")
                    html.append("            <p><strong>代码示例:</strong></p>")
                    for example in issue.code_examples:
                        html.append(f"            <div class='code'>{example['code']}</div>")
                        if example.get('description'):
                            html.append(f"            <p>{example['description']}</p>")
                    html.append("        </div>")
                
                html.append("    </div>")
        
        html.extend([
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html)
    
    def to_markdown(self):
        """转换为Markdown报告"""
        md = [
            "# WCAG 2.2 验证报告\n"
        ]
        
        if self.url:
            md.append(f"URL: {self.url}\n")
        
        # 摘要
        md.extend([
            "## 摘要\n",
            f"- 发现 {self.summary['total_issues']} 个问题",
            f"- A级问题: {self.summary['level_A_issues']}",
            f"- AA级问题: {self.summary['level_AA_issues']}",
            f"- AAA级问题: {self.summary['level_AAA_issues']}",
            f"- 通过规则: {self.summary['passed_rules']}",
            f"- 失败规则: {self.summary['failed_rules']}\n"
        ])
        
        # 问题列表
        if self.issues:
            md.append("## 问题详情\n")
            
            for issue in self.issues:
                md.extend([
                    f"### {issue.rule.name}\n",
                    f"- **WCAG标准:** {issue.rule.wcag_criterion} (级别 {issue.rule.level})",
                    f"- **问题描述:** {issue.description}\n"
                ])
                
                if issue.element_html:
                    md.append(f"```html\n{issue.element_html}\n```\n")
                
                if issue.location:
                    md.append(f"- **位置:** {issue.location}\n")
                
                if issue.fix_suggestions:
                    md.append("#### 修复建议:\n")
                    for suggestion in issue.fix_suggestions:
                        md.append(f"- {suggestion}")
                    md.append("")
                
                if issue.code_examples:
                    md.append("#### 代码示例:\n")
                    for example in issue.code_examples:
                        md.append(f"```html\n{example['code']}\n```")
                        if example.get('description'):
                            md.append(f"{example['description']}\n")
                
                md.append("")
        
        return "\n".join(md)
    
    def __str__(self):
        """转换为字符串"""
        lines = [
            "WCAG 2.2 验证报告",
            "=" * 20
        ]
        
        if self.url:
            lines.append(f"URL: {self.url}")
        
        lines.extend([
            "",
            "摘要:",
            f"- 发现 {self.summary['total_issues']} 个问题",
            f"- A级问题: {self.summary['level_A_issues']}",
            f"- AA级问题: {self.summary['level_AA_issues']}",
            f"- AAA级问题: {self.summary['level_AAA_issues']}",
            f"- 通过规则: {self.summary['passed_rules']}",
            f"- 失败规则: {self.summary['failed_rules']}",
            ""
        ])
        
        if self.issues:
            lines.append("问题详情:")
            lines.append("-" * 20)
            
            for i, issue in enumerate(self.issues, 1):
                lines.extend([
                    f"{i}. {issue.rule.name}",
                    f"   WCAG标准: {issue.rule.wcag_criterion} (级别 {issue.rule.level})",
                    f"   问题描述: {issue.description}"
                ])
                
                if issue.location:
                    lines.append(f"   位置: {issue.location}")
                
                if issue.fix_suggestions:
                    lines.append("   修复建议:")
                    for suggestion in issue.fix_suggestions:
                        lines.append(f"   - {suggestion}")
                
                lines.append("")
        
        return "\n".join(lines)


class Issue:
    """问题类"""
    
    def __init__(self, rule, element=None, description=""):
        self.rule = rule  # 触发问题的规则
        self.element = element  # 问题元素
        self.description = description  # 问题描述
        self.impact = "高"  # 影响程度
        self.fix_suggestions = []  # 修复建议
        self.code_examples = []  # 代码示例
        self.element_html = ""  # 元素HTML
        self.location = ""  # 元素位置
    
    def add_fix_suggestion(self, suggestion):
        """添加修复建议"""
        self.fix_suggestions.append(suggestion)
        return self
    
    def add_code_example(self, code, description=""):
        """添加代码示例"""
        self.code_examples.append({
            "code": code,
            "description": description
        })
        return self
    
    def set_element_html(self, html):
        """设置元素HTML"""
        self.element_html = html
        return self
    
    def set_location(self, location):
        """设置元素位置"""
        self.location = location
        return self
    
    def set_impact(self, impact):
        """设置影响程度"""
        self.impact = impact
        return self
    
    def to_dict(self):
        """转换为字典"""
        return {
            "rule_id": self.rule.id,
            "wcag_criterion": self.rule.wcag_criterion,
            "level": self.rule.level,
            "description": self.description,
            "impact": self.impact,
            "element_html": self.element_html,
            "location": self.location,
            "fix_suggestions": self.fix_suggestions,
            "code_examples": self.code_examples
        }


class WCAGValidator:
    """WCAG验证器主类"""
    
    def __init__(self, wcag_level='AA', rules=None):
        """
        初始化验证器
        
        参数:
            wcag_level: 验证级别 ('A', 'AA', 'AAA')
            rules: 要使用的规则列表，如果为None则使用默认规则
        """
        self.parser = HTMLParser()
        self.wcag_level = wcag_level
        
        # 获取规则
        if rules is None:
            self.rules = RuleRegistry.get_rules_by_level(wcag_level)
        else:
            self.rules = rules
    
    def validate_html(self, html_content, url=None):
        """
        验证HTML内容
        
        参数:
            html_content: HTML字符串
            url: 可选的URL，用于报告中
            
        返回:
            ValidationReport对象
        """
        # 解析HTML
        document = self.parser.parse_html(html_content, url)
        
        # 创建报告
        report = ValidationReport(url)
        
        # 应用规则
        for rule in self.rules:
            issues = rule.validate(document)
            
            if issues:
                # 处理每个问题
                for issue in issues:
                    # 如果元素存在，添加位置和HTML信息
                    if issue.element:
                        # 获取元素位置
                        line, column = self.parser.get_element_position(issue.element)
                        path = self.parser.get_element_path(issue.element)
                        issue.set_location(f"行 {line}, 列 {column}, 路径 {path}")
                        
                        # 获取元素HTML
                        html = self.parser.get_element_html(issue.element)
                        issue.set_element_html(html)
                    
                    # 添加修复建议
                    if not issue.fix_suggestions:
                        suggestions = rule.get_fix_suggestions(issue)
                        for suggestion in suggestions:
                            issue.add_fix_suggestion(suggestion)
                    
                    # 添加到报告
                    report.add_issue(issue)
            else:
                # 规则通过
                report.add_passed_rule(rule)
        
        return report
    
    def validate_file(self, file_path):
        """
        验证HTML文件
        
        参数:
            file_path: HTML文件路径
            
        返回:
            ValidationReport对象
        """
        # 解析文件
        document = self.parser.parse_file(file_path)
        
        # 验证
        return self.validate_html(self.parser.source_code, url=self.parser.url)
    
    def validate_url(self, url):
        """
        验证URL指向的网页
        
        参数:
            url: 网页URL
            
        返回:
            ValidationReport对象
        """
        # 解析URL
        document = self.parser.parse_url(url)
        
        # 验证
        return self.validate_html(self.parser.source_code, url=url)
