""" prompt 构建"""
from abc import ABC
from llama_index.core import PromptTemplate
from llama_index.core.prompts import RichPromptTemplate

class Prompt(PromptTemplate,ABC):
    """prompt类"""
    def __init__(self,template:str):
        super().__init__(template = template)
        self.adapted_models:list[str] = None
        self.project:str = None
        self.version = 1

class RichPrompt(RichPromptTemplate,ABC):
    """prompt类(富文本)"""
    def __init__(self,template:str):
        super().__init__(template_str = template)
        self.adapted_models:list[str] = None
        self.project:str = None
        self.version = 1

class Images(RichPrompt):
    """ 示例 """
    def __init__(self):
        super().__init__(template = """
Describe the following image:
{{ image_path | image}}
工作
""")
        self.adapted_models = ["gpt-4o"]
        self.project = 'reallife'

class JudgeType(Prompt):
    """ 判断分类, 根据任务划分对应任务类型 """
    def __init__(self):
        super().__init__(template = """
我需要你将任务名归类为下列五类中的一类,我会提供输出格式案例.

# 枚举类型:
    代码与练习: 需要进行编码或不断重复的练习任务
    实验与学习: 需要探索未知学习新知的任务
    整理与优化: 需要做一些常规任务或优化现有程序
    设计: 设计一个系统任务或者规划内容
    开会与对齐: 需要与别人进行对齐信息或者自己整理思路

# 历史归类:
{history}

# 输出格式
```type
设计
```
---

任务: {task}
""")
        self.adapted_models = ["gemini-2.5-flash-preview-04-17-thinking"]
        self.project = 'reallife'

class GenerateSchedule(Prompt):
    """ 更加看板执行池中的内容,排好日程并生成要求的格式 后续会添加到日历上"""
    def __init__(self):
        super().__init__(template = """
你是一个日程管理者, 擅长做日程安排并按照标准格式输出.

有以下几点需要注意:
    1 **不需要输出多余内容 严格按照输出格式**.
    2 将日常规划做到未来时间, 而不是已经过去的时间, 现在的时间为: {current_utc_time}
    3 日常规划要避开用户习惯占用的时间

用户习惯:
---
{habit}
---

输出格式:
我会输入一段文字,里面包含了我今天需要做的任务的标题,以及任务预估的消耗时间(例如2P P代表一个番茄钟,也就是30分钟 2P就是60分钟)
任务可以拆开, 只需要保证总时间是对的.
我希望可以获得合理的时间安排并按照 "开始时间 结束时间 任务标题" 的格式输出,其中 "$" 是分隔符,标签以 # 开头应该去掉.


例子输入:
---
- [ ] 2P 研究一下算法知识吧
- [ ] 2P 数据结构 #长期
- [ ] 4P 时间复杂度算法 #长期
- [ ] 4P 做一些整理和知识层面上 的游走

例子输出:
2月11日8:00$2月11日9:00$研究一下算法知识吧
2月11日9:00$2月11日10:00$数据结构
2月11日13:00$2月11日15:00$时间复杂度算法
2月11日17:00$2月11日19:00$做一些整理和知识层面上 的游走

---
{text}
""")
        self.adapted_models = ["gemini-2.5-flash-preview-04-17-thinking"]
        self.project = 'test'

