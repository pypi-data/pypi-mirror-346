"""
Metrics collection and monitoring for AI-on-Rails.

Provides utilities for collecting, aggregating, and exporting metrics.
"""

import time
import threading
from typing import Dict, Any, List, Optional, Callable, Union
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum
import json
import statistics
from dataclasses import dataclass, field
import asyncio


class MetricType(str, Enum):
    """Types of metrics supported."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"
    TIMER = "timer"


@dataclass
class MetricConfig:
    """Configuration for metrics collection."""
    namespace: str = "ai_on_rails"
    flush_interval_seconds: int = 60
    retention_minutes: int = 60
    aggregation_window_seconds: int = 60
    enable_labels: bool = True
    export_format: str = "prometheus"  # prometheus, json, statsd


@dataclass
class Metric:
    """Base class for all metrics."""
    name: str
    metric_type: MetricType
    description: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    value: Union[float, int] = 0


class MetricsCollector:
    """
    Collects and manages metrics for AI agents.
    """
    
    def __init__(self, config: MetricConfig):
        """
        Initialize metrics collector.
        
        Args:
            config: Metrics configuration
        """
        self.config = config
        self._metrics: Dict[str, List[Metric]] = defaultdict(list)
        self._lock = threading.Lock()
        self._running = False
        self._flush_thread = None
        self._exporters: List[Callable] = []
    
    def start(self):
        """Start the metrics collector background tasks."""
        self._running = True
        self._flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()
    
    def stop(self):
        """Stop the metrics collector."""
        self._running = False
        if self._flush_thread:
            self._flush_thread.join()
    
    def register_exporter(self, exporter: Callable):
        """Register a metrics exporter function."""
        self._exporters.append(exporter)
    
    def counter(self, name: str, value: float = 1, 
                labels: Optional[Dict[str, str]] = None,
                description: str = ""):
        """
        Increment a counter metric.
        
        Args:
            name: Metric name
            value: Value to increment by
            labels: Optional labels
            description: Metric description
        """
        metric = Metric(
            name=name,
            metric_type=MetricType.COUNTER,
            description=description,
            labels=labels or {},
            value=value
        )
        self._add_metric(metric)
    
    def gauge(self, name: str, value: float,
              labels: Optional[Dict[str, str]] = None,
              description: str = ""):
        """
        Set a gauge metric.
        
        Args:
            name: Metric name
            value: Gauge value
            labels: Optional labels
            description: Metric description
        """
        metric = Metric(
            name=name,
            metric_type=MetricType.GAUGE,
            description=description,
            labels=labels or {},
            value=value
        )
        self._add_metric(metric)
    
    def histogram(self, name: str, value: float,
                  labels: Optional[Dict[str, str]] = None,
                  description: str = ""):
        """
        Record a histogram metric.
        
        Args:
            name: Metric name
            value: Value to record
            labels: Optional labels
            description: Metric description
        """
        metric = Metric(
            name=name,
            metric_type=MetricType.HISTOGRAM,
            description=description,
            labels=labels or {},
            value=value
        )
        self._add_metric(metric)
    
    def timer(self, name: str, labels: Optional[Dict[str, str]] = None,
              description: str = ""):
        """
        Create a timer context manager.
        
        Args:
            name: Metric name
            labels: Optional labels
            description: Metric description
            
        Returns:
            Timer context manager
        """
        return Timer(self, name, labels, description)
    
    def _add_metric(self, metric: Metric):
        """Add a metric to the collector."""
        with self._lock:
            key = self._get_metric_key(metric)
            self._metrics[key].append(metric)
            
            # Clean old metrics
            self._clean_old_metrics(key)
    
    def _get_metric_key(self, metric: Metric) -> str:
        """Generate a unique key for a metric."""
        if self.config.enable_labels and metric.labels:
            label_str = "_".join(f"{k}={v}" for k, v in sorted(metric.labels.items()))
            return f"{metric.name}_{label_str}"
        return metric.name
    
    def _clean_old_metrics(self, key: str):
        """Remove metrics older than retention period."""
        cutoff = time.time() - (self.config.retention_minutes * 60)
        self._metrics[key] = [
            m for m in self._metrics[key] if m.timestamp > cutoff
        ]
    
    def _flush_loop(self):
        """Background loop for flushing metrics."""
        while self._running:
            time.sleep(self.config.flush_interval_seconds)
            self._flush_metrics()
    
    def _flush_metrics(self):
        """Flush metrics to exporters."""
        with self._lock:
            aggregated = self._aggregate_metrics()
            for exporter in self._exporters:
                try:
                    exporter(aggregated)
                except Exception as e:
                    print(f"Error in metrics exporter: {e}")
    
    def _aggregate_metrics(self) -> Dict[str, Any]:
        """Aggregate metrics for export."""
        aggregated = {}
        
        for key, metrics in self._metrics.items():
            if not metrics:
                continue
            
            metric_type = metrics[0].metric_type
            values = [m.value for m in metrics]
            
            if metric_type == MetricType.COUNTER:
                aggregated[key] = {
                    "type": "counter",
                    "value": sum(values),
                    "labels": metrics[0].labels,
                    "description": metrics[0].description
                }
            
            elif metric_type == MetricType.GAUGE:
                aggregated[key] = {
                    "type": "gauge",
                    "value": values[-1],  # Latest value
                    "labels": metrics[0].labels,
                    "description": metrics[0].description
                }
            
            elif metric_type == MetricType.HISTOGRAM:
                aggregated[key] = {
                    "type": "histogram",
                    "count": len(values),
                    "sum": sum(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": statistics.mean(values),
                    "p50": statistics.median(values),
                    "p95": statistics.quantiles(values, n=20)[18] if len(values) >= 20 else max(values),
                    "p99": statistics.quantiles(values, n=100)[98] if len(values) >= 100 else max(values),
                    "labels": metrics[0].labels,
                    "description": metrics[0].description
                }
        
        return aggregated


class Timer:
    """Context manager for timing operations."""
    
    def __init__(self, collector: MetricsCollector, name: str,
                 labels: Optional[Dict[str, str]] = None,
                 description: str = ""):
        self.collector = collector
        self.name = name
        self.labels = labels
        self.description = description
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.collector.histogram(
            self.name,
            duration,
            self.labels,
            self.description
        )


class PrometheusExporter:
    """Exports metrics in Prometheus format."""
    
    def __init__(self, namespace: str = "ai_on_rails"):
        self.namespace = namespace
    
    def export(self, metrics: Dict[str, Any]) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        
        for name, metric in metrics.items():
            metric_name = f"{self.namespace}_{name}"
            labels_str = self._format_labels(metric.get("labels", {}))
            
            # Add HELP and TYPE lines
            if metric.get("description"):
                lines.append(f"# HELP {metric_name} {metric['description']}")
            lines.append(f"# TYPE {metric_name} {metric['type']}")
            
            if metric["type"] == "counter":
                lines.append(f"{metric_name}{labels_str} {metric['value']}")
            
            elif metric["type"] == "gauge":
                lines.append(f"{metric_name}{labels_str} {metric['value']}")
            
            elif metric["type"] == "histogram":
                lines.extend([
                    f"{metric_name}_count{labels_str} {metric['count']}",
                    f"{metric_name}_sum{labels_str} {metric['sum']}",
                    f"{metric_name}_min{labels_str} {metric['min']}",
                    f"{metric_name}_max{labels_str} {metric['max']}",
                    f"{metric_name}_avg{labels_str} {metric['avg']}",
                    f"{metric_name}_p50{labels_str} {metric['p50']}",
                    f"{metric_name}_p95{labels_str} {metric['p95']}",
                    f"{metric_name}_p99{labels_str} {metric['p99']}"
                ])
        
        return "\n".join(lines)
    
    def _format_labels(self, labels: Dict[str, str]) -> str:
        """Format labels for Prometheus."""
        if not labels:
            return ""
        
        label_parts = [f'{k}="{v}"' for k, v in labels.items()]
        return "{" + ",".join(label_parts) + "}"


# Global metrics collector instance
_metrics_collector = None


def get_metrics_collector(config: Optional[MetricConfig] = None) -> MetricsCollector:
    """Get or create the global metrics collector."""
    global _metrics_collector
    
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector(config or MetricConfig())
        _metrics_collector.start()
    
    return _metrics_collector


# Convenience functions
def increment_counter(name: str, value: float = 1, 
                     labels: Optional[Dict[str, str]] = None):
    """Increment a counter metric."""
    collector = get_metrics_collector()
    collector.counter(name, value, labels)


def set_gauge(name: str, value: float, 
              labels: Optional[Dict[str, str]] = None):
    """Set a gauge metric."""
    collector = get_metrics_collector()
    collector.gauge(name, value, labels)


def record_histogram(name: str, value: float,
                    labels: Optional[Dict[str, str]] = None):
    """Record a histogram metric."""
    collector = get_metrics_collector()
    collector.histogram(name, value, labels)


def timer_metric(name: str, labels: Optional[Dict[str, str]] = None):
    """Create a timer context manager."""
    collector = get_metrics_collector()
    return collector.timer(name, labels)