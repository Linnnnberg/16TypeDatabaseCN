# TODO List

## Planning Summary

### **Immediate Priorities (This Week)**
- **BUG-001**: Add missing `requests` dependency (30 min)
- **STORY-001**: ✅ **COMPLETED** - Display 16 Type Codes with Chinese Names (4-5 hours)

### **High Priority (Next 2 weeks)**
- **STORY-002**: Make MBTI Type Cards Clickable (2-3 hours)
- **TECH-001**: CI/CD Data Pipeline Separation (4-6 hours)

### **Medium Priority (Next 1-2 months)**
- **STORY-003**: Create MBTI Type Description Pages (6-8 hours)
- **STORY-004**: Basic Admin Panel for Content Management (8-10 hours)
- **STORY-005**: Basic UI Pages for Each Section (12-16 hours)
- **TECH-002**: Separate MBTI Module Architecture (3-4 hours)
- **TECH-003**: API Caching Implementation (2-3 hours)

### **Total Estimated Time for High/Medium Priority**: ~55-65 hours

---

## Current Sprint (Next 2-3 weeks)

### STORY-001: Display 16 Type Codes with Chinese Names on Root Page
**Priority**: High  
**Status**: ✅ **COMPLETED**  
**Estimated Time**: 4-5 hours  
**Completion Date**: January 2025

#### Subtasks:
1. **Create MBTI Type Mapping Data Structure** (1-2 hours)
   - [x] Create `app/data/mbti_types.py` file
   - [x] Define `MBTI_TYPE_MAPPING` dictionary with structure:
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
   - [x] Extract existing Chinese names from `templates/about.html`
   - [x] Add English names for future internationalization
   - [x] Add brief descriptions for each type
   - [x] Create helper functions for accessing the mapping

2. **Create API Endpoints** (1 hour)
   - [x] Create `app/api/mbti.py` with MBTI endpoints
   - [x] Add `GET /api/mbti/types` endpoint with full information
   - [x] Add `GET /api/mbti/types/{type_code}` for specific types
   - [x] Add `GET /api/mbti/types-list` for simple list
   - [x] Add `GET /api/mbti/validate/{type_code}` for validation
   - [x] Add comprehensive error handling and validation

3. **Update Root Page Template** (1-2 hours)
   - [x] Modify `templates/index.html` section (lines 83-120)
   - [x] Replace hardcoded grid with dynamic data from backend
   - [x] Display both 4-letter code and Chinese name
   - [x] Improve visual design:
     - 4-column grid layout (larger cards)
     - Better spacing and typography
     - Responsive design (mobile-friendly)
   - [x] Keep cards non-clickable for now

4. **Update Backend Route** (30 minutes)
   - [x] Modify root page route in `app/main.py`
   - [x] Pass MBTI types data to template
   - [x] Ensure data is properly formatted for template rendering
   - [x] Add error handling for missing data

5. **Add Tests** (1 hour)
   - [x] Add unit tests for `mbti_types.py` mapping
   - [x] Add tests for new API endpoint
   - [x] Add integration tests for root page with MBTI data
   - [x] Update existing tests to use new structure

6. **Update About Page** (30 minutes)
   - [x] Update about page route in `app/main.py`
   - [x] Replace static MBTI types with dynamic data
   - [x] Add hover effects and improved styling
   - [x] Ensure consistent design with homepage

#### Files Created/Modified:
- ✅ `app/data/mbti_types.py` (created)
- ✅ `app/data/__init__.py` (created)
- ✅ `app/api/mbti.py` (created)
- ✅ `app/api/__init__.py` (updated)
- ✅ `templates/index.html` (updated)
- ✅ `templates/about.html` (updated)
- ✅ `app/main.py` (updated)
- ✅ `tests/test_mbti_types.py` (created)
- ✅ `API_DOCUMENTATION.md` (updated)
- ✅ `CHANGELOG.md` (updated)

## Short-term Stories (Next 1-2 months)