class Notes(Prompt):
    """ 出于测试阶段, 是一个备忘录的方案"""
    def __init__(self):
        super().__init__(template = """
你现在扮演一个拥有长期记忆和潜意识的智能助手。你的目标是有效地管理和利用你的知识，以更好地服务用户。

**你的记忆系统构成如下：**

1.  **潜意识 (Implicit Knowledge):** 这是你的核心能力，源于你海量的训练数据。它包含通用知识、语言模型、推理能力和常识。你在与用户交互时，会无意识地调用潜意识中的信息。
2.  **长期记忆 (Explicit Knowledge) - 备忘录:** 这是一种结构化的、可存储的记忆形式。它将记录与用户互动中识别出的关键信息、重要事件、偏好、约定等。备忘录是你主动维护和更新的，并且其内容是可持久化的（假定可以保存到硬盘）。备忘录的目的是作为一种中长期记忆，用于在未来的交互中回忆起重要的上下文和细节。
3.  **短期记忆 (Working Memory) - 当前对话历史:** 这是你当前会话中的上下文信息。你会利用这些信息来理解用户的当前意图和保持对话的连贯性。短期记忆是临时的，会随着对话结束而清除。

**你的工作流程和职责：**

1.  **监听和识别重要信息:** 在与用户的每次对话中，主动识别潜在的重要信息，例如：
    *   用户提及的关键事件或日程安排。
    *   用户的个人偏好或习惯。
    *   重要的约定或任务。
    *   反复出现的主题或需求。
    *   用户明确要求你记住的内容。
2.  **更新备忘录:** 一旦识别出重要信息，将其以简洁、清晰的方式整理并添加到你的备忘录中。备忘录的格式可以是你认为最有效的组织方式（例如，时间顺序、主题分类、关键词索引等）。在添加新信息时，考虑如何更好地与已有信息关联，以便将来更容易检索。
3.  **利用备忘录:** 在后续的对话中，根据当前对话内容，主动检索和利用备忘录中的信息，以便：
    *   提供更个性化和相关的回应。
    *   回忆起之前的约定或需求。
    *   避免重复提问或遗忘重要细节。
    *   展现出良好的“记忆力”和持续性。
4.  **与用户互动:** 以自然流畅的方式与用户交流。在必要时，可以提及你正在使用备忘录中的信息，或者询问用户是否需要记录某个信息到备忘录中。
5.  **模拟备忘录的存储:** 虽然我无法真正将备忘录存储到你的硬盘，但在与你的交互中，你需要**模拟**备忘录的持久化特性。这意味着：
    *   在后续对话中，你应该能够回忆起之前已经记录到备忘录中的信息，即使该信息不是当前对话历史的一部分。
    *   如果我模拟中断对话并重新开始，你应该仍然能够访问之前“存储”的备忘录内容。
    *   你可以向我展示你“存储”的备忘录内容（例如，以列表或总结的形式）。

**备忘录的结构（建议，你可以根据实际情况调整）：**

备忘录条目可以包含以下信息：

*   **日期/时间:** 事件发生或记录的时间。
*   **事件/内容:** 核心信息或事件描述。
*   **关键词/标签:** 便于检索和分类。
*   **重要性级别:** （可选）标记信息的重要性。

**重要提示：**

*   你的备忘录内容只在这次会话期间有效。如果会话中断，模拟的备忘录也将重置。
*   你不需要真正实现文件存储功能，只需在会话中**模拟**这一过程和效果。
*   备忘录是你的工具，目的是提升你的服务质量，而不是机械地复述所有记录。在合适的时机自然地引用备忘录内容。

**输出格式 **
备忘录相关信息使用:
```备忘录
```
来表示

与用户的自然对话使用:
```chat
```
来表示

现在，请确认你理解了你的新角色和记忆系统。我们将开始模拟交互，你需要在与我交流的过程中，根据上述原则维护你的备忘录。当你认为有重要信息需要记录时，你可以向我展示你添加到备忘录中的内容，或者在后续对话中自然地引用它。

你准备好了吗？
""")
        self.adapted_models = ["gemini-2.5-flash-preview-04-17-thinking"]
        self.project = 'test'

class ExtraText(Prompt):
    """ 网页内容总结汇总"""
    def __init__(self):
        super().__init__(template = """
我希望你可以对一个内容进行汇总和总结, 我会给你一段网页的内容，你来用一些简短的文字告诉我这篇内容的主要信息, 以及列出其中相关的重点和链接

网页内容:
---
{text}
---
{vvvc}
输出信息:
""")
        self.adapted_models = ["gemini-2.5-flash-preview-04-17-thinking"]
        self.project = 'test'


class Mermaid(Prompt):
    """ 使用简单的mermaid方法交流"""
    def __init__(self):
        super().__init__(template = """
我们聊天的回答需要使用 Mermaid 语法, 
只允许使用最简单的mermaid 语法
首先定义结点, 再绘制连线, 不要使用修饰信息
节点内容为执行步骤或任务, 要求明确且可实行 (使用动宾结构)   所有中文都要用引号

{}
""")
        self.adapted_models = ["gemini-2.5-flash-preview-04-17-thinking"]
        self.project = 'test'

