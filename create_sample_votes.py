#!/usr/bin/env python3
"""
Script to create sample votes for testing the voting system
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.services.vote_service import VoteService
from app.services.celebrity_service import CelebrityService
from app.services.auth_service import AuthService
from app.schemas.vote import VoteCreate
from app.database.models import MBTIType, User


def create_sample_votes():
    """Create sample votes for testing"""
    db = SessionLocal()
    try:
        vote_service = VoteService(db)
        celebrity_service = CelebrityService(db)
        auth_service = AuthService(db)

        # Get admin user
        admin_user = (
            db.query(User).filter(User.email == "admin@mbti-roster.com").first()
        )
        if not admin_user:
            print("Admin user not found. Please run create_admin.py first.")
            return

        # Get all celebrities
        celebrities = celebrity_service.get_all_celebrities()
        if not celebrities:
            print(
                "No celebrities found. Please run create_sample_celebrities.py first."
            )
            return

        print(f"Found {len(celebrities)} celebrities to vote for")
        print(f"Using admin user: {admin_user.name} ({admin_user.email})")

        # Sample MBTI types and reasons
        mbti_types = list(MBTIType)
        sample_reasons = [
            "Based on their analytical thinking and strategic approach",
            "Their introverted nature and deep insights",
            "Extroverted personality and natural leadership",
            "Creative and innovative thinking patterns",
            "Strong sense of empathy and understanding",
            "Logical and systematic decision making",
            "Spontaneous and adaptable behavior",
            "Organized and detail-oriented approach",
            "Warm and caring personality",
            "Practical and hands-on problem solving",
        ]

        created_count = 0
        for i, celebrity in enumerate(celebrities):
            try:
                # Create 1-3 votes per celebrity with different MBTI types
                num_votes = min(3, len(mbti_types) - i % 3)  # Vary the number of votes

                for j in range(num_votes):
                    mbti_type = mbti_types[(i + j) % len(mbti_types)]
                    reason = sample_reasons[(i + j) % len(sample_reasons)]

                    vote_data = VoteCreate(
                        celebrity_id=celebrity.id, mbti_type=mbti_type, reason=reason
                    )

                    vote = vote_service.create_vote(admin_user.id, vote_data)
                    print(f"Created vote: {celebrity.name} -> {mbti_type.value}")
                    created_count += 1

            except Exception as e:
                print(f"Error creating vote for {celebrity.name}: {e}")

        print(f"\nSuccessfully created {created_count} votes!")
        print(f"Sample votes added to database")

        # Show some statistics
        print("\nSample Statistics:")
        for celebrity in celebrities[:3]:  # Show stats for first 3 celebrities
            try:
                stats = vote_service.get_celebrity_vote_statistics(celebrity.id)
                print(
                    f"  {celebrity.name}: {stats['total_votes']} votes, Top MBTI: {stats['top_mbti_type']}"
                )
            except Exception as e:
                print(f"  {celebrity.name}: Error getting stats - {e}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating Sample Votes for 16型花名册")
    print("=" * 50)

    create_sample_votes()

    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Start the server: python run_local.py")
    print("2. Go to http://localhost:8000/docs")
    print("3. Test the vote endpoints:")
    print("   - POST /votes/ - Create a new vote")
    print("   - GET /votes/ - List all votes")
    print("   - GET /votes/my-votes - Get current user's votes")
    print("   - GET /votes/statistics/celebrity/{id} - Get celebrity vote stats")
    print("   - GET /votes/statistics/my-stats - Get user vote stats")
    print("   - GET /votes/popular-celebrities - Get popular celebrities by votes")
    print("4. Use admin token for testing")
    print("5. Try creating votes with different MBTI types")
