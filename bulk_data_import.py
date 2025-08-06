#!/usr/bin/env python3
"""
Fast bulk import script for celebrities and votes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal, engine
from app.database.models import Celebrity, Tag, CelebrityTag, Vote, User, UserRole, MBTIType
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

def bulk_import_data():
    """Fast bulk import of celebrities and votes"""
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print("Starting bulk data import...")
        
        # Get system user
        system_user = db.query(User).filter(User.role == UserRole.SYSTEM).first()
        if not system_user:
            print("System user not found. Please run create_admin.py first.")
            return
        
        # Celebrities data with votes
        celebrities_data = [
            {
                "name": "肖战",
                "name_en": "Xiao Zhan",
                "description": "因主演《陈情令》爆红，影视、歌手与商业代言界多面发展，顶级流量明星之一",
                "image_url": "",
                "mbti": "INTJ",
                "vote_reason": "多数 MBTI‐typing 社群倾向认为肖战是 INTJ（也有粉丝支持 INFJ/ENFJ），因其独立、有远见、严谨规划未来，具洞察力和领导感。",
                "tags": ["演员", "歌手", "流量明星"]
            },
            {
                "name": "王一博",
                "name_en": "Wang Yibo",
                "description": "演员、歌手、舞者、职业摩托车手，多栖发展，自《陈情令》成名",
                "image_url": "",
                "mbti": "ISTP",
                "vote_reason": "主流观点认为 ISTP，更偏向实用型、冷静且擅长技术与艺术表达，也享受个人世界和体验过程。",
                "tags": ["演员", "歌手", "舞者"]
            },
            {
                "name": "易烊千玺",
                "name_en": "Jackson Yee",
                "description": "TFBoys成员起家，后凭《少年的你》《长津湖》等作品转型严肃演员",
                "image_url": "",
                "mbti": "INTP",
                "vote_reason": "推测为 INTP，理性内省，有创造力且专注专业成长（基于粉丝分析偏向思考型）。",
                "tags": ["演员", "歌手"]
            },
            {
                "name": "杨洋",
                "name_en": "Yang Yang",
                "description": "因青春偶像剧成名，后主演多部电视剧与电影，国民男神代表",
                "image_url": "",
                "mbti": "ISFJ",
                "vote_reason": "常被看作 ISFJ，温柔体贴，勤于责任、忠实粉丝，形象稳重亲和。",
                "tags": ["演员", "偶像"]
            },
            {
                "name": "蔡徐坤",
                "name_en": "Cai Xukun",
                "description": "由选秀出道的流量歌手兼全能艺人，多个国际品牌代言人",
                "image_url": "",
                "mbti": "ENFJ",
                "vote_reason": "粉丝分析及公众形象多倾向 ENFJ，善于社交、影响力强，具号召力与感染力。",
                "tags": ["歌手", "流量明星"]
            },
            {
                "name": "周冬雨",
                "name_en": "Zhou Dongyu",
                "description": "实力派演员，主演《山楂树之恋》《少年的你》，多次登福布斯名人榜前列",
                "image_url": "",
                "mbti": "INFP",
                "vote_reason": "推测为 INFP，偏内向、富想象，表演风格细腻感性，有强内在价值观。",
                "tags": ["演员", "实力派"]
            },
            {
                "name": "范冰冰",
                "name_en": "Fan Bingbing",
                "description": "曾连续多年位列福布斯中国名人榜前十，中国最国际化的女星之一",
                "image_url": "",
                "mbti": "ENTJ",
                "vote_reason": "普遍认为范冰冰为 ENTJ，性格果敢，事业导向明显，具领导力和高目标规划力。",
                "tags": ["演员", "国际化"]
            },
            {
                "name": "张艺谋",
                "name_en": "Zhang Yimou",
                "description": "著名导演，执导《英雄》《十面埋伏》《影》，国际电影界重要代表",
                "image_url": "",
                "mbti": "INTJ",
                "vote_reason": "被认为是 INTJ 类型，擅长宏观构架、独立思考，具视觉远见和艺术架构思维。",
                "tags": ["导演", "国际化"]
            },
            {
                "name": "章子怡",
                "name_en": "Zhang Ziyi",
                "description": "凭《卧虎藏龙》《艺伎回忆录》走红全球，代表中国女性影人国际化",
                "image_url": "",
                "mbti": "ESTJ",
                "vote_reason": "有观点认为她是 ESTJ，执行力强、专业高度自律且组织能力佳，表现坚决果断。",
                "tags": ["演员", "国际化"]
            },
            {
                "name": "刘宇宁",
                "name_en": "Liu Yuning",
                "description": "近年来以歌手和演员双重身份走红，新生代流量偶像",
                "image_url": "",
                "mbti": "ISFP",
                "vote_reason": "推测为 ISFP，新生代偶像型艺人，感性表达强，形象自然随性，较注重当下体验。",
                "tags": ["歌手", "演员", "新生代"]
            }
        ]
        
        # Bulk create celebrities
        print("Creating celebrities...")
        celebrities_to_add = []
        votes_to_add = []
        tags_to_add = []
        celebrity_tags_to_add = []
        
        # Track existing tags
        existing_tags = {tag.name: tag for tag in db.query(Tag).all()}
        
        for celeb_data in celebrities_data:
            # Create celebrity
            celebrity = Celebrity(
                id=str(uuid.uuid4()),
                name=celeb_data["name"],
                name_en=celeb_data["name_en"],
                description=celeb_data["description"],
                image_url=celeb_data["image_url"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            celebrities_to_add.append(celebrity)
            
            # Create vote
            vote = Vote(
                id=str(uuid.uuid4()),
                user_id=system_user.id,
                celebrity_id=celebrity.id,
                mbti_type=MBTIType(celeb_data["mbti"]),
                reason=celeb_data["vote_reason"],
                created_at=datetime.utcnow()
            )
            votes_to_add.append(vote)
            
            # Handle tags
            for tag_name in celeb_data["tags"]:
                if tag_name not in existing_tags:
                    tag = Tag(
                        id=str(uuid.uuid4()),
                        name=tag_name,
                        created_at=datetime.utcnow()
                    )
                    tags_to_add.append(tag)
                    existing_tags[tag_name] = tag
                
                # Create celebrity-tag relationship
                celebrity_tag = CelebrityTag(
                    celebrity_id=celebrity.id,
                    tag_id=existing_tags[tag_name].id
                )
                celebrity_tags_to_add.append(celebrity_tag)
        
        # Bulk insert everything
        print("Bulk inserting data...")
        
        if tags_to_add:
            db.bulk_save_objects(tags_to_add)
            print(f"Added {len(tags_to_add)} new tags")
        
        db.bulk_save_objects(celebrities_to_add)
        print(f"Added {len(celebrities_to_add)} celebrities")
        
        db.bulk_save_objects(votes_to_add)
        print(f"Added {len(votes_to_add)} votes")
        
        db.bulk_save_objects(celebrity_tags_to_add)
        print(f"Added {len(celebrity_tags_to_add)} celebrity-tag relationships")
        
        # Commit all changes
        db.commit()
        
        print(f"\nBulk import completed successfully!")
        print(f"Summary:")
        print(f"   - Celebrities: {len(celebrities_to_add)}")
        print(f"   - Votes: {len(votes_to_add)}")
        print(f"   - Tags: {len(tags_to_add)}")
        print(f"   - Tag relationships: {len(celebrity_tags_to_add)}")
        
    except Exception as e:
        db.rollback()
        print(f"Error during bulk import: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Fast Bulk Data Import for 16型花名册")
    print("=" * 50)
    
    bulk_import_data()
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Check the celebrities page: http://localhost:8000/celebrities")
    print("2. View vote statistics: http://localhost:8000/votes/")
    print("3. Test the application with real data!") 