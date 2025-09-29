"""
Online Learning Integration Module
Provides enhanced online learning management and integration
"""

import logging
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from online_learning_bootstrap import OnlineLearningBootstrap
import asyncio
from datetime import datetime, timedelta
import threading
import queue
import time

class EnhancedOnlineLearningManager:
    """Enhanced online learning manager with advanced features"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the enhanced online learning manager"""
        self.config = config or {}
        self.bootstrap = OnlineLearningBootstrap(self.config)
        self.symbols = []
        self.is_initialized = False
        self.update_queue = queue.Queue()
        self.performance_threshold = self.config.get('performance_threshold', 0.6)
        self.update_interval = self.config.get('update_interval', 60)  # seconds
        self.last_update = {}
        self.model_versions = {}
        
        # Async update thread
        self.update_thread = None
        self.stop_updates = False
        
        logging.info("✅ [Integration] EnhancedOnlineLearningManager initialized")
    
    def initialize(self, symbols: List[str]) -> None:
        """Initialize the manager with symbols"""
        self.symbols = symbols
        self.bootstrap.initialize_models(symbols)
        
        # Initialize tracking
        for symbol in symbols:
            self.last_update[symbol] = datetime.now()
            self.model_versions[symbol] = 1
        
        self.is_initialized = True
        self._start_update_thread()
        
        logging.info(f"✅ [Integration] Manager initialized for {len(symbols)} symbols")
    
    def _start_update_thread(self) -> None:
        """Start the background update thread"""
        if self.update_thread is None or not self.update_thread.is_alive():
            self.stop_updates = False
            self.update_thread = threading.Thread(target=self._update_worker, daemon=True)
            self.update_thread.start()
            logging.info("✅ [Integration] Update thread started")
    
    def _update_worker(self) -> None:
        """Background worker for processing updates"""
        while not self.stop_updates:
            try:
                # Process queued updates
                while not self.update_queue.empty():
                    try:
                        symbol, X, y = self.update_queue.get_nowait()
                        self._process_update(symbol, X, y)
                    except queue.Empty:
                        break
                
                # Periodic model evaluation
                self._evaluate_models()
                
                time.sleep(self.update_interval)
                
            except Exception as e:
                logging.error(f"❌ [Integration] Update worker error: {e}")
                time.sleep(5)  # Wait before retrying
    
    def _process_update(self, symbol: str, X: np.ndarray, y: np.ndarray) -> None:
        """Process a model update"""
        try:
            performance = self.bootstrap.update_model(symbol, X, y)
            self.last_update[symbol] = datetime.now()
            self.model_versions[symbol] += 1
            
            # Check if model needs retraining
            if performance.get('accuracy', 0) < self.performance_threshold:
                self._retrain_model(symbol)
                
        except Exception as e:
            logging.error(f"❌ [Integration] Error processing update for {symbol}: {e}")
    
    def _retrain_model(self, symbol: str) -> None:
        """Retrain model if performance is poor"""
        try:
            logging.warning(f"⚠️ [Integration] Retraining model for {symbol} due to poor performance")
            self.bootstrap.reset_model(symbol)
            self.model_versions[symbol] += 1
        except Exception as e:
            logging.error(f"❌ [Integration] Error retraining model for {symbol}: {e}")
    
    def _evaluate_models(self) -> None:
        """Periodically evaluate all models"""
        try:
            for symbol in self.symbols:
                performance = self.bootstrap.get_model_performance(symbol)
                if performance.get('accuracy', 0) < self.performance_threshold:
                    logging.warning(f"⚠️ [Integration] Poor performance detected for {symbol}: {performance}")
        except Exception as e:
            logging.error(f"❌ [Integration] Error evaluating models: {e}")
    
    def add_training_data(self, symbol: str, X: np.ndarray, y: np.ndarray) -> None:
        """Add training data to the queue"""
        if not self.is_initialized:
            logging.warning("⚠️ [Integration] Manager not initialized")
            return
        
        if symbol not in self.symbols:
            logging.warning(f"⚠️ [Integration] Symbol {symbol} not in initialized symbols")
            return
        
        try:
            self.update_queue.put((symbol, X, y))
        except Exception as e:
            logging.error(f"❌ [Integration] Error adding training data for {symbol}: {e}")
    
    def predict(self, symbol: str, X: np.ndarray) -> np.ndarray:
        """Make predictions for a symbol"""
        if not self.is_initialized:
            logging.warning("⚠️ [Integration] Manager not initialized")
            return np.random.choice([0, 1], size=len(X))
        
        return self.bootstrap.predict(symbol, X)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for all symbols"""
        if not self.is_initialized:
            return {}
        
        summary = {}
        for symbol in self.symbols:
            performance = self.bootstrap.get_model_performance(symbol)
            summary[symbol] = {
                'performance': performance,
                'last_update': self.last_update.get(symbol),
                'model_version': self.model_versions.get(symbol, 1),
                'status': 'active' if performance.get('accuracy', 0) >= self.performance_threshold else 'needs_attention'
            }
        
        return summary
    
    def get_model_info(self, symbol: str) -> Dict[str, Any]:
        """Get detailed model information"""
        if not self.is_initialized or symbol not in self.symbols:
            return {}
        
        return {
            'bootstrap_info': self.bootstrap.get_model_info(symbol),
            'last_update': self.last_update.get(symbol),
            'model_version': self.model_versions.get(symbol, 1),
            'queue_size': self.update_queue.qsize()
        }
    
    def save_state(self, filepath: str) -> None:
        """Save the current state"""
        try:
            self.bootstrap.save_models(filepath)
            logging.info(f"✅ [Integration] State saved to {filepath}")
        except Exception as e:
            logging.error(f"❌ [Integration] Error saving state: {e}")
    
    def load_state(self, filepath: str) -> None:
        """Load state from file"""
        try:
            self.bootstrap.load_models(filepath)
            logging.info(f"✅ [Integration] State loaded from {filepath}")
        except Exception as e:
            logging.error(f"❌ [Integration] Error loading state: {e}")
    
    def shutdown(self) -> None:
        """Shutdown the manager"""
        self.stop_updates = True
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=5)
        logging.info("✅ [Integration] Manager shutdown complete")

def create_enhanced_online_learning_manager(config: Optional[Dict[str, Any]] = None) -> EnhancedOnlineLearningManager:
    """Factory function to create enhanced online learning manager"""
    return EnhancedOnlineLearningManager(config)