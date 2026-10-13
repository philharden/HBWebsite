# Hardened Builds LLC — Website

Static, dependency-free marketing website for Hardened Builds LLC, generated from a
single source of truth (`build.py`). Output is plain HTML, CSS, and vanilla JavaScript
with no runtime dependencies, so it is portable to any static host and to the customer
platform with minimal maintenance.

## Build

```
python3 build.py
```

This regenerates the `dist/` directory: `index.html`, one page per service under
`services/`, `styles.css`, `site.js`, the downloadable process image at
`assets/process-overview.svg`, the `_headers` security configuration, `robots.txt`,
and `routes.config.json`.

## Security configuration

- `dist/_headers` — canonical server-set response headers: Content-Security-Policy,
  Strict-Transport-Security (HSTS), X-Content-Type-Options, Referrer-Policy,
  X-Frame-Options, Permissions-Policy, Cross-Origin-Opener-Policy. Apply the equivalent
  configuration on the destination host.
- `routes.config.json` — single-file, default-deny public-route allowlist. This site has
  no authenticated surface; every served route is enumerated as public. Any future
  authenticated surface must sit behind authentication and must not be added to the
  allowlist.

## Deployment

The contents of `dist/` are the deployable artifact. Publish that directory to any static
host. No build step is required at the host; `build.py` runs only to regenerate content.
