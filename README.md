# FusionSec Lab

FusionSec Lab is a Flask-based security training application.

## Docker

Build and run the lab:

```sh
docker build -t fusionsec-lab .
docker run --rm --name fusionsec-lab -p 8080:80 fusionsec-lab
```

The service listens on port 80 inside the container; Docker publishes it as
port 8080 on all VM interfaces. Open `http://<server-lan-ip>:8080` from another
machine.
The image runs as a non-root user and continues to use SQLite. The database is
initialized with seed data whenever the service starts, so account changes are
not preserved across container restarts.

This application contains intentionally vulnerable training modules. Keep it
on an isolated lab network, restrict inbound port 8080 using the host firewall,
and do not expose it directly to the internet.

## Signup

New accounts require a username, a school ID, and a password. The school ID is
stored with the account and shown on the authenticated welcome page as training
data. Use fictional IDs in the lab.

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

## Password-hash logging

Password-hash values are not logged by default. To see the stored and submitted
MD5 digests during signup and login in this training lab, set this option in
`config.toml`:

```toml
log_password_hash = true
```

When enabled, the logs include the generated hash at signup and both the stored
and submitted hashes during login verification. Plaintext passwords are never
logged. Hashes are still sensitive verification material, especially with this
lab's intentionally weak MD5 scheme; keep the option enabled only in an
isolated lab and turn it off afterward:

```toml
log_password_hash = false
```

Restart the app after changing the setting.
