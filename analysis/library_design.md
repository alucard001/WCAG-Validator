# WCAG验证器库设计文档

## 1. 整体架构

WCAG验证器库将采用模块化、可扩展的架构设计，主要包含以下核心组件：

### 1.1 核心组件

1. **HTML解析器**：负责解析HTML文档，构建DOM树
2. **规则引擎**：管理和执行验证规则
3. **规则集合**：按WCAG标准分类的验证规则
4. **报告生成器**：生成详细的验证报告
5. **修复建议生成器**：为发现的问题提供修复建议和代码示例

### 1.2 模块划分

```
wcag_validator/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── parser.py          # HTML解析模块
│   ├── rule_engine.py     # 规则引擎
│   ├── validator.py       # 主验证器
│   └── report.py          # 报告生成
├── rules/
│   ├── __init__.py
│   ├── base.py            # 规则基类
│   ├── perceivable/       # 可感知原则规则
│   ├── operable/          # 可操作原则规则
│   ├── understandable/    # 可理解原则规则
│   └── robust/            # 健壮性原则规则
├── utils/
│   ├── __init__.py
│   ├── color.py           # 颜色对比度计算
│   ├── html_utils.py      # HTML辅助函数
│   └── aria.py            # ARIA属性验证
└── fixes/
    ├── __init__.py
    └── suggestions.py     # 修复建议生成
```

## 2. 核心类和接口设计

### 2.1 主验证器类

```python
class WCAGValidator:
    """WCAG验证器主类"""
    
    def __init__(self, wcag_level='AA', rules=None):
        """
        初始化验证器
        
        参数:
            wcag_level: 验证级别 ('A', 'AA', 'AAA')
            rules: 要使用的规则列表，如果为None则使用默认规则
        """
        pass
        
    def validate_html(self, html_content, url=None):
        """
        验证HTML内容
        
        参数:
            html_content: HTML字符串或文件路径
            url: 可选的URL，用于报告中
            
        返回:
            ValidationReport对象
        """
        pass
    
    def validate_file(self, file_path):
        """验证HTML文件"""
        pass
    
    def validate_url(self, url):
        """验证URL指向的网页"""
        pass
```

### 2.2 规则基类

```python
class Rule:
    """验证规则基类"""
    
    def __init__(self):
        self.id = None  # 规则ID
        self.name = None  # 规则名称
        self.wcag_criterion = None  # WCAG标准编号
        self.level = None  # 级别 (A, AA, AAA)
        self.description = None  # 规则描述
        
    def validate(self, document):
        """
        验证文档
        
        参数:
            document: 解析后的文档对象
            
        返回:
            RuleResult对象列表
        """
        raise NotImplementedError("子类必须实现validate方法")
    
    def get_help_text(self):
        """返回规则的帮助文本"""
        pass
    
    def get_fix_suggestions(self, issue):
        """
        获取修复建议
        
        参数:
            issue: 问题对象
            
        返回:
            修复建议列表
        """
        pass
```

### 2.3 验证结果类

```python
class ValidationReport:
    """验证报告类"""
    
    def __init__(self):
        self.issues = []  # 问题列表
        self.passed_rules = []  # 通过的规则
        self.failed_rules = []  # 失败的规则
        self.summary = {}  # 摘要信息
        
    def add_issue(self, issue):
        """添加问题"""
        pass
    
    def get_issues_by_criterion(self, criterion):
        """按WCAG标准获取问题"""
        pass
    
    def get_issues_by_level(self, level):
        """按级别获取问题"""
        pass
    
    def to_dict(self):
        """转换为字典"""
        pass
    
    def to_json(self):
        """转换为JSON"""
        pass
    
    def to_html(self):
        """转换为HTML报告"""
        pass
    
    def to_markdown(self):
        """转换为Markdown报告"""
        pass
```

### 2.4 问题类

```python
class Issue:
    """问题类"""
    
    def __init__(self, rule, element, description):
        self.rule = rule  # 触发问题的规则
        self.element = element  # 问题元素
        self.description = description  # 问题描述
        self.impact = None  # 影响程度
        self.fix_suggestions = []  # 修复建议
        self.code_examples = []  # 代码示例
        
    def add_fix_suggestion(self, suggestion):
        """添加修复建议"""
        pass
    
    def add_code_example(self, code, description):
        """添加代码示例"""
        pass
```

## 3. 验证规则实现方式

验证规则将采用插件式设计，每个规则作为独立模块，便于扩展和维护。

### 3.1 规则注册机制

```python
class RuleRegistry:
    """规则注册表"""
    
    _rules = {}
    
    @classmethod
    def register(cls, rule_class):
        """注册规则"""
        instance = rule_class()
        cls._rules[instance.id] = instance
        return rule_class
    
    @classmethod
    def get_rule(cls, rule_id):
        """获取规则"""
        return cls._rules.get(rule_id)
    
    @classmethod
    def get_rules_by_level(cls, level):
        """按级别获取规则"""
        return [rule for rule in cls._rules.values() if rule.level <= level]
    
    @classmethod
    def get_rules_by_criterion(cls, criterion):
        """按标准获取规则"""
        return [rule for rule in cls._rules.values() if rule.wcag_criterion == criterion]
```

