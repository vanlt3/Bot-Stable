"""
Production Configuration Module
Provides configuration settings for production deployment
"""

import os
from typing import Dict, Any, Optional

# Deployment Configuration
DEPLOYMENT_CONFIG = {
    'DEBUG_MODE': False,
    'VERBOSE_LOGGING': False,
    'ENABLE_PROFILING': False,
    'ENABLE_METRICS': True,
    'ENABLE_ALERTS': True,
    'ENABLE_BACKUP': True,
    'ENABLE_MONITORING': True,
    'MAX_CONCURRENT_TRADES': 10,
    'RISK_MANAGEMENT_ENABLED': True,
    'AUTO_RECOVERY_ENABLED': True,
    'PERFORMANCE_TRACKING_ENABLED': True
}

# Online Learning Bootstrap Configuration
ONLINE_LEARNING_BOOTSTRAP_CONFIG = {
    'learning_rate': 0.01,
    'max_iter': 1000,
    'random_state': 42,
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'performance_threshold': 0.6,
    'update_interval': 60,
    'enable_auto_retraining': True,
    'enable_performance_tracking': True,
    'enable_model_versioning': True,
    'max_model_versions': 10,
    'backup_interval': 3600,  # 1 hour
    'cleanup_interval': 86400  # 24 hours
}

# Trading Configuration
TRADING_CONFIG = {
    'DEFAULT_TIMEFRAME': '1h',
    'MAX_POSITION_SIZE': 0.1,  # 10% of portfolio
    'STOP_LOSS_PERCENTAGE': 0.02,  # 2%
    'TAKE_PROFIT_PERCENTAGE': 0.04,  # 4%
    'MIN_CONFIDENCE_THRESHOLD': 0.7,
    'MAX_DAILY_TRADES': 50,
    'ENABLE_PAPER_TRADING': True,
    'ENABLE_LIVE_TRADING': False,
    'ENABLE_BACKTESTING': True
}

# API Configuration
API_CONFIG = {
    'REQUEST_TIMEOUT': 30,
    'MAX_RETRIES': 3,
    'RETRY_DELAY': 1,
    'RATE_LIMIT_ENABLED': True,
    'RATE_LIMIT_REQUESTS_PER_MINUTE': 60,
    'ENABLE_CACHING': True,
    'CACHE_TTL': 300,  # 5 minutes
    'ENABLE_COMPRESSION': True
}

# Database Configuration
DATABASE_CONFIG = {
    'ENABLE_PERSISTENCE': True,
    'BACKUP_ENABLED': True,
    'BACKUP_INTERVAL': 3600,  # 1 hour
    'MAX_BACKUP_FILES': 7,
    'ENABLE_COMPRESSION': True,
    'CLEANUP_ENABLED': True,
    'CLEANUP_INTERVAL': 86400  # 24 hours
}

# Logging Configuration
LOGGING_CONFIG = {
    'LOG_LEVEL': 'INFO',
    'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'LOG_FILE_ENABLED': True,
    'LOG_CONSOLE_ENABLED': True,
    'LOG_ROTATION_ENABLED': True,
    'MAX_LOG_FILE_SIZE': '50MB',
    'LOG_RETENTION_DAYS': 7,
    'ENABLE_STRUCTURED_LOGGING': True
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'ENABLE_PROFILING': False,
    'PROFILING_INTERVAL': 300,  # 5 minutes
    'MEMORY_MONITORING_ENABLED': True,
    'CPU_MONITORING_ENABLED': True,
    'DISK_MONITORING_ENABLED': True,
    'NETWORK_MONITORING_ENABLED': True,
    'ALERT_THRESHOLDS': {
        'MEMORY_USAGE_PERCENT': 80,
        'CPU_USAGE_PERCENT': 80,
        'DISK_USAGE_PERCENT': 90,
        'NETWORK_LATENCY_MS': 1000
    }
}

# Security Configuration
SECURITY_CONFIG = {
    'ENABLE_ENCRYPTION': True,
    'ENABLE_AUTHENTICATION': True,
    'ENABLE_AUTHORIZATION': True,
    'SESSION_TIMEOUT': 3600,  # 1 hour
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOCKOUT_DURATION': 900,  # 15 minutes
    'ENABLE_AUDIT_LOGGING': True,
    'ENABLE_INTRUSION_DETECTION': True
}

# Notification Configuration
NOTIFICATION_CONFIG = {
    'ENABLE_EMAIL_ALERTS': False,
    'ENABLE_SMS_ALERTS': False,
    'ENABLE_PUSH_NOTIFICATIONS': False,
    'ENABLE_WEBHOOK_ALERTS': False,
    'ALERT_LEVELS': ['CRITICAL', 'ERROR', 'WARNING', 'INFO'],
    'ALERT_COOLDOWN': 300,  # 5 minutes
    'MAX_ALERTS_PER_HOUR': 10
}

# Feature Flags
FEATURE_FLAGS = {
    'ENABLE_ADVANCED_ANALYTICS': True,
    'ENABLE_MACHINE_LEARNING': True,
    'ENABLE_REINFORCEMENT_LEARNING': True,
    'ENABLE_NEWS_ANALYSIS': True,
    'ENABLE_SENTIMENT_ANALYSIS': True,
    'ENABLE_TECHNICAL_ANALYSIS': True,
    'ENABLE_FUNDAMENTAL_ANALYSIS': True,
    'ENABLE_RISK_MANAGEMENT': True,
    'ENABLE_PORTFOLIO_OPTIMIZATION': True,
    'ENABLE_BACKTESTING': True,
    'ENABLE_PAPER_TRADING': True,
    'ENABLE_LIVE_TRADING': False
}

# Environment-specific overrides
def get_config_for_environment(environment: str = 'production') -> Dict[str, Any]:
    """Get configuration for specific environment"""
    configs = {
        'development': {
            'DEBUG_MODE': True,
            'VERBOSE_LOGGING': True,
            'ENABLE_PROFILING': True,
            'ENABLE_PAPER_TRADING': True,
            'ENABLE_LIVE_TRADING': False,
            'LOG_LEVEL': 'DEBUG'
        },
        'staging': {
            'DEBUG_MODE': True,
            'VERBOSE_LOGGING': True,
            'ENABLE_PAPER_TRADING': True,
            'ENABLE_LIVE_TRADING': False,
            'LOG_LEVEL': 'INFO'
        },
        'production': {
            'DEBUG_MODE': False,
            'VERBOSE_LOGGING': False,
            'ENABLE_PROFILING': False,
            'ENABLE_PAPER_TRADING': False,
            'ENABLE_LIVE_TRADING': True,
            'LOG_LEVEL': 'WARNING'
        }
    }
    
    return configs.get(environment, configs['production'])

def apply_environment_config(environment: str = 'production') -> None:
    """Apply environment-specific configuration"""
    env_config = get_config_for_environment(environment)
    
    # Update deployment config
    DEPLOYMENT_CONFIG.update(env_config)
    
    # Update logging config
    if 'LOG_LEVEL' in env_config:
        LOGGING_CONFIG['LOG_LEVEL'] = env_config['LOG_LEVEL']
    
    # Update trading config
    if 'ENABLE_PAPER_TRADING' in env_config:
        TRADING_CONFIG['ENABLE_PAPER_TRADING'] = env_config['ENABLE_PAPER_TRADING']
    if 'ENABLE_LIVE_TRADING' in env_config:
        TRADING_CONFIG['ENABLE_LIVE_TRADING'] = env_config['ENABLE_LIVE_TRADING']

# Initialize with production environment by default
apply_environment_config('production')