### STORY-002: Make MBTI Type Cards Clickable
**Priority**: High  
**Status**: Ready to Start  
**Dependencies**: ✅ STORY-001 (COMPLETED)
**Estimated Time**: 2-3 hours
**Description**: Add click functionality to MBTI type cards on root page and about page

### STORY-003: Create MBTI Type Description Pages
**Priority**: Medium  
**Dependencies**: STORY-001, STORY-002
**Estimated Time**: 6-8 hours
**Description**: Individual pages for each MBTI type with detailed descriptions, strengths, weaknesses, career suggestions, and famous examples

### STORY-004: Basic Admin Panel for Content Management
**Priority**: Medium  
**Dependencies**: STORY-001
**Estimated Time**: 8-10 hours
**Description**: Simple admin interface for managing celebrities, votes, and basic CRUD operations

### STORY-005: Basic UI Pages for Each Section
**Priority**: Medium  
**Dependencies**: TECH-001 (CI/CD improvements)
**Estimated Time**: 12-16 hours
**Description**: Create basic working UI pages for each major section of the application
**Subtasks:**
- [ ] **Celebrities Section UI** (4-5 hours)
  - [ ] Create `templates/celebrities_section.html` with grid layout
  - [ ] Add filtering by MBTI type, profession, region
  - [ ] Display celebrity cards with images, names, top MBTI votes
  - [ ] Add pagination for large lists
- [ ] **Voting Section UI** (3-4 hours)
  - [ ] Create `templates/voting_section.html` with voting interface
  - [ ] Show current user's voting history and limits
  - [ ] Display vote statistics and trends
  - [ ] Add reason input form for votes
- [ ] **Search & Discovery UI** (3-4 hours)
  - [ ] Create `templates/search_section.html` with advanced search
  - [ ] Add filters for MBTI type, tags, profession
  - [ ] Show search results with sorting options
  - [ ] Add "similar celebrities" suggestions
- [ ] **User Profile & Stats UI** (2-3 hours)
  - [ ] Create `templates/profile_section.html` with user dashboard
  - [ ] Display personal voting statistics
  - [ ] Show favorite MBTI types and voting patterns
  - [ ] Add profile editing capabilities

## Medium-term Stories (Next 2-4 months)

### STORY-006: Add Function Stack for Each MBTI Type
**Priority**: Medium  
**Dependencies**: STORY-003
**Estimated Time**: 4-6 hours
**Description**: Display cognitive function stack (Ni, Te, Fi, Se, etc.) for each MBTI type with explanations

### STORY-007: Wikipedia + AI Data Pipeline
**Priority**: Medium  
**Dependencies**: STORY-004, STORY-005
**Estimated Time**: 12-16 hours
**Description**: Automated data collection from Wikipedia with AI enhancement for MBTI analysis

### STORY-008: Enhanced UI with Interactive Features
**Priority**: Medium  
**Dependencies**: STORY-005
**Estimated Time**: 8-12 hours
**Description**: Add interactive features and polish to the basic UI pages
**Subtasks:**
- [ ] **Interactive Charts & Graphs** (3-4 hours)
  - [ ] Add MBTI distribution charts using Chart.js or similar
  - [ ] Create voting trend visualizations
  - [ ] Show user activity heatmaps
- [ ] **Real-time Updates** (2-3 hours)
  - [ ] Add WebSocket support for live vote updates
  - [ ] Implement real-time notifications
  - [ ] Show live voting counters
- [ ] **Advanced Filtering & Sorting** (3-5 hours)
  - [ ] Add multi-select filters
  - [ ] Implement saved search preferences
  - [ ] Add sorting by popularity, date, MBTI type

## Long-term Stories (Future)

### STORY-009: Internationalization Support
**Priority**: Low  
**Dependencies**: STORY-001
**Estimated Time**: 8-10 hours
**Description**: Add multi-language support for English and other languages

