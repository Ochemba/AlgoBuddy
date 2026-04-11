# supabase_client.py - Supabase client initialization
import os
import time
import streamlit as st
from functools import wraps
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Try secrets first, then environment
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_ANON_KEY = st.secrets["SUPABASE_ANON_KEY"]
except (KeyError, AttributeError, FileNotFoundError):
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
# Custom error messages
ERROR_MESSAGES = {
    "network": " No internet connection. Please check your network and try again.",
    "timeout": "Connection timed out. Server is taking too long to respond.",
    "ssl": " Secure connection failed. Please check your network.",
    "auth": " Authentication failed. Please log in again.",
    "permission": " You don't have permission to perform this action.",
    "not_found": " Requested data not found.",
    "rate_limit": " Too many requests. Please wait a moment.",
    "connection": " Cannot connect to server. Please check your internet.",
}

def get_user_friendly_error(error: Exception) -> str:
    """Convert technical error to user-friendly message."""
    error_str = str(error).lower()
    
    for key, message in ERROR_MESSAGES.items():
        if key in error_str:
            return message
    
    return f"❌ Something went wrong: {str(error)[:100]}"

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
                        "network", "timeout", "connection", "ssl", "rate_limit"
                    ])
                    
                    if not is_network_error or attempt == max_retries:
                        # Don't retry on non-network errors or after last attempt
                        break
                    
                    # Show retry message (only on first attempt)
                    if attempt == 0:
                        st.warning(f"⚠️ {get_user_friendly_error(e)} Retrying...")
                    
                    # Wait before retry
                    time.sleep(current_delay)
                    current_delay *= backoff  # Increase delay for next retry
            
            # All retries failed, show final error
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
        if "network" in error_str or "timeout" in error_str or "connection" in error_str:
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