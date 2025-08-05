
# 🧩 MVP Frontend Plan – Simple Setup (FastAPI + Jinja2 + Tailwind)

---

## 1. Tech Stack
- HTML + Jinja2 (built into FastAPI)
- Tailwind CSS (or basic custom CSS)
- Vanilla JavaScript (or Alpine.js for interactivity)
- Use `fetch()` for API calls

---

## 2. Folder Structure
```
/templates/
  - base.html         (layout shell: nav, footer)
  - index.html        (homepage)
  - test.html         (MBTI test form)
  - result.html       (test result display)
  - celebrities.html  (celebrity directory)
/static/
  /css/
    - style.css       (or Tailwind)
  /js/
    - main.js         (optional interactivity)
```

---

## 3. Pages to Build

- `index.html`: Homepage  
  - Hero section  
  - Links to: Celebrities | What is MBTI | Explore Yourself | Let's Chat  

- `test.html`: Simple MBTI test form  
  - Radio buttons or Likert scale  
  - Submit → redirect to result  

- `result.html`: Display test results  
  - MBTI type  
  - Function stack  
  - Matched celebrities  

- `celebrities.html`: Celebrity directory  
  - Grid of cards  
  - Filter by MBTI  
  - Show name, type, photo  

- `login.html` / `signup.html`: (optional)  

---

## 4. Connect Backend API to Templates (Example)

```python
@app.get("/celebrities", response_class=HTMLResponse)
async def get_celebrities(request: Request):
    celebs = await celeb_service.get_all_celebrities()
    return templates.TemplateResponse("celebrities.html", {"request": request, "celebrities": celebs})
```

In `celebrities.html`:
```html
{% for celeb in celebrities %}
  <div>
    <img src="{{ celeb.image_url }}">
    <h3>{{ celeb.name }}</h3>
    <p>{{ celeb.mbti_type }}</p>
  </div>
{% endfor %}
```

---

## 5. Style Tips
- Use a warm color palette (from your Figma)
- Rounded corners, soft shadows, comfortable padding
- Tailwind utility classes recommended for fast layout
- Mobile-first layout

---

## 6. Minimum Features
- Static homepage
- Basic MBTI test
- Result page with sample data
- Celeb list with API data
- Nice layout and fonts
