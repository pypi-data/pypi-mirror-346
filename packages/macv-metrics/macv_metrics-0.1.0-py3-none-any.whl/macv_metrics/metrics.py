from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Shared metrics, all labeled by module name:
FRAMES_PROCESSED = Counter(
    'macv_frames_processed_total',
    'Total CV frames processed',
    ['module']
)
PROCESSING_TIME = Histogram(
    'macv_frame_processing_seconds',
    'Time to process one frame',
    ['module']
)
MODULE_HEALTH = Gauge(
    'macv_module_health',
    '1 = healthy, 0 = unhealthy',
    ['module']
)

def start_metrics(port: int = 6001) -> None:
    """
    Starts Prometheus metrics server on 0.0.0.0:<port>,
    so its reachable over the Docker network.
    """
    start_http_server(port, addr='0.0.0.0')