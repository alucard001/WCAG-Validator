"""
表单无障碍规则模块，实现与表单相关的WCAG验证规则
"""
from ...rules.base import Rule, RuleRegistry
from bs4 import BeautifulSoup

@RuleRegistry.register
class FormLabelRule(Rule):
    """表单控件必须有关联的标签"""
    
    def __init__(self):
        super().__init__()
        self.id = "form-label"
        self.name = "表单控件必须有关联的标签"
        self.wcag_criterion = "1.3.1"
        self.level = "A"
        self.description = "所有表单控件必须有明确关联的标签，以便辅助技术识别"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        # 需要检查的表单控件类型
        input_types = ['text', 'password', 'checkbox', 'radio', 'file', 'email', 
                      'tel', 'number', 'search', 'url', 'date', 'time', 'datetime-local']
        
        # 检查所有表单控件
        for control in document.find_all(['input', 'select', 'textarea']):
            # 跳过隐藏字段和提交按钮
            if control.name == 'input' and control.has_attr('type'):
                if control['type'] in ['hidden', 'submit', 'button', 'reset', 'image']:
                    continue
            
            # 检查是否有id属性
            if not control.has_attr('id') or not control['id'].strip():
                issue = Issue(
                    rule=self,
                    element=control,
                    description="表单控件缺少id属性，无法与标签关联"
                )
                issue.add_fix_suggestion("添加唯一的id属性")
                
                # 生成修复示例 - 修复f-string语法
                attrs_str = " ".join([f"{k}=\"{v}\"" for k, v in control.attrs.items() if k != "id"])
                if control.name != 'input':
                    code_example = f'<{control.name} id="unique-id" {attrs_str}></{control.name}>'
                else:
                    code_example = f'<input id="unique-id" {attrs_str}>'
                
                issue.add_code_example(code_example)
                issues.append(issue)
                continue
            
            # 检查是否有关联的标签
            control_id = control['id']
            label = document.find('label', attrs={'for': control_id})
            
            if not label:
                # 检查是否在标签内部
                parent_label = control.find_parent('label')
                if not parent_label:
                    issue = Issue(
                        rule=self,
                        element=control,
                        description=f"表单控件 (id=\"{control_id}\") 没有关联的标签"
                    )
                    issue.add_fix_suggestion("添加for属性与控件id匹配的label元素")
                    issue.add_fix_suggestion("或将控件放在label元素内")
                    
                    # 生成修复示例
                    control_html = str(control)
                    issue.add_code_example(
                        f'<label for="{control_id}">标签文本</label>\n{control_html}',
                        "使用for属性关联标签"
                    )
                    issue.add_code_example(
                        f'<label>\n  标签文本\n  {control_html}\n</label>',
                        "将控件放在标签内"
                    )
                    issues.append(issue)
            elif not label.text.strip():
                # 标签存在但没有文本
                issue = Issue(
                    rule=self,
                    element=label,
                    description=f"与表单控件关联的标签 (for=\"{control_id}\") 没有文本内容"
                )
                issue.add_fix_suggestion("为标签添加描述性文本")
                issue.add_code_example(
                    f'<label for="{control_id}">描述性标签文本</label>',
                    "添加描述性标签文本"
                )
                issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "缺少id属性" in issue.description:
            return ["添加唯一的id属性，确保页面中没有重复的id"]
        elif "没有关联的标签" in issue.description:
            return [
                "添加for属性与控件id匹配的label元素",
                "或将控件放在label元素内"
            ]
        elif "没有文本内容" in issue.description:
            return ["为标签添加描述性文本，清晰说明控件的用途"]
        
        return []


