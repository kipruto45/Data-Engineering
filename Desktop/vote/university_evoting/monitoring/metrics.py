"""Simple metrics facade for optional Prometheus/Sentry integration.

- If prometheus_client is available, expose a Counter for named metrics.
- If sentry_sdk is available, provide a capture function.
- Otherwise, functions are no-ops to keep POC simple.
"""

try:
    from prometheus_client import Counter
    _counters = {}
    def increment(name, amount=1):
        c = _counters.get(name)
        if c is None:
            c = Counter(f"university_evoting_{name}", f"Counter for {name}")
            _counters[name] = c
        c.inc(amount)
except Exception:
    def increment(name, amount=1):
        # no-op if prometheus_client not installed
        return

try:
    import sentry_sdk
    def capture_message(msg, **kwargs):
        sentry_sdk.capture_message(msg, **kwargs)
except Exception:
    def capture_message(msg, **kwargs):
        return
