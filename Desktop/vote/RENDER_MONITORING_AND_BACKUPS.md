# Render Monitoring & Backups Configuration Guide

This file documents how to configure monitoring, alerting, and backups for the `university_evoting` application on Render.

## Database Backups

### Automatic Backups (Render Managed PostgreSQL)

1. **In Render Dashboard**, go to **Databases** → **university-evoting-db**
2. Click **Settings** → **Backups**
3. Configure:
   - **Automated backups**: Enable
   - **Retention period**: 7 days (minimum, recommended 14-30 for production)
   - **Backup window**: Choose off-peak hours (e.g., 2-3 AM UTC)

4. **Manual backup** before major schema changes:
   - Go to **Backups** → **Create backup**
   - Add a descriptive label (e.g., "Pre-election-day-backup-2026-01-30")

### Backup Restoration

If you need to restore from a backup:

1. **In Render Database dashboard**, go to **Backups**
2. Click **Restore** on the desired backup
3. Confirm the restore operation (this creates a new database; you'll need to update CONNECTION strings)
4. Update `DATABASE_URL` env var to point to restored database
5. Restart the web service

## Health Checks

### Service Health Monitoring

The `/health/` endpoint is already configured in `render.yaml`:

```yaml
healthCheckPath: /health/
```

This endpoint checks:
- Database connectivity
- Returns JSON: `{"status": "ok", "db": true}`

**Monitor in Render Dashboard**:
1. Go to **Web Service** → **Health**
2. View health check history and status

### Custom Health Checks (Advanced)

To extend health checks, add to `evoting_system/health.py`:

```python
def health(request):
    status = 'ok'
    checks = {'db': True}
    
    # Check Redis
    try:
        from django.core.cache import cache
        cache.set('health_check', 1, 1)
        checks['cache'] = True
    except Exception:
        checks['cache'] = False
        status = 'partial'
    
    # Check Celery
    try:
        from celery import current_app
        current_app.control.ping(timeout=1)
        checks['celery'] = True
    except Exception:
        checks['celery'] = False
        status = 'partial'
    
    return JsonResponse({
        'status': status,
        **checks
    })
```

## Alerting

### Set up Alerts in Render

1. **In Render Dashboard**, go to **Alerts** (or **Organization** → **Settings** → **Alerts**)
2. Click **Create Alert**
3. Configure notifications for:
   - **Deploy failures** → Email/Slack
   - **Service crashes** → Email/Slack
   - **High CPU usage** (>80% for 5 min) → Email/Slack
   - **High memory usage** (>90%) → Email/Slack
   - **Health check failures** → Email/Slack

### Example Alert Configuration

- **Trigger**: Health check fails
- **Condition**: 3 consecutive failures
- **Action**: Send email to ops@university.edu
- **Escalation**: If not resolved in 15 min, trigger incident

### Integration with Monitoring Tools

**Render supports**:
- Email notifications
- Slack webhooks
- PagerDuty (for on-call escalation)

**Setup example for Slack**:
1. Create a Slack webhook: https://api.slack.com/messaging/webhooks
2. In Render, go to **Alerts** → **New Alert** → **Notification** → Paste webhook URL
3. Test the webhook with a deployment

## Database Performance Monitoring

### Query Logs

To view slow queries:

1. **In Render Postgres dashboard**, go to **Logs**
2. Filter for `slow query` or `duration > 1000ms`
3. Identify problematic queries and optimize:
   ```bash
   python manage.py dbshell
   ```
   Then run analysis queries (if DB supports):
   ```sql
   SELECT query, calls, mean_time
   FROM pg_stat_statements
   ORDER BY mean_time DESC
   LIMIT 10;
   ```

### Connection Pooling (Advanced)

For high-traffic production deployments, enable PgBouncer connection pooling in Render:

1. **Database Settings** → **Connection Pool** → Enable
2. Configure pool size: `min_pool_size=5, max_pool_size=20`

## Log Monitoring

### Viewing Service Logs

1. **In Render Web Service dashboard**, click **Logs**
2. Filter by log level or keyword:
   - `ERROR` — application errors
   - `WARNING` — potential issues
   - `CRITICAL` — system failures

### Log Retention

- Render stores logs for **30 days** by default
- For longer retention, integrate with external logging:

### External Logging (Optional)

For centralized log analysis, integrate with:

**Option 1: Sentry (Error Tracking)**
```python
# In settings.py (already supported)
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False
    )
```

To enable:
1. Create a Sentry project at https://sentry.io
2. Copy your DSN
3. Set `SENTRY_DSN=<your-dsn>` in Render env vars
4. Errors will be tracked in Sentry dashboard

**Option 2: ELK Stack / CloudWatch**
- Render doesn't support direct ELK integration
- Alternative: Export logs to CloudWatch or use a logging service like Datadog

**Option 3: Log Aggregation Service (Datadog, New Relic, etc.)**
- Configure via Render's integration marketplace (if available)

## Performance Optimization

### Database Indexes

Ensure critical queries have indexes:

```bash
python manage.py dbshell
```

Check missing indexes:
```sql
-- Recommended indexes for eVoting
CREATE INDEX idx_election_is_published ON elections_election(is_published, start_time, end_time);
CREATE INDEX idx_vote_created_by ON voting_vote(created_by_id);
CREATE INDEX idx_vote_election ON voting_vote(election_id);
CREATE INDEX idx_candidate_election ON elections_candidate(election_id, approved);
CREATE INDEX idx_user_username ON accounts_user(username);
CREATE INDEX idx_user_email ON accounts_user(email);
```

### Query Optimization

Profile slow queries with Django Debug Toolbar (development only):

```python
# In settings.py (development only)
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']
```

## Scaling Recommendations

### When to Scale Up

- **Web Service**: Increase instance type when response times > 500ms or CPU > 80%
- **Worker**: Add more workers if task queue is growing (Celery monitoring)
- **Database**: Scale when queries are slow or connections are maxed

### Horizontal Scaling

- **Web Service**: Enable **Auto Scaling** in Render:
  - Min instances: 2
  - Max instances: 5
  - Scale trigger: CPU > 70% for 2 min

- **Workers**: Increase `concurrency` in `start_command`:
  ```bash
  celery -A evoting_system worker -l info --concurrency=8
  ```

## Disaster Recovery

### RTO/RPO Targets

- **RTO** (Recovery Time Objective): < 1 hour
- **RPO** (Recovery Point Objective): < 1 day (depends on backup frequency)

### Recovery Runbook

1. **Database failure**:
   - Go to **Backups** → Restore latest backup
   - Update `DATABASE_URL` env var
   - Restart web/worker services

2. **Service failure**:
   - Render auto-restarts crashed services
   - If manual restart needed: **Web Service** → **Actions** → **Restart**

3. **Redis loss**:
   - Render auto-provisions a new Redis instance
   - Celery task queue will be lost (non-critical, retried on restart)
   - Update `REDIS_URL` env var if instance changed

4. **Complete outage** (rare):
   - Switch DNS to backup infrastructure (if available)
   - Contact Render support for emergency recovery

## Compliance & Auditing

### Audit Logs

Enable Django admin audit logging:

1. **In Render Shell**:
   ```bash
   python manage.py shell
   >>> from django.contrib.admin.models import LogEntry
   >>> LogEntry.objects.all().count()  # View admin changes
   ```

2. Or integrate with a dedicated audit logging solution (e.g., django-auditlog)

### Data Retention

Configure data retention per regulations (GDPR, etc.):

```python
# Example: Delete user data after 2 years of inactivity
from django.utils import timezone
from datetime import timedelta

User.objects.filter(last_login__lt=timezone.now() - timedelta(days=730)).delete()
```

### Compliance Checklist

- [ ] Database backups enabled and tested
- [ ] Health checks monitoring
- [ ] Log retention configured
- [ ] Error tracking (Sentry) enabled
- [ ] SSL/HTTPS enforced
- [ ] Secrets managed (no hardcoded credentials)
- [ ] Access logs reviewed regularly
- [ ] Data retention policy documented

---

**Questions?** Refer to Render documentation: https://render.com/docs
