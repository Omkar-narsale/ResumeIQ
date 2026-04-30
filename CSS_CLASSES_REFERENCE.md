# 🎨 Premium UI - CSS Classes & Components Reference

## Available CSS Classes

### Container Classes

#### `.card-container`
```css
- White background
- 12px border radius
- 24px padding
- 1px border (#E2E8F0)
- Shadow: 0 2px 8px rgba(0,0,0,0.08)
- Hover shadow: 0 8px 16px rgba(0,0,0,0.1)
- Use: Wrap any major section
```

#### `.header-container`
```css
- Gradient: #2E86AB → #A23B72
- 40px padding
- 16px border radius
- White text
- Box shadow
- Use: Main page header
```

#### `.upload-box`
```css
- Gradient background: #F0F9FF → #F5F3FF
- 2px dashed border (#2E86AB)
- 12px border radius
- 32px padding
- Center text
- Hover: Gradient darkens, border changes
- Use: File upload sections
```

### Feedback Box Classes

#### `.feedback-success`
```css
- Background: #ECFDF5 (Light green)
- Left border: 4px solid #06A77D (Green)
- 16px padding
- Use: Success messages
```

#### `.feedback-warning`
```css
- Background: #FEF3C7 (Light orange)
- Left border: 4px solid #F78C6B (Orange)
- 16px padding
- Use: Warning messages
```

#### `.feedback-info`
```css
- Background: #F0F9FF (Light blue)
- Left border: 4px solid #2E86AB (Blue)
- 16px padding
- Use: Info messages
```

#### `.feedback-highlight`
```css
- Background: #F8FAFC (Light gray)
- Left border: 4px solid #2E86AB (Blue)
- 16px padding
- Use: Important results/highlights
```

### Status Classes

#### `.status-panel`
```css
- Gradient: #F0F9FF → #ECFDF5
- 16px padding
- 12px border radius
- Border: 1px #E2E8F0
- Use: Status indicators
```

#### `.status-badge` + `.status-active`
```css
- Background: #ECFDF5
- Color: #06A77D
- Padding: 6px 12px
- Border radius: 6px
- Font size: 0.9em
- Font weight: 600
- Use: Active status indicator
```

#### `.status-badge` + `.status-inactive`
```css
- Background: #F3F4F6
- Color: #6B7280
- Padding: 6px 12px
- Border radius: 6px
- Font size: 0.9em
- Font weight: 600
- Use: Inactive status indicator
```

### Typography Classes

#### `.header-title`
```css
- Font size: 2.5em
- Font weight: 700
- Color: white
- Letter spacing: -0.5px
- Use: Main page title
```

#### `.header-subtitle`
```css
- Font size: 1.1em
- Font weight: 400
- Color: white (95% opacity)
- Letter spacing: 0.3px
- Use: Subtitle under header
```

#### `.section-header`
```css
- Font size: 1.5em
- Font weight: 700
- Color: #1E293B (Dark)
- Margin: 24px 0 16px 0
- Border bottom: 2px #E2E8F0
- Use: Feature section titles
```

#### `.nav-title`
```css
- Font size: 1.1em
- Font weight: 700
- Color: #2E86AB (Primary blue)
- Margin: 16px 0 12px 0
- Text transform: uppercase
- Letter spacing: 0.5px
- Use: Navigation section titles
```

### Metric Classes

#### `.metric-card`
```css
- Background: Gradient #F0F9FF → #F5F3FF
- Border radius: 12px
- Padding: 16px
- Text align: center
- Border: 1px #E2E8F0
- Use: Metric display (count, score)
```

#### `.metric-value`
```css
- Font size: 2em
- Font weight: 700
- Color: #2E86AB (Primary)
- Use: Large numeric values
```

#### `.metric-label`
```css
- Font size: 0.9em
- Color: #64748B (Gray)
- Margin top: 4px
- Use: Labels below metrics
```

### Progress Classes

#### `.progress-excellent`
```css
- Gradient: #06A77D → #059669 (Green)
- Use: 80-100% scores
```

#### `.progress-good`
```css
- Gradient: #3B82F6 → #2563EB (Blue)
- Use: 60-80% scores
```

#### `.progress-fair`
```css
- Gradient: #F78C6B → #F59E0B (Orange)
- Use: 40-60% scores
```

#### `.progress-poor`
```css
- Gradient: #D62828 → #B91C1C (Red)
- Use: 0-40% scores
```

### Button Classes

