"""
WCAG验证器使用说明文档 (Alpha)
"""

# WCAG Validator User Guide (Alpha)
This is an Alpha version of the WCAG Validator.  Please do not use it for production purposes at this moment.

# WCAG 2.2 验证库

这是一个用于验证HTML内容是否符合WCAG 2.2标准的Python库，可以自动检测常见的无障碍问题，并提供详细的错误报告、修复建议和代码示例。

## 功能特点

- 支持验证HTML字符串、文件和URL
- 实现多项WCAG 2.2标准的自动检测
- 提供详细的错误报告，包括问题描述、位置和代码片段
- 为每个问题提供修复建议和代码示例
- 支持多种报告格式：HTML、Markdown、JSON和控制台输出
- 模块化设计，易于扩展和定制

## 安装方法

```bash
# 克隆仓库
git clone https://github.com/yourusername/wcag-validator.git

# 进入目录
cd wcag-validator

# 安装依赖
pip install -r requirements.txt

# 安装库
pip install -e .
```

## 使用方法

### 基本用法

```python
from wcag_validator import validate_html, validate_file, validate_url, generate_report

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
report = validate_html(html, wcag_level='AA')

# 验证HTML文件
report = validate_file('path/to/file.html', wcag_level='AA')

# 验证URL
report = validate_url('https://example.com', wcag_level='AA')

# 生成HTML报告
html_report = generate_report(report, format='html')
with open('report.html', 'w', encoding='utf-8') as f:
    f.write(html_report)

# 生成Markdown报告
md_report = generate_report(report, format='markdown')
with open('report.md', 'w', encoding='utf-8') as f:
    f.write(md_report)

# 生成JSON报告
json_report = generate_report(report, format='json')
with open('report.json', 'w', encoding='utf-8') as f:
    f.write(json_report)

# 打印控制台报告
console_report = generate_report(report, format='console')
print(console_report)
```

### 命令行使用

```bash
python -m wcag_validator.cli path/to/file.html --level AA --format html --output report.html
```

## 支持的WCAG 2.2标准

该库支持检测以下WCAG 2.2标准：

### 可感知 (Perceivable)

- **1.1.1 非文本内容** - 检查图像是否有alt属性
- **1.3.1 信息和关系** - 检查表单标签、标题结构等
- **1.3.2 有意义的顺序** - 检查内容顺序是否合理
- **1.3.5 识别输入目的** - 检查表单字段是否使用autocomplete属性
- **1.4.1 颜色的使用** - 检查是否仅通过颜色传达信息
- **1.4.3 对比度（最小）** - 检查文本对比度

### 可操作 (Operable)

- **2.4.1 绕过内容块** - 检查是否提供跳过导航链接
- **2.4.2 页面标题** - 检查页面是否有描述性标题
- **2.4.4 链接目的** - 检查链接文本是否描述其目的
- **2.5.3 标签在名称中** - 检查可见标签是否包含在无障碍名称中

### 可理解 (Understandable)

- **3.1.1 页面语言** - 检查页面是否指定了语言
- **3.2.2 输入** - 检查输入时是否自动触发上下文变化
- **3.3.1 错误识别** - 检查表单是否提供错误识别
- **3.3.2 标签或说明** - 检查表单控件是否有标签或说明

### 健壮性 (Robust)

- **4.1.1 解析** - 检查HTML是否有良好的格式
- **4.1.2 名称、角色、值** - 检查ARIA属性是否正确使用
- **4.1.3 状态消息** - 检查状态消息是否可以通过辅助技术呈现

## 自定义规则

您可以通过继承`Rule`基类并实现`validate`方法来创建自定义规则：

```python
from wcag_validator.rules.base import Rule, RuleRegistry

@RuleRegistry.register
class MyCustomRule(Rule):
    def __init__(self):
        super().__init__()
        self.id = "my-custom-rule"
        self.name = "我的自定义规则"
        self.wcag_criterion = "1.1.1"
        self.level = "A"
        self.description = "自定义规则描述"

    def validate(self, document):
        from wcag_validator.core.validator import Issue

        issues = []
        # 实现验证逻辑
        # ...

        return issues
```

## 依赖项

- BeautifulSoup4：用于HTML解析
- Requests：用于URL请求
- HTML5Lib：用于HTML解析

## 许可证

MIT

## 贡献

欢迎提交问题和拉取请求！