### 3.2 规则示例

```python
@RuleRegistry.register
class ImageAltRule(Rule):
    """图像必须有alt属性"""
    
    def __init__(self):
        super().__init__()
        self.id = "img-alt"
        self.name = "图像必须有alt属性"
        self.wcag_criterion = "1.1.1"
        self.level = "A"
        self.description = "所有非装饰性图像必须有描述性的alt属性"
    
    def validate(self, document):
        issues = []
        for img in document.find_all("img"):
            if not img.has_attr("alt") or img["alt"].strip() == "":
                # 检查是否为装饰性图像
                if not (img.has_attr("role") and img["role"] == "presentation"):
                    issue = Issue(
                        rule=self,
                        element=img,
                        description="图像缺少alt属性"
                    )
                    issue.add_fix_suggestion(
                        "添加描述性的alt属性，说明图像内容和目的"
                    )
                    issue.add_code_example(
                        f'<img src="{img.get("src", "")}" alt="[图像描述]">',
                        "添加描述性alt属性的示例"
                    )
                    issues.append(issue)
        return issues
```

## 4. 错误报告格式和内容

错误报告将包含以下内容：

1. **摘要信息**：
   - 总问题数
   - 按WCAG级别分类的问题数
   - 按WCAG标准分类的问题数
   - 通过和失败的规则数

2. **详细问题列表**：
   - 问题描述
   - 相关WCAG标准
   - 问题位置（元素路径、行号）
   - 问题代码片段
   - 影响程度

3. **修复建议**：
   - 问题修复方法说明
   - 修复后的代码示例
   - 最佳实践建议

4. **输出格式**：
   - JSON（用于程序处理）
   - HTML（用于可视化展示）
   - Markdown（用于文档集成）
   - 控制台输出（用于命令行使用）

### 4.1 报告示例（JSON格式）

```json
{
  "summary": {
    "total_issues": 5,
    "level_A_issues": 3,
    "level_AA_issues": 2,
    "level_AAA_issues": 0,
    "passed_rules": 15,
    "failed_rules": 4
  },
  "issues": [
    {
      "rule_id": "img-alt",
      "wcag_criterion": "1.1.1",
      "level": "A",
      "element": "img",
      "location": {
        "path": "/html/body/main/img[1]",
        "line": 24,
        "column": 5
      },
      "html": "<img src=\"logo.png\">",
      "description": "图像缺少alt属性",
      "impact": "高",
      "fix_suggestions": [
        "添加描述性的alt属性，说明图像内容和目的"
      ],
      "code_examples": [
        {
          "code": "<img src=\"logo.png\" alt=\"公司标志\">",
          "description": "添加描述性alt属性的示例"
        }
      ]
    }
  ]
}
```

## 5. 使用示例

### 5.1 基本使用

```python
from wcag_validator import WCAGValidator

# 创建验证器实例
validator = WCAGValidator(wcag_level='AA')

# 验证HTML字符串
html = """
<!DOCTYPE html>
<html>
<head>
    <title>测试页面</title>
</head>
<body>
    <img src="logo.png">
    <a href="#">点击这里</a>
</body>
</html>
"""
report = validator.validate_html(html)

# 输出报告
print(f"发现 {len(report.issues)} 个问题")
for issue in report.issues:
    print(f"- {issue.description}")
    print(f"  修复建议: {issue.fix_suggestions[0]}")
    print(f"  代码示例: {issue.code_examples[0]['code']}")

# 保存HTML报告
with open("report.html", "w") as f:
    f.write(report.to_html())
```

### 5.2 命令行接口

```python
import argparse
from wcag_validator import WCAGValidator

def main():
    parser = argparse.ArgumentParser(description='WCAG 2.2 验证工具')
    parser.add_argument('source', help='HTML文件路径或URL')
    parser.add_argument('--level', choices=['A', 'AA', 'AAA'], default='AA',
                        help='WCAG合规级别 (默认: AA)')
    parser.add_argument('--format', choices=['json', 'html', 'markdown', 'text'],
                        default='text', help='输出格式 (默认: text)')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    validator = WCAGValidator(wcag_level=args.level)
    
    # 判断输入是文件还是URL
    if args.source.startswith(('http://', 'https://')):
        report = validator.validate_url(args.source)
    else:
        report = validator.validate_file(args.source)
    
    # 生成报告
    if args.format == 'json':
        output = report.to_json()
    elif args.format == 'html':
        output = report.to_html()
    elif args.format == 'markdown':
        output = report.to_markdown()
    else:  # text
        output = str(report)
    
    # 输出报告
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        print(output)

if __name__ == '__main__':
    main()
```

## 6. 扩展性考虑

1. **自定义规则**：用户可以创建和注册自定义规则
2. **规则过滤**：可以选择性启用或禁用特定规则
3. **集成API**：提供API接口，便于与其他工具集成
4. **插件系统**：支持第三方插件扩展功能
5. **国际化**：支持多语言报告和错误消息

## 7. 性能优化

1. **增量验证**：支持只验证变更部分
2. **并行处理**：使用多线程处理大型文档
3. **缓存机制**：缓存解析结果，避免重复解析
4. **懒加载规则**：按需加载规则，减少内存占用
