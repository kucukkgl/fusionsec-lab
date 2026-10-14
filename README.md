# FusionSec Lab

FusionSec Lab is a Flask-based security training application.

## Session cookie logging

The app logs when Flask issues or clears its session cookie, along with the
cookie name, lifetime, and security attributes. By default, the raw cookie
value is **not** written to logs.

For a controlled lab exercise, edit `config.toml` and set
`log_session_cookie_value` to `true`:

```toml
log_session_cookie_value = true
```

When enabled, the raw session cookie is written at warning level to the
application logs (`logs/app.log`, `logs/app_log.json`, and the console). Treat
it like a password: anyone who obtains the value may be able to reuse that
session. Enable this only in an isolated lab, restrict access to the logs, and
turn it off when the exercise is complete:

```toml
log_session_cookie_value = false
```

The setting is read when the app starts, so restart the app after changing it.
