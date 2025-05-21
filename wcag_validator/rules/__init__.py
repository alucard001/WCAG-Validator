"""
规则模块初始化，负责导入和注册所有规则
"""

# 导入规则基类
from .base import Rule, RuleRegistry

# 导入所有规则模块
from .perceivable.images import ImageAltRule, ImageInputAltRule, SVGAccessibilityRule
from .perceivable.forms import FormLabelRule, FormFieldsetRule, FormAutocompleteRule
from .understandable.structure import HeadingStructureRule, PageTitleRule, LanguageRule
from .robust.structure import HTMLParsingRule, ARIARule, LinkPurposeRule

# 确保所有规则都已注册
__all__ = [
    'Rule',
    'RuleRegistry',
    'ImageAltRule',
    'ImageInputAltRule',
    'SVGAccessibilityRule',
    'FormLabelRule',
    'FormFieldsetRule',
    'FormAutocompleteRule',
    'HeadingStructureRule',
    'PageTitleRule',
    'LanguageRule',
    'HTMLParsingRule',
    'ARIARule',
    'LinkPurposeRule'
]
