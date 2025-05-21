"""
HTML结构和ARIA规则模块，实现与HTML结构和ARIA相关的WCAG验证规则
"""
from ...rules.base import Rule, RuleRegistry
from bs4 import BeautifulSoup

@RuleRegistry.register
class HTMLParsingRule(Rule):
    """HTML必须可以正确解析"""
    
    def __init__(self):
        super().__init__()
        self.id = "html-parsing"
        self.name = "HTML必须可以正确解析"
        self.wcag_criterion = "4.1.1"
        self.level = "A"
        self.description = "HTML必须有良好的格式，元素必须有完整的开始和结束标签，元素必须嵌套正确"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        # 由于BeautifulSoup会自动修复HTML，所以这里主要检查一些常见的问题
        
        # 检查是否有重复的id
        ids = {}
        for element in document.find_all(attrs={"id": True}):
            element_id = element["id"]
            if element_id in ids:
                issue = Issue(
                    rule=self,
                    element=element,
                    description=f"重复的id属性: '{element_id}'已在其他元素中使用"
                )
                issue.add_fix_suggestion(f"修改id属性为唯一值")
                
                # 修复f-string语法
                attrs_str = " ".join([f"{k}=\"{v}\"" for k, v in element.attrs.items() if k != "id"])
                if element.name not in ['img', 'input', 'br', 'hr']:
                    code_example = f'<{element.name} id="unique-{element_id}" {attrs_str}></{element.name}>'
                else:
                    code_example = f'<{element.name} id="unique-{element_id}" {attrs_str}>'
                
                issue.add_code_example(code_example)
                issues.append(issue)
            else:
                ids[element_id] = element
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "重复的id属性" in issue.description:
            return [
                "修改id属性为唯一值",
                "确保页面中每个id都是唯一的"
            ]
        
        return []


@RuleRegistry.register
class ARIARule(Rule):
    """ARIA属性必须正确使用"""
    
    def __init__(self):
        super().__init__()
        self.id = "aria-usage"
        self.name = "ARIA属性必须正确使用"
        self.wcag_criterion = "4.1.2"
        self.level = "A"
        self.description = "ARIA属性必须正确使用，确保无障碍名称、角色和值可以被辅助技术识别"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        
        # 检查aria-hidden="true"的元素是否包含交互元素
        for element in document.find_all(attrs={"aria-hidden": "true"}):
            interactive_elements = element.find_all(['a', 'button', 'input', 'select', 'textarea'])
            if interactive_elements:
                issue = Issue(
                    rule=self,
                    element=element,
                    description="aria-hidden=\"true\"的元素包含交互元素，这会使交互元素对辅助技术不可见"
                )
                issue.add_fix_suggestion("移除aria-hidden=\"true\"属性")
                issue.add_fix_suggestion("或将交互元素移出aria-hidden=\"true\"的容器")
                
                # 生成修复示例
                element_html = str(element)
                fixed_html = element_html.replace('aria-hidden="true"', '')
                issue.add_code_example(
                    fixed_html,
                    "移除aria-hidden=\"true\"属性"
                )
                issues.append(issue)
        
        # 检查aria-label为空的元素
        for element in document.find_all(attrs={"aria-label": True}):
            if not element["aria-label"].strip():
                issue = Issue(
                    rule=self,
                    element=element,
                    description="元素的aria-label属性为空"
                )
                issue.add_fix_suggestion("为aria-label添加描述性文本")
                issue.add_fix_suggestion("或移除空的aria-label属性")
                
                # 生成修复示例 - 修复f-string语法
                attrs_str = " ".join([f"{k}=\"{v}\"" for k, v in element.attrs.items() if k != "aria-label"])
                if element.name not in ['img', 'input', 'br', 'hr']:
                    code_example = f'<{element.name} {attrs_str} aria-label="描述性文本"></{element.name}>'
                else:
                    code_example = f'<{element.name} {attrs_str} aria-label="描述性文本">'
                
                issue.add_code_example(code_example)
                issues.append(issue)
        
        # 检查aria-labelledby引用的元素是否存在
        for element in document.find_all(attrs={"aria-labelledby": True}):
            referenced_ids = element["aria-labelledby"].split()
            for ref_id in referenced_ids:
                if not document.find(id=ref_id):
                    issue = Issue(
                        rule=self,
                        element=element,
                        description=f"aria-labelledby引用的id '{ref_id}'不存在"
                    )
                    issue.add_fix_suggestion(f"确保id为'{ref_id}'的元素存在")
                    issue.add_fix_suggestion("或修改aria-labelledby属性引用正确的id")
                    
                    # 生成修复示例
                    issue.add_code_example(
                        f'<div id="{ref_id}">标签文本</div>',
                        f"添加id为'{ref_id}'的元素"
                    )
                    issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "aria-hidden=\"true\"的元素包含交互元素" in issue.description:
            return [
                "移除aria-hidden=\"true\"属性",
                "或将交互元素移出aria-hidden=\"true\"的容器"
            ]
        elif "元素的aria-label属性为空" in issue.description:
            return [
                "为aria-label添加描述性文本",
                "或移除空的aria-label属性"
            ]
        elif "aria-labelledby引用的id" in issue.description and "不存在" in issue.description:
            ref_id = issue.description.split("'")[1]
            return [
                f"确保id为'{ref_id}'的元素存在",
                "或修改aria-labelledby属性引用正确的id"
            ]
        
        return []


