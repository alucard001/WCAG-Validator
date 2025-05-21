"""
图像无障碍规则模块，实现与图像相关的WCAG验证规则
"""
from ...rules.base import Rule, RuleRegistry
from bs4 import BeautifulSoup

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
        from ...core.validator import Issue
        
        issues = []
        for img in document.find_all("img"):
            # 检查是否为装饰性图像
            is_decorative = (
                (img.has_attr("role") and img["role"] == "presentation") or
                (img.has_attr("aria-hidden") and img["aria-hidden"] == "true")
            )
            
            # 检查alt属性
            if not is_decorative:
                if not img.has_attr("alt"):
                    # 缺少alt属性
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
                elif img["alt"].strip() == "":
                    # alt属性为空
                    issue = Issue(
                        rule=self,
                        element=img,
                        description="图像的alt属性为空"
                    )
                    issue.add_fix_suggestion(
                        "如果图像是装饰性的，请添加role=\"presentation\"属性"
                    )
                    issue.add_fix_suggestion(
                        "如果图像包含信息，请添加描述性的alt属性"
                    )
                    issue.add_code_example(
                        f'<img src="{img.get("src", "")}" alt="[图像描述]">',
                        "信息性图像示例"
                    )
                    issue.add_code_example(
                        f'<img src="{img.get("src", "")}" alt="" role="presentation">',
                        "装饰性图像示例"
                    )
                    issues.append(issue)
                elif len(img["alt"]) > 100:
                    # alt属性过长
                    issue = Issue(
                        rule=self,
                        element=img,
                        description="图像的alt属性过长（超过100个字符）"
                    )
                    issue.add_fix_suggestion(
                        "缩短alt属性，保持简洁但描述准确"
                    )
                    issue.add_fix_suggestion(
                        "如果需要更详细的描述，考虑使用longdesc属性或在图像附近提供描述"
                    )
                    issue.add_code_example(
                        f'<img src="{img.get("src", "")}" alt="[简短描述]">',
                        "简短alt属性示例"
                    )
                    issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "缺少alt属性" in issue.description:
            return [
                "添加描述性的alt属性，说明图像内容和目的",
                "如果图像是装饰性的，添加alt=\"\"和role=\"presentation\"属性"
            ]
        elif "alt属性为空" in issue.description:
            return [
                "如果图像是装饰性的，请添加role=\"presentation\"属性",
                "如果图像包含信息，请添加描述性的alt属性"
            ]
        elif "alt属性过长" in issue.description:
            return [
                "缩短alt属性，保持简洁但描述准确",
                "如果需要更详细的描述，考虑使用longdesc属性或在图像附近提供描述"
            ]
        
        return []


@RuleRegistry.register
class ImageInputAltRule(Rule):
    """图像按钮必须有alt属性"""
    
    def __init__(self):
        super().__init__()
        self.id = "img-input-alt"
        self.name = "图像按钮必须有alt属性"
        self.wcag_criterion = "1.1.1"
        self.level = "A"
        self.description = "所有图像按钮必须有描述其功能的alt属性"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        for input_elem in document.find_all("input"):
            if input_elem.has_attr("type") and input_elem["type"] == "image":
                if not input_elem.has_attr("alt") or input_elem["alt"].strip() == "":
                    issue = Issue(
                        rule=self,
                        element=input_elem,
                        description="图像按钮缺少alt属性"
                    )
                    issue.add_fix_suggestion(
                        "添加描述按钮功能的alt属性"
                    )
                    issue.add_code_example(
                        f'<input type="image" src="{input_elem.get("src", "")}" alt="[按钮功能描述]">',
                        "添加描述性alt属性的示例"
                    )
                    issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        return [
            "添加描述按钮功能的alt属性",
            "确保alt属性描述的是按钮的功能，而不仅仅是图像内容"
        ]


@RuleRegistry.register
class SVGAccessibilityRule(Rule):
    """SVG图像必须具有无障碍特性"""
    
    def __init__(self):
        super().__init__()
        self.id = "svg-accessibility"
        self.name = "SVG图像必须具有无障碍特性"
        self.wcag_criterion = "1.1.1"
        self.level = "A"
        self.description = "SVG图像必须包含title元素或aria-label属性"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        for svg in document.find_all("svg"):
            # 检查是否为装饰性SVG
            is_decorative = (
                (svg.has_attr("role") and svg["role"] == "presentation") or
                (svg.has_attr("aria-hidden") and svg["aria-hidden"] == "true")
            )
            
            if not is_decorative:
                has_title = svg.find("title") is not None
                has_aria_label = svg.has_attr("aria-label") and svg["aria-label"].strip() != ""
                has_aria_labelledby = svg.has_attr("aria-labelledby") and svg["aria-labelledby"].strip() != ""
                
                if not (has_title or has_aria_label or has_aria_labelledby):
                    issue = Issue(
                        rule=self,
                        element=svg,
                        description="SVG图像缺少无障碍名称"
                    )
                    issue.add_fix_suggestion(
                        "添加<title>元素描述SVG内容"
                    )
                    issue.add_fix_suggestion(
                        "添加aria-label属性描述SVG内容"
                    )
                    issue.add_code_example(
                        f'<svg width="{svg.get("width", "100")}" height="{svg.get("height", "100")}">\n  <title>SVG图像描述</title>\n  <!-- SVG内容 -->\n</svg>',
                        "使用title元素的示例"
                    )
                    issue.add_code_example(
                        f'<svg width="{svg.get("width", "100")}" height="{svg.get("height", "100")}" aria-label="SVG图像描述">\n  <!-- SVG内容 -->\n</svg>',
                        "使用aria-label的示例"
                    )
                    issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        return [
            "添加<title>元素描述SVG内容",
            "添加aria-label属性描述SVG内容",
            "如果SVG是装饰性的，添加role=\"presentation\"和aria-hidden=\"true\"属性"
        ]
