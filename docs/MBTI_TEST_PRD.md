# Feature: Cognitive Function Stack Scoring System (Hidden Mapping)

## Purpose
To measure a user's dominant and auxiliary cognitive functions through a series of real-world scenario questions, without explicitly revealing the function type (Ni, Ne, etc.) to the user. This reduces bias and encourages honest, intuitive answers.

---

## Functional Overview
1. **Question Bank**
   - Each question is derived from the *Function Stack Questionnaire* but reworded with real-world scenarios.
   - Questions are **randomized** in presentation order.
   - The **function type mapping** (e.g., "This question maps to Ni") is stored internally and hidden from the user.

2. **Scoring Mechanism**
   - Each question is linked to **exactly one cognitive function**.
   - Users respond on a **5-point Likert scale**:
     1 = Not at all  
     2 = Not completely agree  
     3 = Not sure  
     4 = Somewhat agree  
     5 = Strongly agree
   - Each selected score is **added directly** to that function's cumulative score.

3. **End Calculation**
   - After all questions are answered, the system sums scores for each of the eight cognitive functions:
     - **Ni, Ne, Si, Se, Ti, Te, Fi, Fe**
   - The **top 4 functions** with the highest scores are returned for the user's profile.

4. **Result Mapping**
   - The 4 highest-scored functions can be used to:
     - Suggest likely MBTI type(s).
     - Show dominant–auxiliary–tertiary–inferior stack order.
     - Offer **growth tips** and **celebrity comparisons**.

---

## Data Model

### Question Entity
| Field              | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| id                 | String   | Unique identifier (e.g., "Ni_1")         |
| text               | String   | Question text (real-world scenario)      |
| function_type      | Enum     | Ni, Ne, Si, Se, Ti, Te, Fi, Fe (hidden)  |
| order              | Integer  | Display order (randomized per session)   |

### User Response Entity
| Field              | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| user_id            | UUID     | Linked to user account                   |
| question_id        | String   | Linked to question entity                |
| score              | Integer  | 1–5                                      |
| function_type      | Enum     | Stored internally for scoring            |
| created_at         | DateTime | When the response was recorded           |

### Test Session Entity
| Field              | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| id                 | UUID     | Unique session identifier                |
| user_id            | UUID     | Linked to user account                   |
| started_at         | DateTime | When the test was started                |
| completed_at       | DateTime | When the test was completed              |
| total_score        | Integer  | Sum of all question scores               |
| function_scores    | JSON     | Individual function scores               |
| mbti_suggestion    | String   | Suggested MBTI type based on results    |

---

## Workflow
1. **Question Presentation**
   - Backend retrieves all questions, shuffles them, and sends them to the frontend without function_type.
2. **User Response**
   - User selects a score from 1–5.
3. **Scoring**
   - Backend adds score to the associated function's total (hidden mapping).
4. **Completion**
   - After last question, backend sorts functions by total score.
   - Returns the top 4 functions (and optionally MBTI type suggestion).

---

## Example
**Q:** "You walk into a meeting and quickly sense the unspoken mood in the room, adjusting your tone accordingly." *(maps internally to Fe)*  
- User selects "5 – Strongly agree" → Fe score += 5.

---

## Edge Cases
- **Skipped Question:** Default to 0 points.
- **Ties:** Apply tie-break rules (e.g., use total variance, compare against secondary responses).
- **Short Tests:** If user quits early, partial results can be shown with disclaimer.

---

## Security/Integrity
- Mapping file is stored server-side, not exposed via API.
- API response contains only question text and ID.
- Score processing is done server-side to prevent manipulation.

---

## Technical Implementation

### API Endpoints
- `GET /api/test/questions` - Get randomized questions (without function_type)
- `POST /api/test/start` - Start a new test session
- `POST /api/test/answer` - Submit answer for a question
- `POST /api/test/complete` - Complete test and get results
- `GET /api/test/results/{session_id}` - Get test results

### Database Schema
```sql
-- Questions table
CREATE TABLE questions (
    id VARCHAR(10) PRIMARY KEY,
    text TEXT NOT NULL,
    function_type VARCHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User responses table
CREATE TABLE user_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    question_id VARCHAR(10) REFERENCES questions(id),
    score INTEGER CHECK (score >= 1 AND score <= 5),
    function_type VARCHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test sessions table
CREATE TABLE test_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_score INTEGER DEFAULT 0,
    function_scores JSONB,
    mbti_suggestion VARCHAR(4)
);
```

### Scoring Algorithm
```python
def calculate_function_scores(responses):
    """Calculate scores for each cognitive function"""
    function_scores = {
        'Ni': 0, 'Ne': 0, 'Si': 0, 'Se': 0,
        'Ti': 0, 'Te': 0, 'Fi': 0, 'Fe': 0
    }
    
    for response in responses:
        function_type = response.function_type
        score = response.score
        function_scores[function_type] += score
    
    return function_scores

def get_top_functions(function_scores, top_n=4):
    """Get top N functions by score"""
    sorted_functions = sorted(
        function_scores.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    return sorted_functions[:top_n]

def suggest_mbti_type(function_scores):
    """Suggest MBTI type based on function scores"""
    # Implementation logic for MBTI type suggestion
    # Based on dominant functions and their order
    pass
```

---

## User Experience

### Test Interface
- Clean, distraction-free design
- Progress indicator (X of Y questions)
- Clear question text with easy-to-use 5-point scale
- Option to go back and change previous answers
- Save progress functionality

### Results Display
- Visual representation of function scores
- MBTI type suggestion with confidence level
- Function stack analysis (dominant → inferior)
- Personalized growth recommendations
- Celebrity comparisons with similar profiles

---

## Success Metrics
- **Completion Rate**: Percentage of users who complete the full test
- **Accuracy**: Correlation between test results and user self-assessment
- **User Satisfaction**: Feedback scores on test experience
- **Retention**: Users returning to retake or share results

---

## Future Enhancements
- **Adaptive Testing**: Adjust question difficulty based on responses
- **Result History**: Track changes in cognitive function scores over time
- **Social Features**: Share results and compare with friends
- **Detailed Analysis**: Deep dive into specific function characteristics
- **Mobile App**: Native mobile testing experience

---

## Dependencies
- User authentication system (existing)
- Database infrastructure (existing)
- Frontend framework (FastAPI + Jinja2 + Tailwind CSS)
- Question bank data (Questionaire Mapping.json)

---

## Risk Assessment
- **Low Risk**: Core functionality is straightforward to implement
- **Medium Risk**: MBTI type mapping algorithm complexity
- **Low Risk**: User experience and interface design
- **Medium Risk**: Data integrity and scoring accuracy

---

## Acceptance Criteria
- [ ] Users can complete the full test without seeing function types
- [ ] Scoring algorithm correctly calculates function scores
- [ ] Results accurately reflect user responses
- [ ] Test interface is intuitive and responsive
- [ ] All edge cases are handled gracefully
- [ ] Comprehensive test coverage for all components
- [ ] Performance meets requirements (<2s response time)
- [ ] Mobile-responsive design
