# supabase_client.py - Supabase client initialization
import os
import time
import streamlit as st
from functools import wraps
from supabase import create_client, Client
from dotenv import load_dotenv

# ============================================
# FIX: Get Supabase credentials from Streamlit secrets OR environment
# ============================================

def get_supabase_url():
    """Get Supabase URL from st.secrets or environment variable."""
    try:
        return st.secrets["SUPABASE_URL"]
    except (FileNotFoundError, KeyError, AttributeError):
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        if url:
            return url
        else:
            st.error("🔌 Supabase URL not found! Please add it to your secrets.")
            st.stop()

def get_supabase_anon_key():
    """Get Supabase anon key from st.secrets or environment variable."""
    try:
        return st.secrets["SUPABASE_ANON_KEY"]
    except (FileNotFoundError, KeyError, AttributeError):
        load_dotenv()
        key = os.getenv("SUPABASE_ANON_KEY")
        if key:
            return key
        else:
            st.error("🔑 Supabase anon key not found! Please add it to your secrets.")
            st.stop()

# Get credentials
SUPABASE_URL = get_supabase_url()
SUPABASE_ANON_KEY = get_supabase_anon_key()

# Custom error messages
ERROR_MESSAGES = {
    "network": "🌐 No internet connection. Please check your network and try again.",
    "timeout": "⏰ Connection timed out. The server is taking too long to respond.",
    "ssl": "🔒 Secure connection failed. Please check your network/proxy settings.",
    "auth": "🔑 Authentication failed. Please log in again.",
    "permission": "🚫 You don't have permission to perform this action.",
    "not_found": "🔍 Requested data not found.",
    "rate_limit": "🐌 Too many requests. Please wait a moment.",
    "connection": "📡 Cannot connect to server. Please check your internet.",
    "getaddrinfo failed": "🌐 No internet connection. Please check your Wi-Fi or mobile data.",
}

def get_user_friendly_error(error: Exception) -> str:
    """Convert technical error to user-friendly message."""
    error_str = str(error).lower()
    
    for key, message in ERROR_MESSAGES.items():
        if key in error_str:
            return message
    
    return f"❌ Something went wrong: {str(error)[:100]}"

# ============================================
# RETRY DECORATOR
# ============================================

def retry_on_error(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry a function on failure.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay increase after each retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    error_str = str(e).lower()
                    
                    # Only retry on network-related errors
                    is_network_error = any(keyword in error_str for keyword in [
                        "network", "timeout", "connection", "ssl", "rate_limit", "getaddrinfo"
                    ])
                    
                    if not is_network_error or attempt == max_retries:
                        break
                    
                    if attempt == 0:
                        st.warning(f"⚠️ {get_user_friendly_error(e)} Retrying...")
                    
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            st.error(get_user_friendly_error(last_error))
            return None
        return wrapper
    return decorator

def get_supabase_client() -> Client:
    """Get authenticated Supabase client with error handling."""
    try:
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            st.error("🔌 Configuration error: Missing Supabase credentials")
            return None
        
        return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    except Exception as e:
        st.error(get_user_friendly_error(e))
        return None

def check_connection() -> bool:
    """Test if Supabase connection is working."""
    try:
        client = get_supabase_client()
        if client is None:
            return False
        client.table("user_progress").select("count").limit(1).execute()
        return True
    except Exception as e:
        error_str = str(e).lower()
        if "network" in error_str or "timeout" in error_str or "connection" in error_str or "getaddrinfo" in error_str:
            st.warning("⚠️ You're offline. Progress will sync when reconnected.")
        return False

# Singleton instance
_supabase = None

def supabase():
    """Get Supabase client instance (singleton)."""
    global _supabase
    if _supabase is None:
        _supabase = get_supabase_client()
    return _supabase