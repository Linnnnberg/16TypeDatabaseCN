#!/usr/bin/env python3
"""
Script to create sample celebrities for testing the celebrity management system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.services.celebrity_service import CelebrityService
from app.services.auth_service import AuthService
from app.schemas.celebrity import CelebrityCreate

def create_sample_celebrities():
    """Create sample celebrities for testing"""
    db = SessionLocal()
    try:
        celebrity_service = CelebrityService(db)
        
        # Sample celebrities data
        sample_celebrities = [
            {
                "name": "周杰伦",
                "name_en": "Jay Chou",
                "description": "台湾著名歌手、音乐人、演员、导演",
                "image_url": "https://example.com/jay-chou.jpg"
            },
            {
                "name": "刘德华",
                "name_en": "Andy Lau",
                "description": "香港著名演员、歌手、制片人",
                "image_url": "https://example.com/andy-lau.jpg"
            },
            {
                "name": "成龙",
                "name_en": "Jackie Chan",
                "description": "香港著名演员、导演、武术家",
                "image_url": "https://example.com/jackie-chan.jpg"
            },
            {
                "name": "李连杰",
                "name_en": "Jet Li",
                "description": "中国著名演员、武术家",
                "image_url": "https://example.com/jet-li.jpg"
            },
            {
                "name": "周星驰",
                "name_en": "Stephen Chow",
                "description": "香港著名演员、导演、编剧",
                "image_url": "https://example.com/stephen-chow.jpg"
            },
            {
                "name": "张国荣",
                "name_en": "Leslie Cheung",
                "description": "香港著名歌手、演员",
                "image_url": "https://example.com/leslie-cheung.jpg"
            },
            {
                "name": "梅艳芳",
                "name_en": "Anita Mui",
                "description": "香港著名歌手、演员",
                "image_url": "https://example.com/anita-mui.jpg"
            },
            {
                "name": "邓丽君",
                "name_en": "Teresa Teng",
                "description": "台湾著名歌手",
                "image_url": "https://example.com/teresa-teng.jpg"
            },
            {
                "name": "王菲",
                "name_en": "Faye Wong",
                "description": "中国著名歌手、演员",
                "image_url": "https://example.com/faye-wong.jpg"
            },
            {
                "name": "张学友",
                "name_en": "Jacky Cheung",
                "description": "香港著名歌手、演员",
                "image_url": "https://example.com/jacky-cheung.jpg"
            }
        ]
        
        created_count = 0
        for celeb_data in sample_celebrities:
            try:
                celebrity = celebrity_service.create_celebrity(CelebrityCreate(**celeb_data))
                print(f"Created celebrity: {celebrity.name} ({celebrity.name_en})")
                created_count += 1
                
                # Add some tags to celebrities
                if "歌手" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "歌手")
                if "演员" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "演员")
                if "导演" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "导演")
                if "香港" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "香港")
                if "台湾" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "台湾")
                if "中国" in celeb_data["description"]:
                    celebrity_service.add_tag_to_celebrity(celebrity.id, "中国")
                    
            except Exception as e:
                print(f"Error creating {celeb_data['name']}: {e}")
        
        print(f"\nSuccessfully created {created_count} celebrities!")
        print(f"Sample celebrities added to database")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating Sample Celebrities for 16型花名册")
    print("=" * 50)
    
    create_sample_celebrities()
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Start the server: python run_local.py")
    print("2. Go to http://localhost:8000/docs")
    print("3. Test the celebrity endpoints:")
    print("   - GET /celebrities/ - List all celebrities")
    print("   - GET /celebrities/popular - Get popular celebrities")
    print("   - GET /celebrities/tag/歌手 - Get celebrities by tag")
    print("   - POST /celebrities/ - Create new celebrity (admin only)")
    print("4. Use admin token for admin operations") 