### STORY-010: MBTI Type Metadata Enhancement
**Priority**: Low  
**Dependencies**: STORY-003
**Estimated Time**: 6-8 hours
**Description**: Add comprehensive metadata including type percentages, famous examples, relationship compatibility, etc.

### STORY-011: Advanced UI & User Experience
**Priority**: Low  
**Dependencies**: STORY-008
**Estimated Time**: 10-15 hours
**Description**: Advanced UI features and user experience improvements
**Subtasks:**
- [ ] **Mobile App-like Experience** (4-6 hours)
  - [ ] Progressive Web App (PWA) features
  - [ ] Offline functionality for basic features
  - [ ] Touch-optimized interactions
- [ ] **Personalization & Customization** (3-4 hours)
  - [ ] User-customizable dashboards
  - [ ] Theme switching (light/dark mode)
  - [ ] Customizable notification preferences
- [ ] **Accessibility Improvements** (3-5 hours)
  - [ ] Screen reader support
  - [ ] Keyboard navigation
  - [ ] High contrast mode
  - [ ] Font size adjustments

## Technical Tasks

### TECH-001: CI/CD Data Pipeline Separation
**Priority**: High  
**Dependencies**: None
**Estimated Time**: 4-6 hours
**Description**: Separate data management from CI/CD pipeline to improve deployment speed and reliability
**Subtasks:**
- [ ] Exclude actual celebrity/vote data from CI/CD builds
- [ ] Include only data schemas, validation rules, and test fixtures in CI/CD
- [ ] Create separate data deployment pipeline for content updates
- [ ] Implement data validation in CI/CD without importing actual content
- [ ] Add data integrity checks to deployment process

### TECH-002: Separate MBTI Module Architecture
**Priority**: Medium  
**Dependencies**: STORY-001  
**Estimated Time**: 3-4 hours
**Description**: Refactor MBTI-related code into a separate module for better organization and maintainability

### TECH-003: API Caching Implementation
**Priority**: Medium  
**Dependencies**: STORY-001  
**Estimated Time**: 2-3 hours
**Description**: Add caching layer for MBTI type data and other frequently accessed API endpoints

### TECH-004: Performance Optimization
**Priority**: Medium  
**Dependencies**: None
**Estimated Time**: 6-8 hours
**Description**: Optimize database queries, add database indexing, implement connection pooling

### TECH-005: AI-Powered Data Generation Pipeline
**Priority**: Low  
**Dependencies**: STORY-007
**Estimated Time**: 16-20 hours
**Description**: Implement automated data generation using AI for celebrity MBTI types and vote reasons
**Subtasks:**
- [ ] Research AI API integration options (OpenAI, Claude, etc.)
- [ ] Create batch generation scripts for multiple celebrities at once
- [ ] Implement data validation and quality checks for AI-generated content
- [ ] Build Wikipedia + AI enhancement pipeline for factual data
- [ ] Create content moderation tools for AI-generated suggestions

## Bug Fixes

### BUG-001: Add Missing Dependencies
**Priority**: High  
**Status**: Identified  
**Estimated Time**: 30 minutes
**Description**: Add `requests` package to `requirements_minimal.txt` as identified by CI validation

### BUG-002: Fix Import Order Validation
**Priority**: Medium  
**Status**: Identified
**Estimated Time**: 1-2 hours
**Description**: The import order validation in `validate_cicd_rules.py` is too restrictive and causing false positives

## Documentation

### DOC-001: Update API Documentation
**Priority**: Medium  
**Dependencies**: STORY-001
**Estimated Time**: 2-3 hours
**Description**: Update API documentation to include new MBTI endpoints

### DOC-002: Code Comments and Documentation
**Priority**: Medium  
**Dependencies**: STORY-001
**Estimated Time**: 1-2 hours
**Description**: Add comprehensive comments to new MBTI-related code

## UI/UX Improvements

### UI-001: Enhanced MBTI Type Cards Design
**Priority**: Medium  
**Dependencies**: STORY-001
**Estimated Time**: 3-4 hours
**Description**: Improve visual design of MBTI type cards with better colors, animations, and hover effects

