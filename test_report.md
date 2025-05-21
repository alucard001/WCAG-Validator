# WCAG 2.2 验证报告

生成时间: 2025-05-21 00:31:16
URL: file:///home/ubuntu/wcag_validator/test_sample.html

## 摘要

- **总问题数:** 17
- **A级问题:** 13
- **AA级问题:** 4
- **AAA级问题:** 0
- **通过规则:** 3
- **失败规则:** 9

## 问题详情

### 1. 图像必须有alt属性

**WCAG标准:** 1.1.1 (级别 A)

**问题描述:** 图像缺少alt属性

**位置:** `行 0, 列 0, 路径 /[document]/html/body/img`

**问题代码:**
```html
<img src="logo.png"/>
```

**修复建议:**

- 添加描述性的alt属性，说明图像内容和目的

**代码示例:**

```html
<img src="logo.png" alt="[图像描述]">
```
*添加描述性alt属性的示例*

[了解更多关于 WCAG 1.1.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-1-1.html)

---

### 2. 图像必须有alt属性

**WCAG标准:** 1.1.1 (级别 A)

**问题描述:** 图像的alt属性为空

**位置:** `行 0, 列 0, 路径 /[document]/html/body/img[2]`

**问题代码:**
```html
<img alt="" src="banner.jpg"/>
```

**修复建议:**

- 如果图像是装饰性的，请添加role="presentation"属性
- 如果图像包含信息，请添加描述性的alt属性

**代码示例:**

```html
<img src="banner.jpg" alt="[图像描述]">
```
*信息性图像示例*

```html
<img src="banner.jpg" alt="" role="presentation">
```
*装饰性图像示例*

[了解更多关于 WCAG 1.1.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-1-1.html)

---

### 3. 表单控件必须有关联的标签

**WCAG标准:** 1.3.1 (级别 A)

**问题描述:** 表单控件 (id="username") 没有关联的标签

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input`

**问题代码:**
```html
<input id="username" type="text"/>
```

**修复建议:**

- 添加for属性与控件id匹配的label元素
- 或将控件放在label元素内

**代码示例:**

```html
<label for="username">标签文本</label>
<input id="username" type="text"/>
```
*使用for属性关联标签*

```html
<label>
  标签文本
  <input id="username" type="text"/>
</label>
```
*将控件放在标签内*

[了解更多关于 WCAG 1.3.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-1.html)

---

### 4. 表单控件必须有关联的标签

**WCAG标准:** 1.3.1 (级别 A)

**问题描述:** 与表单控件关联的标签 (for="password") 没有文本内容

**位置:** `行 18, 列 5, 路径 /[document]/html/body/label`

**问题代码:**
```html
<label for="password"></label>
```

**修复建议:**

- 为标签添加描述性文本

**代码示例:**

```html
<label for="password">描述性标签文本</label>
```
*添加描述性标签文本*

[了解更多关于 WCAG 1.3.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-1.html)

---

### 5. 表单控件必须有关联的标签

**WCAG标准:** 1.3.1 (级别 A)

**问题描述:** 表单控件 (id="email") 没有关联的标签

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input[5]`

**问题代码:**
```html
<input id="email" name="email" type="text"/>
```

**修复建议:**

- 添加for属性与控件id匹配的label元素
- 或将控件放在label元素内

**代码示例:**

```html
<label for="email">标签文本</label>
<input id="email" name="email" type="text"/>
```
*使用for属性关联标签*

```html
<label>
  标签文本
  <input id="email" name="email" type="text"/>
</label>
```
*将控件放在标签内*

[了解更多关于 WCAG 1.3.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-1.html)

---

### 6. 表单控件必须有关联的标签

**WCAG标准:** 1.3.1 (级别 A)

**问题描述:** 表单控件 (id="phone") 没有关联的标签

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input[6]`

**问题代码:**
```html
<input id="phone" name="phone" type="text"/>
```

**修复建议:**

- 添加for属性与控件id匹配的label元素
- 或将控件放在label元素内

**代码示例:**

```html
<label for="phone">标签文本</label>
<input id="phone" name="phone" type="text"/>
```
*使用for属性关联标签*

```html
<label>
  标签文本
  <input id="phone" name="phone" type="text"/>
</label>
```
*将控件放在标签内*

[了解更多关于 WCAG 1.3.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-1.html)

---

### 7. 相关表单控件应使用fieldset分组

**WCAG标准:** 1.3.1 (级别 A)

**问题描述:** 单选按钮组 (name="gender") 没有使用fieldset和legend元素分组

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input[3]`

**问题代码:**
```html
<input id="male" name="gender" type="radio"/>
```

**修复建议:**

- 使用fieldset元素包围单选按钮组
- 添加legend元素描述单选按钮组的用途

**代码示例:**

```html
<fieldset>
  <legend>gender选项</legend>
  <input id="male" name="gender" type="radio"/> <label for="male">选项文本</label>
  <input id="female" name="gender" type="radio"/> <label for="female">选项文本</label>
</fieldset>
```
*使用fieldset和legend分组单选按钮*

[了解更多关于 WCAG 1.3.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-1.html)

---

### 8. 输入字段应使用适当的autocomplete属性

**WCAG标准:** 1.3.5 (级别 AA)

**问题描述:** 输入字段可能需要autocomplete="name"属性

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input`

**问题代码:**
```html
<input id="username" type="text"/>
```

**修复建议:**

- 添加autocomplete="name"属性

**代码示例:**

```html
<input type="text" id="username" autocomplete="name">
```
*添加autocomplete="name"属性*

[了解更多关于 WCAG 1.3.5 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-5.html)

---

### 9. 输入字段应使用适当的autocomplete属性

**WCAG标准:** 1.3.5 (级别 AA)

**问题描述:** 输入字段可能需要autocomplete="password"属性

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input[2]`

