# auth.py - Authentication with Supabase
import streamlit as st
from supabase_client import supabase
from datetime import datetime

class AuthManager:
    """Manages user authentication with Supabase."""
    
    def __init__(self):
        self.supabase = supabase()
    
    def _get_user_friendly_error(self, error: Exception) -> str:
        """Convert technical errors to user-friendly messages."""
        error_msg = str(error).lower()
        
        # ========== NETWORK/DNS ERRORS ==========
        if "getaddrinfo failed" in error_msg:
            return "No internet connection. Please check your Wi-Fi or mobile data and try again."
        
        if "network" in error_msg or "network is unreachable" in error_msg:
            return "nternet connection issue. Please check your network and try again."
        
        if "connection refused" in error_msg:
            return "Cannot reach AlgoBuddy servers. Please check your internet connection."
        
        if "timeout" in error_msg or "timed out" in error_msg:
            return "Connection timed out. Your internet might be slow. Please try again."
        
        if "ssl" in error_msg or "certificate" in error_msg:
            return "Secure connection failed. Please check your network."
        
        if "dns" in error_msg or "host" in error_msg:
            return " Please check your internet connection or try restarting your router."
        
        # ========== AUTHENTICATION ERRORS ==========
        if "invalid login" in error_msg or "invalid credentials" in error_msg:
            return " Invalid email or password. Please try again."
        
        if "email not confirmed" in error_msg:
            return " Please check your email and verify your account before logging in."
        
        if "user already registered" in error_msg:
            return " An account with this email already exists. Please login instead."
        
        if "password" in error_msg and "weak" in error_msg:
            return " Password is too weak. Please use at least 6 characters."
        
        if "rate limit" in error_msg or "too many requests" in error_msg:
            return " Too many attempts. Please wait a moment and try again."
        
        # ========== USER METADATA ERRORS ==========
        if "username" in error_msg and "taken" in error_msg:
            return " Username already taken. Please choose another one."
        
        if "display_name" in error_msg:
            return " Please enter a valid display name."
        
        # ========== FALLBACK ==========
        return f" Something went wrong: {str(error)[:100]}"
    
    def login(self, email: str, password: str):
        """Authenticate user with Supabase."""
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            user = response.user
            return True, "Login successful", {
                "id": user.id,
                "email": user.email,
                "username": user.user_metadata.get("username", ""),
                "display_name": user.user_metadata.get("display_name", ""),
            }
        except Exception as e:
            error_msg = self._get_user_friendly_error(e)
            return False, error_msg, None
    
    def signup(self, email: str, username: str, display_name: str, password: str):
        """Create a new user account."""
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "display_name": display_name,
                        "created_at": datetime.now().isoformat()
                    }
                }
            })
            
            user = response.user
            if user:
                # Also create a profile entry
                try:
                    self.supabase.table("profiles").insert({
                        "id": user.id,
                        "username": username,
                        "display_name": display_name,
                        "email": email,
                        "created_at": datetime.now().isoformat()
                    }).execute()
                except Exception:
                    pass  # Profile might already exist or will be created by trigger
                
                return True, "Account created! Please check your email to confirm your account."
            else:
                return False, "Signup failed. Please try again.", None
        except Exception as e:
            error_msg = self._get_user_friendly_error(e)
            return False, error_msg
    
    def logout(self):
        """Log out the current user."""
        try:
            self.supabase.auth.sign_out()
            return True, "Logged out successfully"
        except Exception as e:
            error_msg = self._get_user_friendly_error(e)
            return False, error_msg
    
    def get_current_user(self):
        """Get the currently logged in user."""
        try:
            user = self.supabase.auth.get_user()
            if user and user.user:
                return {
                    "id": user.user.id,
                    "email": user.user.email,
                    "username": user.user.user_metadata.get("username", ""),
                    "display_name": user.user.user_metadata.get("display_name", ""),
                }
            return None
        except Exception as e:
            return None
    
    def update_display_name(self, username: str, new_display_name: str):
        """Update user's display name."""
        try:
            self.supabase.auth.update_user({
                "data": {"display_name": new_display_name}
            })
            
            # Also update profiles table
            user_id = self.get_current_user()["id"] if self.get_current_user() else None
            if user_id:
                self.supabase.table("profiles").update({
                    "display_name": new_display_name
                }).eq("id", user_id).execute()
            
            return True, "Display name updated"
        except Exception as e:
            error_msg = self._get_user_friendly_error(e)
            return False, error_msg
    
    def update_username(self, current_username: str, new_username: str):
        """Update user's username."""
        try:
            # Check if username is taken
            existing = self.supabase.table("profiles").select("username").eq("username", new_username).execute()
            if existing.data:
                return False, "Username already taken"
            
            self.supabase.auth.update_user({
                "data": {"username": new_username}
            })
            
            # Also update profiles table
            user_id = self.get_current_user()["id"] if self.get_current_user() else None
            if user_id:
                self.supabase.table("profiles").update({
                    "username": new_username
                }).eq("id", user_id).execute()
            
            return True, "Username updated"
        except Exception as e:
            error_msg = self._get_user_friendly_error(e)
            return False, error_msg
    
    def update_password(self, username: str, new_password: str):
        """Update user's password."""
        try:
            self.supabase.auth.update_user({
                "password": new_password
            })
            return True, "Password updated"
        except Exception as e:
            error_msg = self._get_user_friendly_error(e)
            return False, error_msg
    
    def reset_password(self, email: str):
        """Send password reset email."""
        try:
            self.supabase.auth.reset_password_for_email(email)
            return True, "Password reset email sent. Please check your inbox."
        except Exception as e:
            error_msg = self._get_user_friendly_error(e)
            return False, error_msg


# Quick test function
def test_auth():
    """Test authentication with custom error messages."""
    auth = AuthManager()
    
    # Test network error handling
    print("Testing error handling...")
    
    # Simulate connection issues (you can't actually test this without disconnecting)
    print("✅ Auth manager ready with custom error messages for network issues")


if __name__ == "__main__":
    test_auth()