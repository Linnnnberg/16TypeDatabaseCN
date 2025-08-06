#!/usr/bin/env python3
"""
Data template for easy bulk imports
Just modify this data and run bulk_data_import.py
"""

# Template for adding new celebrities with votes
CELEBRITIES_DATA = [
    {
        "name": "名人姓名",
        "name_en": "English Name",
        "description": "简短描述",
        "image_url": "https://example.com/image.jpg",  # 可选
        "mbti": "INTJ",  # 16种MBTI类型之一
        "vote_reason": "为什么认为这个名人是这个MBTI类型的理由",
        "tags": ["标签1", "标签2", "标签3"],  # 相关标签
    },
    # 复制上面的格式添加更多名人
]

# 可用的MBTI类型
MBTI_TYPES = [
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
    "ESTP",
    "ESFP",
]

# 常用标签
COMMON_TAGS = [
    # 职业
    "演员",
    "歌手",
    "导演",
    "制片人",
    "音乐人",
    "舞者",
    "编剧",
    "主持人",
    # 地区
    "中国",
    "香港",
    "台湾",
    "美国",
    "英国",
    "日本",
    "韩国",
    # 特点
    "流量明星",
    "偶像",
    "实力派",
    "国际化",
    "新生代",
    "经典",
    # 领域
    "电影",
    "电视剧",
    "音乐",
    "综艺",
    "体育",
    "科技",
    "商业",
]

# 使用示例
EXAMPLE_DATA = [
    {
        "name": "周杰伦",
        "name_en": "Jay Chou",
        "description": "台湾著名歌手、音乐人、演员、导演",
        "image_url": "",
        "mbti": "INTP",
        "vote_reason": "周杰伦表现出INTP的特点：内向、理性、创新思维，在音乐创作中展现独特的逻辑性和创造力。",
        "tags": ["歌手", "音乐人", "演员", "导演", "台湾"],
    }
]
