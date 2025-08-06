#!/usr/bin/env python3
"""
Script to add new celebrities to the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.services.celebrity_service import CelebrityService
from app.schemas.celebrity import CelebrityCreate

def add_new_celebrities():
    """Add new celebrities to the database"""
    db = SessionLocal()
    try:
        celebrity_service = CelebrityService(db)
        
        # New celebrities data
        new_celebrities = [
            {
                "name": "肖战",
                "name_en": "Xiao Zhan",
                "description": "因主演《陈情令》爆红，影视、歌手与商业代言界多面发展，顶级流量明星之一",
                "image_url": ""
            },
            {
                "name": "王一博",
                "name_en": "Wang Yibo",
                "description": "演员、歌手、舞者、职业摩托车手，多栖发展，自《陈情令》成名",
                "image_url": ""
            },
            {
                "name": "易烊千玺",
                "name_en": "Jackson Yee",
                "description": "TFBoys成员起家，后凭《少年的你》《长津湖》等作品转型严肃演员",
                "image_url": ""
            },
            {
                "name": "杨洋",
                "name_en": "Yang Yang",
                "description": "因青春偶像剧成名，后主演多部电视剧与电影，国民男神代表",
                "image_url": ""
            },
            {
                "name": "蔡徐坤",
                "name_en": "Cai Xukun",
                "description": "由选秀出道的流量歌手兼全能艺人，多个国际品牌代言人",
                "image_url": ""
            },
            {
                "name": "周冬雨",
                "name_en": "Zhou Dongyu",
                "description": "实力派演员，主演《山楂树之恋》《少年的你》，多次登福布斯名人榜前列",
                "image_url": ""
            },
            {
                "name": "范冰冰",
                "name_en": "Fan Bingbing",
                "description": "曾连续多年位列福布斯中国名人榜前十，中国最国际化的女星之一",
                "image_url": ""
            },
            {
                "name": "张艺谋",
                "name_en": "Zhang Yimou",
                "description": "著名导演，执导《英雄》《十面埋伏》《影》，国际电影界重要代表",
                "image_url": ""
            },
            {
                "name": "章子怡",
                "name_en": "Zhang Ziyi",
                "description": "凭《卧虎藏龙》《艺伎回忆录》走红全球，代表中国女性影人国际化",
                "image_url": ""
            },
            {
                "name": "刘宇宁",
                "name_en": "Liu Yuning",
                "description": "近年来以歌手和演员双重身份走红，新生代流量偶像",
                "image_url": ""
            }
        ]
        
        created_count = 0
        for celeb_data in new_celebrities:
            try:
                celebrity = celebrity_service.create_celebrity(CelebrityCreate(**celeb_data))
                print(f"Created celebrity: {celebrity.name} ({celebrity.name_en})")
                created_count += 1
                
                # Add tags based on description content
                if "演员" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "演员")
                if "歌手" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "歌手")
                if "导演" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "导演")
                if "舞者" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "舞者")
                if "流量" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "流量明星")
                if "偶像" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "偶像")
                if "实力派" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "实力派")
                if "国际化" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "国际化")
                if "新生代" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "新生代")
                    
            except Exception as e:
                print(f"Error creating {celeb_data['name']}: {e}")
        
        print(f"\nSuccessfully created {created_count} new celebrities!")
        print(f"New celebrities added to database")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding New Celebrities to 16型花名册")
    print("=" * 50)
    
    add_new_celebrities()
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Check the celebrities page: http://localhost:8000/celebrities")
    print("2. View API documentation: http://localhost:8000/docs")
    print("3. Test celebrity endpoints:")
    print("   - GET /celebrities/ - List all celebrities")
    print("   - GET /celebrities/tag/演员 - Get celebrities by tag")
    print("   - POST /celebrities/ - Create new celebrity (admin only)") 