# Mobile Auth Split Layout Design

**Context**

The mobile auth page currently mixes login and registration into one card with mode switching. The new requirement is to show login and registration together: on wide screens they should appear side by side, while on narrow screens they should stack vertically.

**Decision**

Use two independent cards inside a responsive grid:
- Left card: login
- Right card: registration

The login card keeps the existing password login and code login switch. The registration card stays visible at the same time and keeps the existing register-then-auto-login behavior.

**Why this approach**

- It matches the requested visual model directly.
- It avoids forcing users to switch away from login just to discover registration.
- It keeps auth behavior unchanged and limits the change to one view file.

**Component Design**

- Keep the page hero at the top.
- Replace the single card with an `auth-grid`.
- Render `login-card` and `register-card` as separate sections.
- Keep login state and registration state separate in the view.

**State and Data Flow**

- `loginMode` controls only the login card.
- `loginErrorMessage` and `registerErrorMessage` are independent.
- `loginSubmitting` and `registerSubmitting` are independent local flags.
- Registration still calls `authStore.registerAndLogin(...)` and then redirects to `/`.

**Responsive Behavior**

- Default: single-column layout for narrow screens.
- At a desktop-like breakpoint: two equal-width columns.

**Validation and Errors**

- Login validation remains minimal and delegates failures to backend responses.
- Registration keeps password confirmation validation before calling the API.
- Error messages render only inside the card that triggered them.

**Verification**

- This frontend currently has no existing UI test harness in the mobile package.
- Verify the change with `npm run build` in `frontend/mobile`.
