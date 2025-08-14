"""
MBTI Type Mapping Data Structure
Contains Chinese names, English names, and descriptions for all 16 MBTI types
"""

from typing import Dict, List, Optional


class MBTITypeInfo:
    """Information structure for an MBTI type"""

    def __init__(self, code: str, chinese: str, english: str, description: str):
        self.code = code
        self.chinese = chinese
        self.english = english
        self.description = description


# MBTI Type Mapping with Chinese names, English names, and descriptions
MBTI_TYPE_MAPPING = {
    "INTJ": {
        "chinese": "建筑师",
        "english": "Architect",
        "description": "富有想象力和战略性的思考者，一切都要经过深思熟虑",
    },
    "INTP": {
        "chinese": "逻辑学家",
        "english": "Logician",
        "description": "具有创新想法和独特见解的发明家",
    },
    "ENTJ": {
        "chinese": "指挥官",
        "english": "Commander",
        "description": "大胆、富有想象力的领导者，总能找到或创造解决方案",
    },
    "ENTP": {
        "chinese": "辩论家",
        "english": "Debater",
        "description": "聪明好奇的思想家，不会放过任何智力挑战",
    },
    "INFJ": {
        "chinese": "提倡者",
        "english": "Advocate",
        "description": "安静而神秘，富有同情心和洞察力",
    },
    "INFP": {
        "chinese": "调停者",
        "english": "Mediator",
        "description": "诗意、善良的利他主义者，总是热情地为正当理由而努力",
    },
    "ENFJ": {
        "chinese": "主人公",
        "english": "Protagonist",
        "description": "富有魅力和鼓舞人心的领导者，具有强烈的同理心",
    },
    "ENFP": {
        "chinese": "竞选者",
        "english": "Campaigner",
        "description": "热情、有创造力、社交能力强，总是能找到理由微笑",
    },
    "ISTJ": {
        "chinese": "物流师",
        "english": "Logistician",
        "description": "实际而注重事实的个体，可靠性无可挑剔",
    },
    "ISFJ": {
        "chinese": "守卫者",
        "english": "Defender",
        "description": "非常专注和温暖的守护者，时刻准备保护所爱的人",
    },
    "ESTJ": {
        "chinese": "总经理",
        "english": "Executive",
        "description": "优秀的管理者，在管理事情或人员方面无与伦比",
    },
    "ESFJ": {
        "chinese": "执政官",
        "english": "Consul",
        "description": "非常关心他人，社交能力强，总是渴望帮助",
    },
    "ISTP": {
        "chinese": "鉴赏家",
        "english": "Virtuoso",
        "description": "大胆而实际的实验家，掌握各种工具",
    },
    "ISFP": {
        "chinese": "探险家",
        "english": "Adventurer",
        "description": "灵活而有魅力的艺术家，随时准备探索和体验新事物",
    },
    "ESTP": {
        "chinese": "企业家",
        "english": "Entrepreneur",
        "description": "聪明、精力充沛、非常善于感知的人，真正享受生活在边缘",
    },
    "ESFP": {
        "chinese": "表演者",
        "english": "Entertainer",
        "description": "自发的、精力充沛的表演者，生活永远不会无聊",
    },
}


def get_mbti_type_info(type_code: str) -> Optional[Dict[str, str]]:
    """Get information for a specific MBTI type"""
    return MBTI_TYPE_MAPPING.get(type_code.upper())


def get_chinese_name(type_code: str) -> Optional[str]:
    """Get Chinese name for an MBTI type"""
    info = get_mbti_type_info(type_code)
    return info.get("chinese") if info else None


def get_english_name(type_code: str) -> Optional[str]:
    """Get English name for an MBTI type"""
    info = get_mbti_type_info(type_code)
    return info.get("english") if info else None


def get_description(type_code: str) -> Optional[str]:
    """Get description for an MBTI type"""
    info = get_mbti_type_info(type_code)
    return info.get("description") if info else None


def get_all_types() -> List[str]:
    """Get list of all MBTI type codes"""
    return list(MBTI_TYPE_MAPPING.keys())


def get_all_types_with_info() -> List[Dict[str, str]]:
    """Get all MBTI types with their information"""
    return [
        {
            "code": code,
            "chinese_name": info["chinese"],
            "english_name": info["english"],
            "description": info["description"],
        }
        for code, info in MBTI_TYPE_MAPPING.items()
    ]


def validate_mbti_type(type_code: str) -> bool:
    """Validate if a type code is valid"""
    return type_code.upper() in MBTI_TYPE_MAPPING
