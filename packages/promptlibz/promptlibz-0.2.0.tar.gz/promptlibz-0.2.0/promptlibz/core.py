""" prompt lib"""
from enum import Enum
from .prompts import Prompt,RichPrompt
from .prompts import Images
from .prompts import JudgeType,GenerateSchedule,Notes,ExtraText,Mermaid,GitHelp


class TemplateType(Enum):
    """ template type"""
    JUDGETYPE = 'JudgeType'
    GENERATE_SCHEDULE = 'GenerateSchedule'
    NOTES = 'Notes'
    EXTRATEXT = "ExtraText"
    GITHELP = "GitHelp"
    MERMAID = "Mermaid"
    RICH_IMAGES = "RichImages"

class Templates:
    """Template Factory"""
    def __new__(cls, template_type: TemplateType) -> Prompt|RichPrompt:
        assert template_type.value in [item.value for item in TemplateType]

        if template_type.value == 'JudgeType':
            return JudgeType()

        elif template_type.value == 'GenerateSchedule':
            # 定义提示模板字符串
            return GenerateSchedule()
        elif template_type.value == 'Notes':
            # 定义提示模板字符串
            return Notes()
        elif template_type.value == 'ExtraText':
            # 定义提示模板字符串
            return ExtraText()
        elif template_type.value == 'GitHelp':
            # 定义提示模板字符串
            return GitHelp()
        elif template_type.value == 'Mermaid':
            # 定义提示模板字符串
            return Mermaid()
        elif template_type.value == 'RichImages':
            # 定义提示模板字符串
            return Images()
        elif template_type.value == 'Other':
            # 定义提示模板字符串
            return None
        else:
            # 定义提示模板字符串
            return None
