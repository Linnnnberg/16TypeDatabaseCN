# TODO List

## 🚀 Current Sprint

### STORY-006: Display 16 Type Codes with Chinese Names on Root Page
**Priority**: High  
**Status**: Ready to Start  
**Estimated Time**: 4-5 hours

#### Subtasks:
1. **Create MBTI Type Mapping Data Structure** (1-2 hours)
   - [ ] Create `app/data/mbti_types.py` file
   - [ ] Define `MBTI_TYPE_MAPPING` dictionary with structure:
     ```python
     MBTI_TYPE_MAPPING = {
         "INTJ": {
             "chinese": "建筑师",
             "english": "Architect",
             "description": "富有想象力和战略性的思考者"
         },
         # ... all 16 types
     }
     ```
   - [ ] Extract existing Chinese names from `templates/about.html`
   - [ ] Add English names for future internationalization
   - [ ] Add brief descriptions for each type
   - [ ] Create helper functions for accessing the mapping

2. **Update Database Models** (30 minutes)
   - [ ] Import MBTI mapping in `app/database/models.py`
   - [ ] Add helper methods to `MBTIType` enum:
     - `get_chinese_name()`
     - `get_english_name()`
     - `get_description()`
     - `get_all_types_with_names()`
   - [ ] Ensure backward compatibility with existing code

3. **Create API Endpoint for MBTI Types** (1 hour)
   - [ ] Add new endpoint in `app/api/search.py` or create new `app/api/mbti.py`
   - [ ] Endpoint: `GET /api/mbti-types` with full information
   - [ ] Return structure:
     ```json
     {
       "types": [
         {
           "code": "INTJ",
           "chinese_name": "建筑师",
           "english_name": "Architect",
           "description": "富有想象力和战略性的思考者"
         }
       ],
       "total": 16
     }
     ```
   - [ ] Add API documentation

4. **Update Root Page Template** (1-2 hours)
   - [ ] Modify `templates/index.html` section (lines 83-120)
   - [ ] Replace hardcoded grid with dynamic data from backend
   - [ ] Display both 4-letter code and Chinese name
   - [ ] Improve visual design:
     - 4-column grid layout (larger cards)
     - Better spacing and typography
     - Responsive design (mobile-friendly)
   - [ ] Keep cards non-clickable for now

5. **Update Backend Route** (30 minutes)
   - [ ] Modify root page route in `app/main.py`
   - [ ] Pass MBTI types data to template
   - [ ] Ensure data is properly formatted for template rendering
   - [ ] Add error handling for missing data

6. **Add Tests** (1 hour)
   - [ ] Add unit tests for `mbti_types.py` mapping
   - [ ] Add tests for new API endpoint
   - [ ] Add integration tests for root page with MBTI data
   - [ ] Update existing tests to use new structure

#### Files to Create/Modify:
- `app/data/mbti_types.py` (new)
- `app/data/__init__.py` (new)
- `app/database/models.py`
- `app/api/mbti.py` (new)
- `app/api/__init__.py`
- `templates/index.html`
- `app/main.py`
- `tests/test_mbti_types.py` (new)

## 📋 Future Stories

### STORY-007: Make MBTI Type Cards Clickable
**Priority**: Medium  
**Dependencies**: STORY-006
**Description**: Add click functionality to MBTI type cards on root page

### STORY-008: Create MBTI Type Description Pages
**Priority**: Medium  
**Dependencies**: STORY-006, STORY-007
**Description**: Individual pages for each MBTI type with detailed descriptions, strengths, weaknesses, career suggestions, and famous examples

### STORY-009: Add Function Stack for Each MBTI Type
**Priority**: Medium  
**Dependencies**: STORY-008
**Description**: Display cognitive function stack (Ni, Te, Fi, Se, etc.) for each MBTI type with explanations

### STORY-010: Internationalization Support
**Priority**: Low  
**Dependencies**: STORY-006
**Description**: Add multi-language support for English and other languages

### STORY-011: MBTI Type Metadata Enhancement
**Priority**: Low  
**Dependencies**: STORY-008
**Description**: Add comprehensive metadata including type percentages, famous examples, relationship compatibility, etc.

## 🔧 Technical Tasks

### TECH-001: Separate MBTI Module Architecture
**Priority**: Low  
**Dependencies**: STORY-006
**Description**: Refactor MBTI-related code into a separate module for better organization and maintainability

### TECH-002: API Caching Implementation
**Priority**: Low  
**Dependencies**: STORY-006
**Description**: Add caching layer for MBTI type data and other frequently accessed API endpoints

### TECH-003: Performance Optimization
**Priority**: Low  
**Description**: Optimize database queries, add database indexing, implement connection pooling

## 🐛 Bug Fixes

### BUG-001: Fix Import Order Validation
**Priority**: Low  
**Status**: Identified
**Description**: The import order validation in `validate_cicd_rules.py` is too restrictive and causing false positives

### BUG-002: Add Missing Dependencies
**Priority**: Low  
**Status**: Identified  
**Description**: Add `requests` package to `requirements_minimal.txt` as identified by CI validation

## 📚 Documentation

### DOC-001: Update API Documentation
**Priority**: Low  
**Dependencies**: STORY-006
**Description**: Update API documentation to include new MBTI endpoints

### DOC-002: Code Comments and Documentation
**Priority**: Low  
**Dependencies**: STORY-006
**Description**: Add comprehensive comments to new MBTI-related code

## 🎨 UI/UX Improvements

### UI-001: Enhanced MBTI Type Cards Design
**Priority**: Low  
**Dependencies**: STORY-006
**Description**: Improve visual design of MBTI type cards with better colors, animations, and hover effects

### UI-002: Mobile Responsiveness Improvements
**Priority**: Low  
**Description**: Enhance mobile experience across all pages

## 🔍 Code Quality

### QUALITY-001: Code Review and Refactoring
**Priority**: Low  
**Description**: Review existing code for improvements and refactoring opportunities

### QUALITY-002: Test Coverage Enhancement
**Priority**: Low  
**Dependencies**: STORY-006
**Description**: Increase test coverage for new MBTI-related functionality

---

## 📊 Progress Tracking

### Completed Stories
- ✅ STORY-001: Basic MBTI application setup
- ✅ STORY-002: User authentication system
- ✅ STORY-003: Celebrity database and voting
- ✅ STORY-004: Search and filtering functionality
- ✅ STORY-005: CI/CD pipeline and code quality

### In Progress
- 🔄 STORY-006: Display 16 Type Codes with Chinese Names on Root Page

### Next Up
- 📋 STORY-007: Make MBTI Type Cards Clickable
- 📋 STORY-008: Create MBTI Type Description Pages

---

**Note**: This TODO list is organized by priority and dependencies. Stories marked as "Future" are planned but not yet scheduled for implementation. 