@RuleRegistry.register
class LinkPurposeRule(Rule):
    """链接文本必须描述其目的"""
    
    def __init__(self):
        super().__init__()
        self.id = "link-purpose"
        self.name = "链接文本必须描述其目的"
        self.wcag_criterion = "2.4.4"
        self.level = "A"
        self.description = "链接文本必须描述其目的，使用户能够确定是否要跟随链接"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        
        # 检查所有链接
        for link in document.find_all('a'):
            # 获取链接文本
            link_text = link.get_text().strip()
            
            # 检查是否有文本内容
            if not link_text:
                # 检查是否有图像并且图像有alt属性
                img = link.find('img')
                if img and img.has_attr('alt') and img['alt'].strip():
                    continue  # 图像有alt属性，链接有描述
                
                # 检查是否有aria-label或title属性
                if (link.has_attr('aria-label') and link['aria-label'].strip()) or \
                   (link.has_attr('title') and link['title'].strip()):
                    continue  # 有aria-label或title属性，链接有描述
                
                issue = Issue(
                    rule=self,
                    element=link,
                    description="链接没有描述性文本"
                )
                issue.add_fix_suggestion("添加描述链接目的的文本")
                issue.add_fix_suggestion("或为链接添加aria-label属性")
                
                # 生成修复示例
                href = link.get('href', '#')
                issue.add_code_example(
                    f'<a href="{href}">描述性链接文本</a>',
                    "添加描述性链接文本"
                )
                
                # 修复f-string语法
                link_content = str(link.contents[0]) if link.contents else ""
                issue.add_code_example(
                    f'<a href="{href}" aria-label="描述性链接文本">{link_content}</a>',
                    "添加aria-label属性"
                )
                issues.append(issue)
            elif link_text.lower() in ['点击这里', '点击', '这里', 'click here', 'click', 'here', 'more', '更多']:
                # 链接文本不描述目的
                issue = Issue(
                    rule=self,
                    element=link,
                    description=f"链接文本 '{link_text}' 不足以描述链接目的"
                )
                issue.add_fix_suggestion("使用描述链接目的的文本替换通用文本")
                
                # 生成修复示例
                href = link.get('href', '#')
                issue.add_code_example(
                    f'<a href="{href}">描述性链接文本</a>',
                    "使用描述性链接文本"
                )
                issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "链接没有描述性文本" in issue.description:
            return [
                "添加描述链接目的的文本",
                "或为链接添加aria-label属性"
            ]
        elif "不足以描述链接目的" in issue.description:
            return [
                "使用描述链接目的的文本替换通用文本",
                "确保链接文本能够独立理解，不依赖上下文"
            ]
        
        return []