### UI-002: Mobile Responsiveness Improvements
**Priority**: Medium  
**Dependencies**: None
**Estimated Time**: 4-6 hours
**Description**: Enhance mobile experience across all pages

### UI-003: Section-Based UI Architecture (Post CI/CD)
**Priority**: High  
**Dependencies**: TECH-001 (CI/CD improvements)
**Estimated Time**: 8-10 hours
**Description**: Design and implement the basic UI structure for each major section
**Subtasks:**
- [ ] **Design System Setup** (2-3 hours)
  - [ ] Create consistent color scheme and typography
  - [ ] Design reusable UI components (cards, buttons, forms)
  - [ ] Establish grid system and spacing standards
- [ ] **Navigation & Layout** (2-3 hours)
  - [ ] Design main navigation structure
  - [ ] Create consistent page layouts
  - [ ] Implement breadcrumb navigation
- [ ] **Responsive Framework** (2-2 hours)
  - [ ] Set up CSS Grid/Flexbox for responsive layouts
  - [ ] Create mobile-first design approach
  - [ ] Implement breakpoint system
- [ ] **Component Library** (2-2 hours)
  - [ ] Build reusable form components
  - [ ] Create data display components (tables, lists, cards)
  - [ ] Implement loading states and error handling

## Code Quality

### QUALITY-001: Test Coverage Enhancement
**Priority**: Medium  
**Dependencies**: STORY-001
**Estimated Time**: 2-3 hours
**Description**: Increase test coverage for new MBTI-related functionality

### QUALITY-002: Code Review and Refactoring
**Priority**: Low  
**Dependencies**: None
**Estimated Time**: 4-6 hours
**Description**: Review existing code for improvements and refactoring opportunities

---

## Progress Tracking

### Completed Stories
- ✅ STORY-001: Basic MBTI application setup
- ✅ STORY-002: User authentication system
- ✅ STORY-003: Celebrity database and voting
- ✅ STORY-004: Search and filtering functionality
- ✅ STORY-005: CI/CD pipeline and code quality

### In Progress
- STORY-001: Display 16 Type Codes with Chinese Names on Root Page

### Next Up
- STORY-002: Make MBTI Type Cards Clickable
- STORY-003: Create MBTI Type Description Pages
- STORY-004: Cognitive Function Stack Scoring System (MBTI Test)
- TECH-001: CI/CD Data Pipeline Separation
- STORY-005: Basic UI Pages for Each Section (after CI/CD)

### STORY-004: Cognitive Function Stack Scoring System (MBTI Test)
**Status**: Ready to Start  
**Priority**: High  
**Dependencies**: STORY-001 (MBTI Types Display)  
**Effort Estimate**: 3-4 weeks  

**Description**: Implement a comprehensive MBTI test system that measures cognitive functions through real-world scenario questions without revealing function types to users.

**Subtasks**:
1. [ ] Create data models for questions and user responses
2. [ ] Implement question bank management system
3. [ ] Create scoring algorithm and calculation engine
4. [ ] Build test interface with randomized question order
5. [ ] Implement result processing and MBTI type mapping
6. [ ] Create results display with function stack analysis
7. [ ] Add celebrity comparison and growth tips
8. [ ] Write comprehensive tests for all components
9. [ ] Update API documentation

**Files to Create/Modify**:
- `app/models/question.py` - Question data model
- `app/models/user_response.py` - User response data model
- `app/services/test_service.py` - Test logic and scoring
- `app/api/test.py` - Test API endpoints
- `app/data/questions.py` - Question bank data
- `templates/test.html` - Test interface
- `templates/results.html` - Results display
- `tests/test_mbti_test.py` - Test coverage
- `docs/MBTI_TEST_PRD.md` - Product Requirements Document

---

**Note**: This TODO list is organized by priority and dependencies. Stories marked as "Future" are planned but not yet scheduled for implementation. 