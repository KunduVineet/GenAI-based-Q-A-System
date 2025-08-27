"""
Monitoring utilities for the AI Backend Service
"""

import time
import psutil
from typing import Dict, Any
from app.utils.logger import app_logger

class SystemMonitor:
    """System monitoring utilities"""
    
    @staticmethod
    def get_system_metrics() -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_usage_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                },
                "timestamp": time.time()
            }
        except Exception as e:
            app_logger.error(f"Error getting system metrics: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def check_system_health() -> Dict[str, Any]:
        """Check overall system health"""
        metrics = SystemMonitor.get_system_metrics()
        
        if "error" in metrics:
            return {"status": "unhealthy", "reason": metrics["error"]}
        
        # Define health thresholds
        cpu_threshold = 90.0
        memory_threshold = 90.0
        disk_threshold = 90.0
        
        issues = []
        
        if metrics["cpu_usage_percent"] > cpu_threshold:
            issues.append(f"High CPU usage: {metrics['cpu_usage_percent']:.1f}%")
        
        if metrics["memory"]["percent"] > memory_threshold:
            issues.append(f"High memory usage: {metrics['memory']['percent']:.1f}%")
        
        if metrics["disk"]["percent"] > disk_threshold:
            issues.append(f"High disk usage: {metrics['disk']['percent']:.1f}%")
        
        if issues:
            return {
                "status": "warning",
                "issues": issues,
                "metrics": metrics
            }
        
        return {
            "status": "healthy",
            "metrics": metrics
        }