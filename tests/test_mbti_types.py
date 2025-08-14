"""
Tests for MBTI types functionality
"""

import pytest
from app.data.mbti_types import (
    get_mbti_type_info,
    get_chinese_name,
    get_english_name,
    get_description,
    get_all_types,
    get_all_types_with_info,
    validate_mbti_type,
)


class TestMBTITypes:
    """Test MBTI types functionality"""

    def test_get_mbti_type_info_valid(self):
        """Test getting info for valid MBTI type"""
        info = get_mbti_type_info("INTJ")
        assert info is not None
        assert info["chinese"] == "建筑师"
        assert info["english"] == "Architect"
        assert "富有想象力和战略性的思考者" in info["description"]

    def test_get_mbti_type_info_invalid(self):
        """Test getting info for invalid MBTI type"""
        info = get_mbti_type_info("INVALID")
        assert info is None

    def test_get_chinese_name(self):
        """Test getting Chinese name"""
        assert get_chinese_name("INTJ") == "建筑师"
        assert get_chinese_name("ENFP") == "竞选者"
        assert get_chinese_name("INVALID") is None

    def test_get_english_name(self):
        """Test getting English name"""
        assert get_english_name("INTJ") == "Architect"
        assert get_english_name("ENFP") == "Campaigner"
        assert get_english_name("INVALID") is None

    def test_get_description(self):
        """Test getting description"""
        description = get_description("INTJ")
        assert description is not None
        assert "富有想象力和战略性的思考者" in description
        assert get_description("INVALID") is None

    def test_get_all_types(self):
        """Test getting all type codes"""
        types = get_all_types()
        assert len(types) == 16
        assert "INTJ" in types
        assert "ENFP" in types
        assert "ISTJ" in types
        assert "ESFP" in types

    def test_get_all_types_with_info(self):
        """Test getting all types with full information"""
        types_info = get_all_types_with_info()
        assert len(types_info) == 16

        # Check structure of first item
        first_type = types_info[0]
        assert "code" in first_type
        assert "chinese_name" in first_type
        assert "english_name" in first_type
        assert "description" in first_type

        # Check that all types are present
        type_codes = [t["code"] for t in types_info]
        assert "INTJ" in type_codes
        assert "ENFP" in type_codes

    def test_validate_mbti_type_valid(self):
        """Test validating valid MBTI types"""
        assert validate_mbti_type("INTJ") is True
        assert validate_mbti_type("ENFP") is True
        assert validate_mbti_type("intj") is True  # Case insensitive
        assert validate_mbti_type("ENFP") is True

    def test_validate_mbti_type_invalid(self):
        """Test validating invalid MBTI types"""
        assert validate_mbti_type("INVALID") is False
        assert validate_mbti_type("") is False
        assert validate_mbti_type("ABC") is False

    def test_all_16_types_present(self):
        """Test that all 16 MBTI types are present"""
        expected_types = [
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

        actual_types = get_all_types()
        for expected_type in expected_types:
            assert expected_type in actual_types

        assert len(actual_types) == 16

    def test_type_info_completeness(self):
        """Test that all types have complete information"""
        types_info = get_all_types_with_info()

        for type_info in types_info:
            assert type_info["code"] is not None
            assert type_info["chinese_name"] is not None
            assert type_info["english_name"] is not None
            assert type_info["description"] is not None

            # Check that strings are not empty
            assert len(type_info["code"]) > 0
            assert len(type_info["chinese_name"]) > 0
            assert len(type_info["english_name"]) > 0
            assert len(type_info["description"]) > 0
