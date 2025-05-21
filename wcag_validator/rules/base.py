"""
规则基类，定义验证规则的基本接口和功能
"""

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
        return self.description
    
    def get_fix_suggestions(self, issue):
        """
        获取修复建议
        
        参数:
            issue: 问题对象
            
        返回:
            修复建议列表
        """
        return []
    
    def get_wcag_reference(self):
        """返回WCAG参考链接"""
        if not self.wcag_criterion:
            return ""
        
        # 提取主要部分，如1.1.1
        parts = self.wcag_criterion.split('.')
        if len(parts) >= 3:
            principle, guideline, criterion = parts[:3]
            return f"https://www.w3.org/WAI/WCAG22/Understanding/{principle}-{guideline}-{criterion}.html"
        
        return ""


class RuleRegistry:
    """规则注册表"""
    
    _rules = {}
    
    @classmethod
    def register(cls, rule_class):
        """
        注册规则
        
        参数:
            rule_class: 规则类
            
        返回:
            规则类（用于装饰器模式）
        """
        instance = rule_class()
        cls._rules[instance.id] = instance
        return rule_class
    
    @classmethod
    def get_rule(cls, rule_id):
        """
        获取规则
        
        参数:
            rule_id: 规则ID
            
        返回:
            规则实例
        """
        return cls._rules.get(rule_id)
    
    @classmethod
    def get_all_rules(cls):
        """
        获取所有规则
        
        返回:
            规则实例列表
        """
        return list(cls._rules.values())
    
    @classmethod
    def get_rules_by_level(cls, level):
        """
        按级别获取规则
        
        参数:
            level: WCAG级别 ('A', 'AA', 'AAA')
            
        返回:
            规则实例列表
        """
        level_map = {'A': 1, 'AA': 2, 'AAA': 3}
        target_level = level_map.get(level.upper(), 3)
        
        return [
            rule for rule in cls._rules.values() 
            if level_map.get(rule.level, 0) <= target_level
        ]
    
    @classmethod
    def get_rules_by_criterion(cls, criterion):
        """
        按标准获取规则
        
        参数:
            criterion: WCAG标准编号
            
        返回:
            规则实例列表
        """
        return [
            rule for rule in cls._rules.values() 
            if rule.wcag_criterion == criterion
        ]