@RuleRegistry.register
class FormFieldsetRule(Rule):
    """相关表单控件应使用fieldset分组"""
    
    def __init__(self):
        super().__init__()
        self.id = "form-fieldset"
        self.name = "相关表单控件应使用fieldset分组"
        self.wcag_criterion = "1.3.1"
        self.level = "A"
        self.description = "相关的表单控件（如单选按钮组）应使用fieldset和legend元素分组"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        
        # 查找所有单选按钮组
        radio_groups = {}
        for radio in document.find_all('input', type='radio'):
            if radio.has_attr('name') and radio['name'].strip():
                group_name = radio['name']
                if group_name not in radio_groups:
                    radio_groups[group_name] = []
                radio_groups[group_name].append(radio)
        
        # 检查每个单选按钮组
        for group_name, radios in radio_groups.items():
            if len(radios) < 2:
                continue  # 单个单选按钮不需要fieldset
            
            # 检查是否在fieldset内
            in_fieldset = False
            for radio in radios:
                if radio.find_parent('fieldset'):
                    in_fieldset = True
                    break
            
            if not in_fieldset:
                # 获取组中第一个单选按钮作为参考
                first_radio = radios[0]
                issue = Issue(
                    rule=self,
                    element=first_radio,
                    description=f"单选按钮组 (name=\"{group_name}\") 没有使用fieldset和legend元素分组"
                )
                issue.add_fix_suggestion("使用fieldset元素包围单选按钮组")
                issue.add_fix_suggestion("添加legend元素描述单选按钮组的用途")
                
                # 生成修复示例
                radio_html_parts = []
                for radio in radios:
                    if radio.has_attr('id'):
                        radio_html_parts.append(str(radio) + " <label for=\"" + radio.get('id', '') + "\">选项文本</label>")
                
                radio_html = "\n  ".join(radio_html_parts)
                issue.add_code_example(
                    f'<fieldset>\n  <legend>{group_name}选项</legend>\n  {radio_html}\n</fieldset>',
                    "使用fieldset和legend分组单选按钮"
                )
                issues.append(issue)
        
        # 检查checkbox组（相同name属性的复选框）
        checkbox_groups = {}
        for checkbox in document.find_all('input', type='checkbox'):
            if checkbox.has_attr('name') and checkbox['name'].strip():
                group_name = checkbox['name']
                if group_name.endswith('[]'):  # 常见的PHP风格数组表示
                    group_name = group_name[:-2]
                if group_name not in checkbox_groups:
                    checkbox_groups[group_name] = []
                checkbox_groups[group_name].append(checkbox)
        
        # 检查每个复选框组
        for group_name, checkboxes in checkbox_groups.items():
            if len(checkboxes) < 2:
                continue  # 单个复选框不需要fieldset
            
            # 检查是否在fieldset内
            in_fieldset = False
            for checkbox in checkboxes:
                if checkbox.find_parent('fieldset'):
                    in_fieldset = True
                    break
            
            if not in_fieldset:
                # 获取组中第一个复选框作为参考
                first_checkbox = checkboxes[0]
                issue = Issue(
                    rule=self,
                    element=first_checkbox,
                    description=f"复选框组 (name=\"{group_name}\") 没有使用fieldset和legend元素分组"
                )
                issue.add_fix_suggestion("使用fieldset元素包围复选框组")
                issue.add_fix_suggestion("添加legend元素描述复选框组的用途")
                
                # 生成修复示例
                checkbox_html_parts = []
                for checkbox in checkboxes:
                    if checkbox.has_attr('id'):
                        checkbox_html_parts.append(str(checkbox) + " <label for=\"" + checkbox.get('id', '') + "\">选项文本</label>")
                
                checkbox_html = "\n  ".join(checkbox_html_parts)
                issue.add_code_example(
                    f'<fieldset>\n  <legend>{group_name}选项</legend>\n  {checkbox_html}\n</fieldset>',
                    "使用fieldset和legend分组复选框"
                )
                issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "单选按钮组" in issue.description:
            return [
                "使用fieldset元素包围单选按钮组",
                "添加legend元素描述单选按钮组的用途"
            ]
        elif "复选框组" in issue.description:
            return [
                "使用fieldset元素包围复选框组",
                "添加legend元素描述复选框组的用途"
            ]
        
        return []


@RuleRegistry.register
class FormAutocompleteRule(Rule):
    """输入字段应使用适当的autocomplete属性"""
    
    def __init__(self):
        super().__init__()
        self.id = "form-autocomplete"
        self.name = "输入字段应使用适当的autocomplete属性"
        self.wcag_criterion = "1.3.5"
        self.level = "AA"
        self.description = "收集用户信息的输入字段应使用适当的autocomplete属性"
    
    def validate(self, document):
        from ...core.validator import Issue
        
        issues = []
        
        # 常见的输入字段类型和对应的autocomplete值
        common_fields = {
            'name': ['name', 'fname', 'lname', 'fullname', 'first-name', 'last-name', 'full-name'],
            'email': ['email'],
            'tel': ['tel', 'phone', 'telephone', 'mobile'],
            'address': ['address', 'street', 'city', 'state', 'province', 'zip', 'postal', 'country'],
            'username': ['username', 'user', 'login'],
            'password': ['password', 'pwd', 'pass'],
            'url': ['url', 'website'],
            'cc-name': ['cc-name', 'card-name', 'cardholder', 'card-holder'],
            'cc-number': ['cc-number', 'card-number', 'cardnumber', 'card'],
            'cc-exp': ['cc-exp', 'card-exp', 'expiry', 'expiration'],
            'cc-csc': ['cc-csc', 'cvc', 'cvv', 'security-code'],
            'bday': ['bday', 'birthday', 'date-of-birth', 'dob'],
        }
        
        # 检查所有文本输入字段
        for input_field in document.find_all('input'):
            if not input_field.has_attr('type'):
                continue
                
            input_type = input_field['type'].lower()
            if input_type not in ['text', 'email', 'tel', 'url', 'password', 'date']:
                continue
            
            # 检查是否有name或id属性
            field_id = input_field.get('id', '').lower()
            field_name = input_field.get('name', '').lower()
            
            # 检查是否有autocomplete属性
            has_autocomplete = input_field.has_attr('autocomplete') and input_field['autocomplete'].strip()
            
            # 根据字段名称推断应该使用的autocomplete值
            suggested_autocomplete = None
            for ac_value, patterns in common_fields.items():
                for pattern in patterns:
                    if (pattern in field_id or pattern in field_name):
                        suggested_autocomplete = ac_value
                        break
                if suggested_autocomplete:
                    break
            
            # 如果能推断出autocomplete值但没有设置
            if suggested_autocomplete and not has_autocomplete:
                issue = Issue(
                    rule=self,
                    element=input_field,
                    description=f"输入字段可能需要autocomplete=\"{suggested_autocomplete}\"属性"
                )
                issue.add_fix_suggestion(f"添加autocomplete=\"{suggested_autocomplete}\"属性")
                
                # 生成修复示例
                attrs = ' '.join([f'{k}="{v}"' for k, v in input_field.attrs.items() if k != 'autocomplete'])
                issue.add_code_example(
                    f'<input {attrs} autocomplete="{suggested_autocomplete}">',
                    f"添加autocomplete=\"{suggested_autocomplete}\"属性"
                )
                issues.append(issue)
        
        return issues
    
    def get_fix_suggestions(self, issue):
        """获取修复建议"""
        if "autocomplete" in issue.description:
            autocomplete_value = issue.description.split("autocomplete=\"")[1].split("\"")[0]
            return [
                f"添加autocomplete=\"{autocomplete_value}\"属性",
                "确保autocomplete值与字段用途匹配"
            ]
        
        return []
