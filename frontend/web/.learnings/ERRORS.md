## [ERR-20260309-001] npm_install_timeout

**Logged**: 2026-03-09T23:28:21.4964785+08:00
**Priority**: medium
**Status**: resolved
**Area**: frontend

### Summary
`npm install` in the frontend project timed out before completion.

### Error
```
command timed out after 120099 milliseconds
```

### Context
- Command attempted: `npm install`
- Working directory: `F:\work\project\shop\frontend\web`
- Registry: `https://registry.npmjs.org/`
- Project state after timeout: `node_modules` and `package-lock.json` were still missing

### Suggested Fix
Retry with a longer timeout and only investigate deeper if installation still does not produce `node_modules`.

### Metadata
- Reproducible: unknown
- Related Files: package.json

### Resolution
- **Resolved**: 2026-03-09T23:40:00+08:00
- **Commit/PR**: none
- **Notes**: Installed dependencies with a workspace-local npm cache outside the sandbox, then installed the missing `@rollup/rollup-win32-x64-msvc@4.59.0` optional package. `npx vite --version` and `npm run build` succeeded afterward.

---