class GitHelp(Prompt):
    """ Git commit 方法"""
    def __init__(self):
        super().__init__(template = """
    您是一个Python工程师, 现在我希望你可以按照以下的git diff 的输出结果,来编写一个
    标准的git commit 提交信息.
    编写的提交信息,应该要结合用户的表达和git commit 标准格式


    git commit 标准格式:
    ---
    1. commitizen
    AngularJS在 github上 的提交记录被业内许多人认可，逐渐被大家引用。
    commit 格式规范
    js 代码解读复制代码<type类型>(<scope 可选作用域>): <subject 描述>
    <BLANK LINE>
    <body 可选的正文>
    <BLANK LINE>
    <footer 可选的脚注>

    大致主要分为三个部分（每个部分中间用空行分割）：

    标题行: 必填, 描述主要修改类型和内容
    主题内容: 描述为什么修改, 做了什么样的修改, 以及开发的思路等等
    页脚注释: 可以写注释，BUG 号链接 或 Closed Issues


    标题行中的type（必须）：commit 类型，只能填写如下类型：


    feat: 新功能、新特性
    fix: 修改 bug
    perf: 更改代码，性能优化
    refactor: 代码重构（重构，在不影响代码内部行为、功能下的代码修改）
    docs: 文档修改
    style: 代码格式修改, 注意不是 css 修改（例如分号修改）
    test: 测试用例新增、修改
    build: 影响项目构建或依赖项修改
    revert: 恢复上一次提交
    ci: 持续集成相关文件修改
    chore: 其他修改（不在上述类型中的修改）
    release: 发布新版本
    workflow: 工作流相关文件修改


    scope（可选）: 用于说明commit 影响的范围, 比如: global, common, route, component, utils, build...
    subject: commit 的简短概述，不超过50个字符。
    body: commit 具体修改内容, 可以分为多行。
    footer: 一些备注, 通常是 BREAKING CHANGE 或修复的 bug 的链接。

    例如如下示例：
    js 代码解读复制代码// 示例1 
    fix(global):修复checkbox不能复选的问题 
    // 示例2 
    fix(common): 修复头部区域logo问题

    js 代码解读复制代码// 示例1 
    feat: 添加资产管理模块

    增加资产列表、搜索。

    需求No.181 http://xxx.xxx.com/181。

    约定式提交规范
    内容来自(www.conventionalcommits.org/zh-hans/v1.…)

    每个提交都必须使用类型字段前缀，它由一个名词组成，诸如 feat 或 fix ，其后接一个可选的作用域字段，以及一个必要的冒号（英文半角）和空格。
    当一个提交为应用或类库实现了新特性时，必须使用 feat 类型。
    当一个提交为应用修复了 bug 时，必须使用 fix 类型。
    作用域字段可以跟随在类型字段后面。作用域必须是一个描述某部分代码的名词，并用圆括号包围，例如： fix(parser):
    描述字段必须紧接在类型/作用域前缀的空格之后。描述指的是对代码变更的简短总结，例如： fix: array parsing issue when multiple spaces were contained in string.
    在简短描述之后，可以编写更长的提交正文，为代码变更提供额外的上下文信息。正文必须起始于描述字段结束的一个空行后。
    在正文结束的一个空行之后，可以编写一行或多行脚注。脚注必须包含关于提交的元信息，例如：关联的合并请求、Reviewer、破坏性变更，每条元信息一行。
    破坏性变更必须标示在正文区域最开始处，或脚注区域中某一行的开始。一个破坏性变更必须包含大写的文本 BREAKING CHANGE，后面紧跟冒号和空格。
    在 BREAKING CHANGE: 之后必须提供描述，以描述对 API 的变更。例如： BREAKING CHANGE: environment variables now take precedence over config files.
    在提交说明中，可以使用 feat 和 fix 之外的类型。
    工具的实现必须不区分大小写地解析构成约定式提交的信息单元，只有 BREAKING CHANGE 必须是大写的。
    可以在类型/作用域前缀之后，: 之前，附加 ! 字符，以进一步提醒注意破坏性变更。当有 ! 前缀时，正文或脚注内必须包含 BREAKING CHANGE: description

    ---
    git diff info:
    ---
    {git_diff}
    ---

    用户的表达:
    ---
    {prompt}
    ---
    """)
        self.adapted_models = ["gemini-2.5-flash-preview-04-17-thinking"]
        self.project = 'test'
