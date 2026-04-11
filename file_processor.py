# file_processor.py — Extract content from uploaded files

import base64
import io
import uuid
from datetime import datetime
from typing import Optional


# ── PDF ───────────────────────────────────────────────────────────────────────

def extract_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        return "\n\n".join(text_parts).strip()
    except ImportError:
        return "[PDF extraction failed: install pdfplumber]"
    except Exception as e:
        return f"[PDF extraction error: {e}]"


# ── DOCX ──────────────────────────────────────────────────────────────────────

def extract_docx(file_bytes: bytes) -> str:
    """Extract all text from a Word document."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs).strip()
    except ImportError:
        return "[DOCX extraction failed: install python-docx]"
    except Exception as e:
        return f"[DOCX extraction error: {e}]"


# ── IMAGE ─────────────────────────────────────────────────────────────────────

def encode_image(file_bytes: bytes, filename: str) -> dict:
    """Encode image as base64 for OpenAI vision API."""
    ext = filename.rsplit(".", 1)[-1].lower()
    media_type_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }
    media_type = media_type_map.get(ext, "image/png")
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    return {"base64": b64, "media_type": media_type, "filename": filename}


# ── SUPABASE STORAGE FUNCTIONS ────────────────────────────────────────────────

def save_file_to_db(user_id: str, filename: str, file_type: str, content: str = None) -> Optional[dict]:
    """Save uploaded file reference to Supabase"""
    if not user_id:
        return None
    
    try:
        from supabase_client import supabase
        
        file_id = str(uuid.uuid4())
        data = {
            "id": file_id,
            "user_id": user_id,
            "filename": filename,
            "file_type": file_type,
            "content": content[:10000] if content else None,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase().table("uploaded_files").insert(data).execute()
        return {"file_id": file_id}
    except Exception as e:
        print(f"Error saving file to DB: {e}")
        return None


def get_user_files(user_id: str) -> list:
    """Get all files uploaded by a user"""
    if not user_id:
        return []
    
    try:
        from supabase_client import supabase
        result = supabase().table("uploaded_files").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        print(f"Error loading files: {e}")
        return []


def delete_file_from_db(user_id: str, file_id: str) -> bool:
    """Delete a file from Supabase"""
    if not user_id or not file_id:
        return False
    
    try:
        from supabase_client import supabase
        supabase().table("uploaded_files").delete().eq("user_id", user_id).eq("id", file_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


# ── MAIN ENTRY POINT ─────────────────────────────────────────────────────────

def process_upload(uploaded_file, user_id: str = None) -> dict:
    """
    Process a Streamlit UploadedFile object.
    ALWAYS returns a dictionary.
    """
    # Always return a dictionary, never None
    if uploaded_file is None:
        return {"type": None, "error": "No file provided", "filename": None, "content": None, "image_data": None, "file_id": None}

    filename = uploaded_file.name
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    raw_bytes = uploaded_file.read()

    # PDF files
    if ext == "pdf":
        text = extract_pdf(raw_bytes)
        error = None if not text.startswith("[") else text
        
        result = {
            "type": "text",
            "filename": filename,
            "content": text if not error else "",
            "image_data": None,
            "file_id": None,
            "error": error,
        }
        
        if user_id and not error:
            saved = save_file_to_db(user_id, filename, "pdf", content=text[:10000])
            if saved:
                result["file_id"] = saved["file_id"]
        
        return result

    # DOCX files
    elif ext in ("docx", "doc"):
        text = extract_docx(raw_bytes)
        error = None if not text.startswith("[") else text
        
        result = {
            "type": "text",
            "filename": filename,
            "content": text if not error else "",
            "image_data": None,
            "file_id": None,
            "error": error,
        }
        
        if user_id and not error:
            saved = save_file_to_db(user_id, filename, "docx", content=text[:10000])
            if saved:
                result["file_id"] = saved["file_id"]
        
        return result

    # Image files
    elif ext in ("jpg", "jpeg", "png", "gif", "webp"):
        image_data = encode_image(raw_bytes, filename)
        
        result = {
            "type": "image",
            "filename": filename,
            "content": "",
            "image_data": image_data,
            "file_id": None,
            "error": None,
        }
        
        if user_id:
            saved = save_file_to_db(user_id, filename, "image", content=image_data.get("base64", ""))
            if saved:
                result["file_id"] = saved["file_id"]
        
        return result

    # Unsupported file type
    else:
        return {
            "type": None,
            "filename": filename,
            "content": None,
            "image_data": None,
            "file_id": None,
            "error": f"Unsupported file type: .{ext}",
        }


def truncate_context(text: str, max_chars: int = 6000) -> str:
    """Trim extracted text to avoid blowing the context window."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[... content truncated to fit context window ...]"