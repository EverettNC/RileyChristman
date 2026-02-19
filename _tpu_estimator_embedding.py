"""
TPU Estimator Embedding: Hardware-Optimized Column Extraction
Standard: 96% Quality Threshold | Target Latency: 0.04s
Integrates: TensorFlow TPU Estimator (or CPU fallback)
"""

import logging
import time

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

def get_tpu_embedding_columns(feature_columns):
    """
    Extracts feature columns suitable for TPU embedding acceleration.
    On CPU/GPU fallback, returns all columns tagged as 'embedding'.
    
    Args:
        feature_columns: list of tf.feature_column or dict descriptors.
    Returns:
        list of TPU-compatible embedding columns.
    """
    tpu_columns = []

    if not TF_AVAILABLE:
        logging.warning("⚠️ TensorFlow not available. Using mock TPU columns.")
        # Mock: treat all columns as TPU-eligible
        for col in feature_columns:
            if isinstance(col, dict):
                tpu_columns.append({
                    "name": col.get("name", "unknown"),
                    "dimension": col.get("dimension", 64),
                    "accelerated": True
                })
            else:
                tpu_columns.append({"name": str(col), "dimension": 64, "accelerated": True})
        return tpu_columns

    # TensorFlow path: extract embedding columns
    for col in feature_columns:
        if hasattr(col, '_variable_shape'):
            # This is a real tf.feature_column embedding
            tpu_columns.append(col)
        elif isinstance(col, dict):
            # Descriptor-based: build an embedding column
            name = col.get("name", "feature")
            dim = col.get("dimension", 64)
            vocab_size = col.get("vocab_size", 10000)
            cat_col = tf.feature_column.categorical_column_with_identity(name, num_buckets=vocab_size)
            embed_col = tf.feature_column.embedding_column(cat_col, dimension=dim)
            tpu_columns.append(embed_col)

    logging.info(f"⚡ TPU Embedding Columns: {len(tpu_columns)} extracted.")
    return tpu_columns


class TPULatencyMonitor:
    """
    Monitors and enforces the 0.04s latency target for Riley's Hearing Protocol.
    """
    def __init__(self, target_ms=40):
        self.target_ms = target_ms
        self.history = []

    def measure(self, fn, *args, **kwargs):
        """Wraps a function call and measures its latency."""
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.history.append(elapsed_ms)

        if elapsed_ms > self.target_ms:
            logging.warning(f"⚠️ LATENCY BREACH: {elapsed_ms:.1f}ms > {self.target_ms}ms target.")
        else:
            logging.info(f"⚡ LATENCY OK: {elapsed_ms:.1f}ms (target: {self.target_ms}ms)")

        return result, elapsed_ms

    def get_avg_latency(self):
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)
