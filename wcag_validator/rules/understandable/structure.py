"""
标题和结构规则模块，实现与页面结构相关的WCAG验证规则
"""
from ...rules.base import Rule, RuleRegistry
from bs4 import BeautifulSoup

@RuleRegistry.register
class HeadingStructureRule(Rule):
    """标题层次结构必须正确"""
    
    def __init__(self):
        super().__init__()
        self.id = "heading-structure"
        self.name = "标题层次结构必须正确"
        self.wcag_criterion = "1.3.1"
        self.level = "A"
        self.description = "标题层次结构必须正确，不应跳过级别"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        headings = document.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headings:
            # 页面没有标题
            issue = Issue(
                rule=self,
                element=document.find('body'),
                description="页面没有标题元素"
            )
            issue.add_fix_suggestion("添加适当的标题元素，如h1作为主标题")
            issue.add_code_example(
                "<h1>页面主标题</h1>",
                "添加主标题"
            )
            issues.append(issue)
            return issues
        
        # 检查是否有h1
        if not document.find('h1'):
            issue = Issue(
                rule=self,
                element=headings[0],
                description="页面缺少h1主标题"
            )
            issue.add_fix_suggestion("添加h1作为页面主标题")
            issue.add_code_example(
                "<h1>页面主标题</h1>",
                "添加主标题"
            )
            issues.append(issue)
        
        # 检查标题层次是否正确
        current_level = 0
        for heading in headings:
            level = int(heading.name[1])
            
            # 检查是否跳过级别
            if level > current_level + 1 and current_level > 0:
                issue = Issue(
                    rule=self,
                    element=heading,
                    description=f"标题层次结构不正确：从h{current_level}跳到h{level}"
                )
                issue.add_fix_suggestion(f"添加h{current_level + 1}作为中间层次")
                issue.add_fix_suggestion(f"或将当前h{level}改为h{current_level + 1}")
                
                # 生成修复示例
                issue.add_code_example(
                    f"<h{current_level + 1}>中间层次标题</h{current_level + 1}>\n{str(heading)}",
                    "添加中间层次标题"
                )
                issue.add_code_example(
                    f"<h{current_level + 1}>{heading.get_text()}</h{current_level + 1}>",
                    f"将h{level}改为h{current_level + 1}"
                )
                issues.append(issue)
            
            current_level = level
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "页面没有标题元素" in issue.description:
            return ["添加适当的标题元素，如h1作为主标题"]
        elif "页面缺少h1主标题" in issue.description:
            return ["添加h1作为页面主标题"]
        elif "标题层次结构不正确" in issue.description:
            levels = issue.description.split("从h")[1].split("跳到h")
            current_level = int(levels[0])
            target_level = int(levels[1])
            return [
                f"添加h{current_level + 1}作为中间层次",
                f"或将当前h{target_level}改为h{current_level + 1}"
            ]
        
        return []


@RuleRegistry.register
class PageTitleRule(Rule):
    """页面必须有描述性标题"""
    
    def __init__(self):
        super().__init__()
        self.id = "page-title"
        self.name = "页面必须有描述性标题"
        self.wcag_criterion = "2.4.2"
        self.level = "A"
        self.description = "页面必须有描述其内容或目的的title元素"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        title = document.find('title')
        
        if not title:
            # 页面没有title元素
            issue = Issue(
                rule=self,
                element=document.find('head'),
                description="页面缺少title元素"
            )
            issue.add_fix_suggestion("添加描述页面内容或目的的title元素")
            issue.add_code_example(
                "<title>页面标题 - 网站名称</title>",
                "添加描述性title元素"
            )
            issues.append(issue)
        elif not title.text.strip():
            # title元素为空
            issue = Issue(
                rule=self,
                element=title,
                description="页面的title元素为空"
            )
            issue.add_fix_suggestion("为title元素添加描述性文本")
            issue.add_code_example(
                "<title>页面标题 - 网站名称</title>",
                "添加描述性title文本"
            )
            issues.append(issue)
        elif len(title.text.strip()) < 5:
            # title元素过短
            issue = Issue(
                rule=self,
                element=title,
                description="页面的title元素过短，可能不足以描述页面内容"
            )
            issue.add_fix_suggestion("为title元素添加更详细的描述性文本")
            issue.add_code_example(
                "<title>详细的页面标题 - 网站名称</title>",
                "添加更详细的title文本"
            )
            issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "缺少title元素" in issue.description:
            return ["添加描述页面内容或目的的title元素"]
        elif "title元素为空" in issue.description:
            return ["为title元素添加描述性文本"]
        elif "title元素过短" in issue.description:
            return ["为title元素添加更详细的描述性文本"]
        
        return []


@RuleRegistry.register
class LanguageRule(Rule):
    """页面必须指定语言"""
    
    def __init__(self):
        super().__init__()
        self.id = "page-language"
        self.name = "页面必须指定语言"
        self.wcag_criterion = "3.1.1"
        self.level = "A"
        self.description = "页面必须通过html元素的lang属性指定默认语言"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        html = document.find('html')
        
        if not html:
            return issues
        
        if not html.has_attr('lang') or not html['lang'].strip():
            # 页面没有指定语言
            issue = Issue(
                rule=self,
                element=html,
                description="页面没有通过html元素的lang属性指定默认语言"
            )
            issue.add_fix_suggestion("为html元素添加lang属性，指定页面的默认语言")
            issue.add_code_example(
                '<html lang="zh-CN">',
                "指定简体中文"
            )
            issue.add_code_example(
                '<html lang="en">',
                "指定英文"
            )
            issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        return [
            "为html元素添加lang属性，指定页面的默认语言",
            "常见语言代码：zh-CN（简体中文）、zh-TW（繁体中文）、en（英文）、ja（日文）、ko（韩文）"
        ]
