#!/usr/bin/env python3
"""
Script to add initial votes for celebrities with MBTI types and comments
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.services.celebrity_service import CelebrityService
from app.services.vote_service import VoteService
from app.services.auth_service import AuthService
from app.schemas.vote import VoteCreate
from app.database.models import User, UserRole

def add_initial_votes():
    """Add initial votes for celebrities"""
    db = SessionLocal()
    try:
        celebrity_service = CelebrityService(db)
        vote_service = VoteService(db)
        auth_service = AuthService(db)
        
        # Get or create a system user for these votes
        system_user = db.query(User).filter(User.role == UserRole.SYSTEM).first()
        if not system_user:
            print("❌ System user not found. Please run create_admin.py first.")
            return
        
        # Initial votes data
        initial_votes = [
            {
                "name": "肖战",
                "mbti": "INTJ",
                "comment": "多数 MBTI‐typing 社群倾向认为肖战是 INTJ（也有粉丝支持 INFJ/ENFJ），因其独立、有远见、严谨规划未来，具洞察力和领导感。"
            },
            {
                "name": "王一博",
                "mbti": "ISTP",
                "comment": "主流观点认为 ISTP，更偏向实用型、冷静且擅长技术与艺术表达，也享受个人世界和体验过程。"
            },
            {
                "name": "易烊千玺",
                "mbti": "INTP",
                "comment": "推测为 INTP，理性内省，有创造力且专注专业成长（基于粉丝分析偏向思考型）。"
            },
            {
                "name": "杨洋",
                "mbti": "ISFJ",
                "comment": "常被看作 ISFJ，温柔体贴，勤于责任、忠实粉丝，形象稳重亲和。"
            },
            {
                "name": "蔡徐坤",
                "mbti": "ENFJ",
                "comment": "粉丝分析及公众形象多倾向 ENFJ，善于社交、影响力强，具号召力与感染力。"
            },
            {
                "name": "周冬雨",
                "mbti": "INFP",
                "comment": "推测为 INFP，偏内向、富想象，表演风格细腻感性，有强内在价值观。"
            },
            {
                "name": "范冰冰",
                "mbti": "ENTJ",
                "comment": "普遍认为范冰冰为 ENTJ，性格果敢，事业导向明显，具领导力和高目标规划力。"
            },
            {
                "name": "张艺谋",
                "mbti": "INTJ",
                "comment": "被认为是 INTJ 类型，擅长宏观构架、独立思考，具视觉远见和艺术架构思维。"
            },
            {
                "name": "章子怡",
                "mbti": "ESTJ",
                "comment": "有观点认为她是 ESTJ，执行力强、专业高度自律且组织能力佳，表现坚决果断。"
            },
            {
                "name": "刘宇宁",
                "mbti": "ISFP",
                "comment": "推测为 ISFP，新生代偶像型艺人，感性表达强，形象自然随性，较注重当下体验。"
            }
        ]
        
        created_count = 0
        for vote_data in initial_votes:
            try:
                # Find the celebrity by name
                celebrity = celebrity_service.get_celebrity_by_name(vote_data["name"])
                if not celebrity:
                    print(f"❌ Celebrity not found: {vote_data['name']}")
                    continue
                
                # Create vote
                vote_create = VoteCreate(
                    celebrity_id=celebrity.id,
                    mbti_type=vote_data["mbti"],
                    reason=vote_data["comment"]
                )
                
                vote = vote_service.create_vote(system_user.id, vote_create)
                print(f"✅ Added vote for {celebrity.name}: {vote_data['mbti']} - {vote_data['comment'][:50]}...")
                created_count += 1
                    
            except Exception as e:
                print(f"❌ Error creating vote for {vote_data['name']}: {e}")
        
        print(f"\n🎉 Successfully created {created_count} initial votes!")
        print(f"📝 Initial votes added to database")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🎭 Adding Initial Votes to 16型花名册")
    print("=" * 50)
    
    add_initial_votes()
    
    print("\n" + "=" * 50)
    print("📝 Next steps:")
    print("1. Check the celebrities page: http://localhost:8000/celebrities")
    print("2. View vote statistics: http://localhost:8000/votes/")
    print("3. Test vote endpoints:")
    print("   - GET /votes/ - List all votes")
    print("   - GET /votes/celebrities/{celebrity_id} - Get votes for specific celebrity")
    print("   - GET /votes/mbti-types - Get all MBTI types") 