# Mobile Registration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a registration flow to the mobile login page that creates an account, automatically logs the user in, and redirects to the home page.

**Architecture:** Keep the change inside the existing mobile auth flow. Add a register API method, expose a register action in the auth store that chains register plus password login, and extend the existing `LoginView.vue` tabbed form with a registration mode.

**Tech Stack:** Vue 3, Pinia, TypeScript, Vite

---

### Task 1: Extend mobile auth data layer

**Files:**
- Modify: `frontend/mobile/src/api/auth.ts`
- Modify: `frontend/mobile/src/stores/auth.ts`

**Step 1:** Add a typed register request function for `POST /api/auth/register`.

**Step 2:** Add a store action that calls register, then immediately calls password login to persist token and user info.

**Step 3:** Keep optional fields (`phone`, `email`) omitted when empty so the payload stays aligned with backend expectations.

### Task 2: Add registration mode to the login screen

**Files:**
- Modify: `frontend/mobile/src/views/LoginView.vue`

**Step 1:** Add a third tab for registration.

**Step 2:** Add username, password, confirm password, phone, and email fields for registration mode.

**Step 3:** Add minimal client-side validation for password confirmation and preserve existing error display behavior.

**Step 4:** Redirect to `/` after successful registration and auto-login.

### Task 3: Verify the change

**Files:**
- Verify: `frontend/mobile/package.json`

**Step 1:** Run `npm run build` in `frontend/mobile`.

**Step 2:** Confirm the mobile app still builds successfully after the auth flow changes.
