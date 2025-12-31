from django.http import HttpResponse

try:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    def metrics_view(request):
        data = generate_latest()
        return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
except Exception:
    def metrics_view(request):
        return HttpResponse(b"# no prometheus_client available\n", content_type="text/plain")