**问题代码:**
```html
<input id="password" type="password"/>
```

**修复建议:**

- 添加autocomplete="password"属性

**代码示例:**

```html
<input type="password" id="password" autocomplete="password">
```
*添加autocomplete="password"属性*

[了解更多关于 WCAG 1.3.5 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-5.html)

---

### 10. 输入字段应使用适当的autocomplete属性

**WCAG标准:** 1.3.5 (级别 AA)

**问题描述:** 输入字段可能需要autocomplete="email"属性

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input[5]`

**问题代码:**
```html
<input id="email" name="email" type="text"/>
```

**修复建议:**

- 添加autocomplete="email"属性

**代码示例:**

```html
<input type="text" name="email" id="email" autocomplete="email">
```
*添加autocomplete="email"属性*

[了解更多关于 WCAG 1.3.5 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-5.html)

---

### 11. 输入字段应使用适当的autocomplete属性

**WCAG标准:** 1.3.5 (级别 AA)

**问题描述:** 输入字段可能需要autocomplete="tel"属性

**位置:** `行 0, 列 0, 路径 /[document]/html/body/input[6]`

**问题代码:**
```html
<input id="phone" name="phone" type="text"/>
```

**修复建议:**

- 添加autocomplete="tel"属性

**代码示例:**

```html
<input type="text" name="phone" id="phone" autocomplete="tel">
```
*添加autocomplete="tel"属性*

[了解更多关于 WCAG 1.3.5 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-5.html)

---

### 12. 标题层次结构必须正确

**WCAG标准:** 1.3.1 (级别 A)

**问题描述:** 标题层次结构不正确：从h1跳到h3

**位置:** `行 29, 列 5, 路径 /[document]/html/body/h3`

**问题代码:**
```html
<h3>子标题</h3>
```

**修复建议:**

- 添加h2作为中间层次
- 或将当前h3改为h2

**代码示例:**

```html
<h2>中间层次标题</h2>
<h3>子标题</h3>
```
*添加中间层次标题*

```html
<h2>子标题</h2>
```
*将h3改为h2*

[了解更多关于 WCAG 1.3.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/1-3-1.html)

---

### 13. 页面必须指定语言

**WCAG标准:** 3.1.1 (级别 A)

**问题描述:** 页面没有通过html元素的lang属性指定默认语言

**位置:** `行 0, 列 0, 路径 /[document]/html`

**问题代码:**
```html
<html>
<head>
<title>WCAG测试页面</title>
<meta charset="utf-8"/>
</head>
<body>
<!-- 图像无alt属性 -->
<img ...
```

**修复建议:**

- 为html元素添加lang属性，指定页面的默认语言

**代码示例:**

```html
<html lang="zh-CN">
```
*指定简体中文*

```html
<html lang="en">
```
*指定英文*

[了解更多关于 WCAG 3.1.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/3-1-1.html)

---

### 14. HTML必须可以正确解析

**WCAG标准:** 4.1.1 (级别 A)

**问题描述:** 重复的id属性: 'content'已在其他元素中使用

**位置:** `行 37, 列 5, 路径 /[document]/html/body/div[2]`

**问题代码:**
```html
<div id="content">第二个内容</div>
```

**修复建议:**

- 修改id属性为唯一值

**代码示例:**

```html
<div id="unique-content" ></div>
```

[了解更多关于 WCAG 4.1.1 的信息](https://www.w3.org/WAI/WCAG22/Understanding/4-1-1.html)

---

### 15. ARIA属性必须正确使用

**WCAG标准:** 4.1.2 (级别 A)

**问题描述:** 元素的aria-label属性为空

**位置:** `行 40, 列 5, 路径 /[document]/html/body/button`

**问题代码:**
```html
<button aria-label="">提交</button>
```

**修复建议:**

- 为aria-label添加描述性文本
- 或移除空的aria-label属性

**代码示例:**

```html
<button  aria-label="描述性文本"></button>
```

[了解更多关于 WCAG 4.1.2 的信息](https://www.w3.org/WAI/WCAG22/Understanding/4-1-2.html)

---

### 16. 链接文本必须描述其目的

**WCAG标准:** 2.4.4 (级别 A)

**问题描述:** 链接文本 '点击这里' 不足以描述链接目的

**位置:** `行 32, 列 5, 路径 /[document]/html/body/a`

**问题代码:**
```html
<a href="page.html">点击这里</a>
```

**修复建议:**

- 使用描述链接目的的文本替换通用文本

**代码示例:**

```html
<a href="page.html">描述性链接文本</a>
```
*使用描述性链接文本*

[了解更多关于 WCAG 2.4.4 的信息](https://www.w3.org/WAI/WCAG22/Understanding/2-4-4.html)

---

### 17. 链接文本必须描述其目的

**WCAG标准:** 2.4.4 (级别 A)

**问题描述:** 链接没有描述性文本

**位置:** `行 33, 列 5, 路径 /[document]/html/body/a[2]`

**问题代码:**
```html
<a href="contact.html"></a>
```

**修复建议:**

- 添加描述链接目的的文本
- 或为链接添加aria-label属性

**代码示例:**

```html
<a href="contact.html">描述性链接文本</a>
```
*添加描述性链接文本*

```html
<a href="contact.html" aria-label="描述性链接文本"></a>
```
*添加aria-label属性*

[了解更多关于 WCAG 2.4.4 的信息](https://www.w3.org/WAI/WCAG22/Understanding/2-4-4.html)

---

*由 WCAG 2.2 验证器生成*