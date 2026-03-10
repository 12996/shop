## [ERR-20260310-001] local_dev_startup

**Logged**: 2026-03-10T11:25:00Z
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
Codex sandbox blocked Django on port 8000 and prevented Vite from spawning `esbuild`.

### Error
```
Error: You don't have permission to access that port.

error when starting dev server:
Error: spawn EPERM
```

### Context
- Command attempted: `python backend/manage.py runserver 127.0.0.1:8000 --noreload`
- Command attempted: `node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173`
- Environment details: sandboxed execution could not bind the chosen backend port and could not allow Vite's child-process spawn path

### Suggested Fix
Use backend port `18000` for local startup in this environment, and start Vite outside the sandbox with direct `node vite.js` or normal local terminal usage.

### Metadata
- Reproducible: yes
- Related Files: README.md

### Resolution
- **Resolved**: 2026-03-10T11:30:00Z
- **Commit/PR**: uncommitted
- **Notes**: Switched the documented backend dev port to `18000`, kept frontends on `5173/5174`, and started the services outside the sandbox where Vite child-process spawning is allowed.

---
