"""
Online Learning Bootstrap Module
Provides enhanced online learning capabilities for the trading bot
"""

import logging
import numpy as np
from typing import Dict, Any, Optional, List
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib
import os
from datetime import datetime

class OnlineLearningBootstrap:
    """Enhanced online learning bootstrap for trading models"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the bootstrap module"""
        self.config = config or {}
        self.models = {}
        self.performance_tracker = {}
        self.feature_importance = {}
        self.model_history = {}
        
        # Default configuration
        self.default_config = {
            'learning_rate': 0.01,
            'max_iter': 1000,
            'random_state': 42,
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2
        }
        
        # Merge with provided config
        self.config = {**self.default_config, **self.config}
        
        logging.info("✅ [Bootstrap] OnlineLearningBootstrap initialized")
    
    def initialize_models(self, symbols: List[str]) -> None:
        """Initialize models for all symbols"""
        for symbol in symbols:
            self.models[symbol] = self._create_initial_model()
            self.performance_tracker[symbol] = {
                'accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0,
                'total_predictions': 0,
                'correct_predictions': 0,
                'last_updated': datetime.now()
            }
            self.feature_importance[symbol] = {}
            self.model_history[symbol] = []
            
        logging.info(f"✅ [Bootstrap] Initialized models for {len(symbols)} symbols")
    
    def _create_initial_model(self):
        """Create initial model for a symbol"""
        # Use SGDClassifier as default for online learning
        model = SGDClassifier(
            learning_rate='adaptive',
            eta0=self.config['learning_rate'],
            max_iter=self.config['max_iter'],
            random_state=self.config['random_state']
        )
        return model
    
    def update_model(self, symbol: str, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Update model with new data"""
        if symbol not in self.models:
            self.models[symbol] = self._create_initial_model()
        
        # Partial fit for online learning
        self.models[symbol].partial_fit(X, y, classes=np.unique(y))
        
        # Update performance metrics
        if len(y) > 0:
            predictions = self.models[symbol].predict(X)
            accuracy = accuracy_score(y, predictions)
            precision = precision_score(y, predictions, average='weighted', zero_division=0)
            recall = recall_score(y, predictions, average='weighted', zero_division=0)
            
            self.performance_tracker[symbol].update({
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'total_predictions': self.performance_tracker[symbol]['total_predictions'] + len(y),
                'correct_predictions': self.performance_tracker[symbol]['correct_predictions'] + np.sum(predictions == y),
                'last_updated': datetime.now()
            })
        
        return self.performance_tracker[symbol]
    
    def predict(self, symbol: str, X: np.ndarray) -> np.ndarray:
        """Make predictions for a symbol"""
        if symbol not in self.models:
            # Return random predictions if model doesn't exist
            return np.random.choice([0, 1], size=len(X))
        
        return self.models[symbol].predict(X)
    
    def get_model_performance(self, symbol: str) -> Dict[str, float]:
        """Get performance metrics for a symbol"""
        return self.performance_tracker.get(symbol, {})
    
    def save_models(self, filepath: str) -> None:
        """Save all models to file"""
        model_data = {
            'models': self.models,
            'performance_tracker': self.performance_tracker,
            'feature_importance': self.feature_importance,
            'config': self.config
        }
        joblib.dump(model_data, filepath)
        logging.info(f"✅ [Bootstrap] Models saved to {filepath}")
    
    def load_models(self, filepath: str) -> None:
        """Load models from file"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.models = model_data.get('models', {})
            self.performance_tracker = model_data.get('performance_tracker', {})
            self.feature_importance = model_data.get('feature_importance', {})
            self.config = model_data.get('config', self.config)
            logging.info(f"✅ [Bootstrap] Models loaded from {filepath}")
        else:
            logging.warning(f"⚠️ [Bootstrap] Model file {filepath} not found")
    
    def get_all_performance(self) -> Dict[str, Dict[str, float]]:
        """Get performance metrics for all symbols"""
        return self.performance_tracker
    
    def reset_model(self, symbol: str) -> None:
        """Reset model for a specific symbol"""
        if symbol in self.models:
            self.models[symbol] = self._create_initial_model()
            self.performance_tracker[symbol] = {
                'accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0,
                'total_predictions': 0,
                'correct_predictions': 0,
                'last_updated': datetime.now()
            }
            logging.info(f"✅ [Bootstrap] Model reset for {symbol}")
    
    def get_model_info(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive model information"""
        return {
            'model_type': type(self.models.get(symbol, None)).__name__,
            'performance': self.get_model_performance(symbol),
            'feature_importance': self.feature_importance.get(symbol, {}),
            'config': self.config
        }