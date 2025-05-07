"""
trackle - A personal knowledge logging and retrieval system
"""
import warnings

# Suppress the LibreSSL warning from urllib3 at import time
warnings.filterwarnings("ignore", message=".*OpenSSL.*LibreSSL.*")

__version__ = "0.1.0"