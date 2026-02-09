# MilenAI Website Usability & Professional Look Assessment

## Executive Summary

MilenAI is an AI-powered clinical intelligence assistant built with Streamlit, targeting nurses, nursing students, and healthcare professionals. The assessment below covers both application files (`MilenAI.py` and `MilenAI_app.py`) and evaluates usability, visual design, code quality, and overall professionalism.

**Overall Rating: 5/10** - Functional prototype with significant room for improvement in visual polish, UX patterns, and code robustness.

---

## 1. VISUAL DESIGN & PROFESSIONAL APPEARANCE

### Strengths
- Clear medical branding with stethoscope emoji and "Clinical Intelligence" title
- Consistent use of healthcare-themed icons throughout
- Medical disclaimer is present in the footer (important for compliance)
- Green accent color (#4CAF50) is appropriate for a healthcare application

### Issues

| Issue | Severity | File | Details |
|-------|----------|------|---------|
| No custom Streamlit theme | Medium | `.streamlit/` | No `config.toml` with `[theme]` section. The app uses Streamlit's default light theme with no brand colors, fonts, or accent customization |
| Heavy emoji usage replaces real design | High | Both files | Emojis (⚕️💬🩺📝⚠️🚀) are used as a substitute for proper icons, badges, or styled components. This gives a casual/amateur feel for a medical tool |
| No favicon or logo asset | Medium | Both files | Only `page_icon="⚕️"` is set in `MilenAI.py`; `MilenAI_app.py` has no `set_page_config()` at all |
| Inline HTML styling | Medium | `MilenAI_app.py` | Raw `<h1>`, `<h4>`, `<h6>` tags with inline styles instead of Streamlit components or proper CSS |
| Inconsistent app naming | Low | Both files | Header says "MilenAI" in one file and "MilenAi" in the other (note capitalization) |
| No responsive design considerations | Medium | Both files | Streamlit handles basic responsiveness, but no testing or adjustment for mobile viewports is evident |
| EKG_rhythm.png and digestive_tract.mp4 are unused | Low | Root dir | Assets exist but are not referenced in either application file |

### Recommendations
1. Add a `.streamlit/config.toml` with a custom theme (primary color, background, text color, font)
2. Replace emoji-heavy headers with clean, styled Streamlit components or a lightweight CSS framework
3. Add `st.set_page_config()` to `MilenAI_app.py` with consistent branding
4. Standardize the app name to "MilenAI" everywhere
5. Incorporate the medical assets (EKG image, video) into the UI where relevant, or remove them

---

## 2. USABILITY & USER EXPERIENCE

### Strengths
- Simple, single-purpose interface focused on asking clinical questions
- Quick questions feature in `MilenAI_app.py` helps users discover what to ask
- Query history provides context of recent interactions
- Chat message bubbles in `MilenAI.py` provide a familiar conversational pattern

### Issues

| Issue | Severity | File | Details |
|-------|----------|------|---------|
| `st.text_input` instead of `st.chat_input` | High | `MilenAI.py` | Uses `st.text_input()` for chat, which lacks the native chat UX (auto-focus, enter-to-submit, bottom-anchored). `st.chat_input()` is the standard for chat apps in Streamlit |
| Separate Submit button required | High | `MilenAI_app.py` | Users must click a small "Submit" button placed in a narrow 20% column. No enter-key submission. This is a significant friction point |
| No loading/spinner indicator | High | `MilenAI.py` | API calls take time but there is no `st.spinner()` or streaming indicator. Users see no feedback while waiting |
| Quick questions section not functional | Critical | `MilenAI_app.py` | The dynamic questions feature (`get_dynamic_questions`) is defined but **never rendered as clickable buttons**. There is a hardcoded test call (`user_input = "What are priority..."`) and a `print()` statement that outputs to the server console, not the UI |
| No conversation context in MilenAI_app.py | High | `MilenAI_app.py` | Messages are sent without conversation history - each query is treated independently with `messages = [{"role": "user", "content": query}]`. The AI has no context of prior exchanges |
| Full message history sent on every request | Medium | `MilenAI.py` | The entire `st.session_state.messages` is sent on every API call. For long sessions this will exceed token limits and increase costs |
| No input validation or character limit | Medium | Both files | Users can submit empty-looking whitespace or extremely long queries with no guardrails |
| No clear chat / reset option | Medium | Both files | No button to start a fresh conversation or clear history |
| Cached responses are never invalidated | Low | `MilenAI_app.py` | The query cache persists for the entire session. If a user asks the same question hoping for a different or updated response, they always get the cached version |
| Query history duplicates on cached responses | Low | `MilenAI_app.py` | `query_history.append(query)` runs even for cached responses, so repeating the same question fills the history with duplicates |

### Recommendations
1. Switch to `st.chat_input()` for the primary input in both files
2. Add `st.spinner("Thinking...")` or use `st.write_stream()` during API calls
3. Implement the quick questions as clickable `st.button()` elements that populate the chat
4. Maintain conversation context in `MilenAI_app.py` by passing message history
5. Add a "Clear Conversation" button
6. Implement token-count awareness for message history truncation

---

## 3. CODE QUALITY & RELIABILITY

### Issues

| Issue | Severity | File | Details |
|-------|----------|------|---------|
| API key retrieval is incorrect | Critical | `MilenAI.py:6` | `st.secrets["general"].get("gsk_6B1g0YIs...")` uses what appears to be the actual API key as the **dictionary key name**, not as a value. This is either a bug or a leaked key fragment in source code |
| Outdated OpenAI SDK usage | High | `MilenAI_app.py` | Uses `openai.ChatCompletion.create()` which is the legacy v0.x API. The `requirements.txt` pins `openai==0.28.0`. The current SDK is v1.x+ with a completely different interface |
| Duplicate import | Low | `MilenAI_app.py:4,108` | `import random` appears twice |
| Debug print statement in production code | Medium | `MilenAI_app.py:159` | `print(quick_questions)` outputs to server logs, not user-facing |
| Hardcoded test code in production | Medium | `MilenAI_app.py:157-159` | Lines 157-159 contain test code (`user_input = "What are priority..."`) that overwrites the user input variable |
| No system prompt | Medium | Both files | Neither file sends a system message to establish the AI's role, tone, or scope. The model responds as a general assistant rather than a specialized clinical educator |
| Generic exception catching | Low | Both files | `except Exception as e` catches all errors including `KeyboardInterrupt`, `SystemExit`, etc. |
| Model name mismatch | Medium | `MilenAI.py:43` | Uses `model="groq/gpt-4-turbo"` - Groq does not host GPT-4 models; this will likely fail. Groq hosts models like `llama3-70b-8192`, `mixtral-8x7b-32768` |
| Unused imports | Low | `MilenAI_app.py` | `pandas` is imported but never used |

### Recommendations
1. Fix the API key retrieval to use a proper secret name (e.g., `st.secrets["general"]["GROQ_API_KEY"]`)
2. Upgrade to `openai>=1.0` and update the SDK calls accordingly
3. Remove duplicate imports, debug prints, and test code
4. Add a system prompt that defines MilenAI's role and boundaries
5. Use the correct Groq model names

---

## 4. INFORMATION ARCHITECTURE

### Issues

| Issue | Severity | Details |
|-------|----------|---------|
| Two separate app files with no clear entry point | High | `MilenAI.py` and `MilenAI_app.py` appear to be competing versions. The devcontainer references a third file (`deepveinseek_app.py`) that does not exist |
| No navigation or multi-page structure | Medium | Everything is on a single page. Streamlit supports multi-page apps natively via a `pages/` directory |
| No onboarding or help text | Medium | New users see a text input with no guidance on what the AI can do, its limitations, or example use cases (quick questions exist but are not rendered) |
| No about/help page | Low | No information about the project, team, or how the AI works |

### Recommendations
1. Consolidate into a single, canonical application file
2. Add a sidebar with navigation, app info, and settings
3. Display quick-start examples prominently for first-time users
4. Reference the correct entry point in devcontainer config

---

## 5. ACCESSIBILITY & COMPLIANCE

### Issues

| Issue | Severity | Details |
|-------|----------|---------|
| `unsafe_allow_html=True` used extensively | Medium | Bypasses Streamlit's XSS protections. While Streamlit sanitizes by default, raw HTML injection opens risk if user-generated content is ever rendered |
| Medical disclaimer is minimal | Medium | A single-line disclaimer may not meet healthcare software compliance standards. Consider a more prominent, always-visible disclaimer |
| No HIPAA or data privacy notice | High | For a healthcare-focused tool, there is no mention of data handling, privacy policy, or whether conversations are stored/transmitted securely |
| No rate limiting | Medium | No protection against excessive API usage or abuse |

### Recommendations
1. Minimize use of `unsafe_allow_html=True`; use Streamlit native components where possible
2. Add a prominent privacy notice about data handling
3. Add a terms-of-use acknowledgment before first interaction
4. Implement basic rate limiting

---

## 6. PERFORMANCE

### Issues

| Issue | Severity | Details |
|-------|----------|---------|
| Blocking API calls with no streaming | Medium | AI responses are fetched synchronously. For long responses, the UI freezes with no feedback. Streamlit supports `st.write_stream()` for progressive rendering |
| No connection pooling or timeout configuration | Low | Default HTTP timeouts apply. Long-running queries could hang indefinitely |
| Session state grows unbounded | Low | Chat history and query cache grow indefinitely during a session |

### Recommendations
1. Implement streaming responses with `st.write_stream()`
2. Set explicit API timeouts
3. Implement session state cleanup for long-running sessions

---

## 7. PRIORITY ACTION ITEMS (Ranked)

| Priority | Action | Impact |
|----------|--------|--------|
| 1 | Fix API key handling and model names so the app actually works | Critical - app is currently broken |
| 2 | Consolidate into one application file, remove test/debug code | High - reduces confusion |
| 3 | Switch to `st.chat_input()` and add `st.spinner()` | High - core UX improvement |
| 4 | Add a system prompt for clinical educator persona | High - defines AI behavior |
| 5 | Implement quick questions as clickable buttons | Medium - feature completion |
| 6 | Add custom Streamlit theme via config.toml | Medium - visual polish |
| 7 | Add privacy notice and enhanced medical disclaimer | Medium - compliance |
| 8 | Upgrade OpenAI SDK to v1.x | Medium - maintainability |
| 9 | Add sidebar with navigation and app info | Low - information architecture |
| 10 | Implement streaming responses | Low - performance polish |

---

*Assessment conducted on 2026-02-09*