#### `.stButton > button`
```css
- Gradient: #2E86AB → #1E5A8E
- Color: white
- Border radius: 8px
- Padding: 12px 24px
- Font weight: 600
- Hover: +shadow, -2px translateY
- Use: All buttons (auto-applied)
```

---

## Color Palette Reference

```css
Primary Color:      #2E86AB    /* Professional Blue */
Secondary Color:    #A23B72   /* Accent Purple */
Success Color:      #06A77D   /* Green */
Warning Color:      #F78C6B   /* Orange */
Danger Color:       #D62828   /* Red */
Background Light:   #F8FAFC   /* Very Light Gray */
Text Dark:          #1E293B   /* Dark Slate */
Border Color:       #E2E8F0   /* Light Gray */
```

---

## Helper Functions Reference

### `get_score_color(score)`
Returns color based on score value:
```python
get_score_color(90)  # Returns "#06A77D" (green)
get_score_color(75)  # Returns "#3B82F6" (blue)
get_score_color(55)  # Returns "#F78C6B" (orange)
get_score_color(25)  # Returns "#D62828" (red)
```

### `render_card(title, content_func, icon)`
Renders a card container with optional title and content:
```python
def my_content():
    st.write("Card content here")

render_card("My Section", my_content, "📊")
```

### `render_score_display(score, total)`
Displays score with color-coded progress bar:
```python
render_score_display(85, 100)  # Shows 85/100 with green bar
render_score_display(7, 10)    # Shows 7/10 with blue bar
```

### `show_success_box(title, content)`
Green success feedback box:
```python
show_success_box("Success", "Your resume was uploaded successfully!")
```

### `show_warning_box(title, content)`
Orange warning feedback box:
```python
show_warning_box("Error", "Please enter a valid job description")
```

### `show_info_box(title, content)`
Blue info feedback box:
```python
show_info_box("Tip", "Upload a resume to enable this feature")
```

### `show_highlight_box(content, title)`
Gray highlight feedback box:
```python
show_highlight_box("Important information", "Score Explanation")
```

---

## CSS Variables Available

Access in custom CSS using:
```css
var(--primary-color)
var(--secondary-color)
var(--success-color)
var(--warning-color)
var(--danger-color)
var(--bg-light)
var(--text-dark)
var(--border-color)
```

---

## Common Usage Patterns

### Pattern 1: Card with Content
```python
st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">📊 My Section</h2>', unsafe_allow_html=True)
# Your content here
st.markdown('</div>', unsafe_allow_html=True)
```

### Pattern 2: Status Display
```python
if condition:
    st.markdown('<div class="status-panel"><span class="status-badge status-active">✅ Active</span></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-panel"><span class="status-badge status-inactive">❌ Inactive</span></div>', unsafe_allow_html=True)
```

### Pattern 3: Score Display
```python
render_score_display(score_value, total_value)
```

### Pattern 4: Success Message
```python
show_success_box("Title", "Your message here")
```

### Pattern 5: Upload Box
```python
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
st.markdown("<h4>📤 Upload Section</h4>", unsafe_allow_html=True)
# Upload widget here
st.markdown('</div>', unsafe_allow_html=True)
```

---

## Responsive Design Notes

- Uses Streamlit's native `st.columns()` for responsive layouts
- Card styling adapts to container width
- Typography scales for readability
- Tested on desktop and tablet sizes
- Mobile optimization handled by Streamlit

---

## Dark/Light Theme Compatibility

- CSS uses explicit colors (not theme-dependent)
- Works well in both Streamlit light and dark themes
- Gradients are visible in both modes
- Contrast meets WCAG AA standards

---

## Performance Notes

- Minimal CSS (~400 lines)
- No heavy animations
- Smooth transitions (0.3s)
- No external dependencies
- Fast rendering

---

## Accessibility

- ✓ Color contrasts meet WCAG standards
- ✓ Icons accompany text
- ✓ Clear visual hierarchy
- ✓ Labels on all inputs
- ✓ Meaningful button text

---

## Extension Guide

To add new styled cards:

```python
# 1. Create card wrapper
st.markdown('<div class="card-container">', unsafe_allow_html=True)

# 2. Add header
st.markdown('<h2 class="section-header">📈 My New Feature</h2>', unsafe_allow_html=True)

# 3. Add content
st.write("Your content here")

# 4. Close card
st.markdown('</div>', unsafe_allow_html=True)
```

---

**All classes are production-ready and follow modern web design standards.**
