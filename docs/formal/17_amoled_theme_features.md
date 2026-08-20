# UI Enhancement — AMOLED Black Theme & Feature Additions

Project: Westminster Business License Eligibility & Pathway Assistant (WBLEPA)
Location: src/ui/web/ (index.html, styles.css, app.js)

## Goal
Building on the previous chat-interface redesign (16_ui_chat_enhancement.md), 
convert the color scheme to true AMOLED black and add a handful of polished, 
lightweight interactive features. Keep this scoped entirely to 
src/ui/web/ — no backend/API changes.

If 16_ui_chat_enhancement.md has not been implemented yet, implement both 
together in the same pass.

## 1. AMOLED Black Theme

- Change the primary background color to true black (#000000), not dark 
  gray, so it looks correct and saves battery on OLED phone screens
- Keep existing accent colors (green, teal/blue highlights) for buttons, 
  links, and category cards — they should pop more against true black
- Message bubbles should use a very subtle off-black/dark gray (e.g., 
  #0d0d0d to #121212) so they're distinguishable from the pure black 
  background without breaking the AMOLED effect
- Ensure text contrast remains fully readable (light gray/white text, 
  WCAG AA minimum contrast ratio)
- Update any card borders/dividers to thin, subtle gray lines (e.g., 
  rgba(255,255,255,0.08)) so sections are visually separated without harsh 
  white borders

## 2. Feature Additions (pick lightweight, high-impact ones)

Implement the following:

1. **Copy answer button** — small icon button on each AI response bubble 
   that copies the answer text to clipboard, with a brief "Copied!" toast 
   confirmation
2. **Dark-mode toggle is unnecessary (already all-dark) — skip this**
3. **Suggested follow-up questions** — after each AI answer, show 2-3 small 
   clickable "chip" buttons with relevant follow-up questions (can be simple 
   static suggestions per category, e.g., after a home-business answer, 
   suggest "What permits do I need?" or "How much does it cost?")
4. **Message timestamp** — small, subtle timestamp (e.g., "2:34 PM") under 
   each message bubble
5. **Smooth scroll-to-bottom button** — a small floating button that appears 
   when the user has scrolled up in the chat history, letting them jump back 
   to the latest message
6. **Subtle haptic-style micro-interaction** — button press animations (scale 
   down slightly on tap) for a more native-app feel on mobile
7. **Category cards get a subtle glow/highlight on tap** before starting a 
   conversation from that category

Do not implement all of these if it risks bloating the page — prioritize 
items 1, 3, 4, and 5 as the most valuable; items 2, 6, 7 are nice-to-haves 
if time allows.

## 3. Technical Constraints
- Stay vanilla HTML/CSS/JavaScript, no frameworks, no build step
- No heavy external libraries — clipboard copy and toast notifications can be 
  done in a few lines of native JS
- Maintain full mobile responsiveness
- Test locally via `npx serve src/ui/web` before pushing

## 4. Verification Before Reporting Done
- Confirm AMOLED black renders correctly and text remains readable
- Confirm each implemented feature works with a real test question against 
  the live Render backend (not mocked data)
- Take a screenshot of the local preview showing the new theme and at least 
  one new feature in action

## 5. Deploy
```
git add src/ui/web/
git commit -m "Enhance: AMOLED black theme and chat feature additions"
git push
```
Wait ~30-60 seconds for Vercel auto-deploy, then verify:
```
curl -I https://westminster-license-assistant.vercel.app
```
Confirm HTTP 200. Then manually open the live URL in a browser and confirm 
the black theme and new features actually render correctly in production, 
not just locally.

Do not report this as complete without confirming the live redeployed site 
actually shows the AMOLED theme and new features working, with real backend 
answers.
