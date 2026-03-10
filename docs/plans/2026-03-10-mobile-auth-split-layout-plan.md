# Mobile Auth Split Layout Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rework the mobile auth page so login and registration are visible together, with a responsive two-column layout on wide screens and a stacked layout on narrow screens.

**Architecture:** Keep auth API and store behavior unchanged. Refactor `LoginView.vue` so the page renders two separate cards in a responsive grid, with local state split between login and registration flows.

**Tech Stack:** Vue 3, Pinia, TypeScript, Vite

---

### Task 1: Refactor auth page structure

**Files:**
- Modify: `frontend/mobile/src/views/LoginView.vue`

**Step 1:** Replace the single auth card with a responsive grid container.

**Step 2:** Render a dedicated login card and a dedicated registration card.

**Step 3:** Keep password/code switching only inside the login card.

### Task 2: Split local view state

**Files:**
- Modify: `frontend/mobile/src/views/LoginView.vue`

**Step 1:** Split error messages into `loginErrorMessage` and `registerErrorMessage`.

**Step 2:** Split local loading flags into `loginSubmitting` and `registerSubmitting`.

**Step 3:** Keep registration password confirmation validation in the registration submit handler.

### Task 3: Update responsive styling

**Files:**
- Modify: `frontend/mobile/src/views/LoginView.vue`

**Step 1:** Add grid styles for stacked mobile layout by default.

**Step 2:** Add a breakpoint that switches the auth grid to two columns.

**Step 3:** Keep the cards visually aligned with the existing page style.

### Task 4: Verify the change

**Files:**
- Verify: `frontend/mobile/package.json`

**Step 1:** Run `npm run build` in `frontend/mobile`.

**Step 2:** Confirm the app still builds successfully after the layout refactor.
