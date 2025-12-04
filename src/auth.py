"""
Authentication Module for API Key Management.
Handles key generation, hashing, and validation.
"""
import secrets
import hashlib
import sqlite3
from datetime import datetime
from src.storage import DB_PATH

def generate_api_key():
    """
    Generate a secure random API key.
    Format: sk_live_<32_random_hex_chars>
    """
    return f"sk_live_{secrets.token_hex(16)}"

def hash_key(api_key):
    """
    Create a SHA-256 hash of the API key for secure storage.
    """
    return hashlib.sha256(api_key.encode()).hexdigest()

def create_api_key(owner_name, tier="free"):
    """
    Generate a new API key, hash it, and store it in the database.
    Returns the raw API key (show this to the user only once!).
    """
    raw_key = generate_api_key()
    hashed_key = hash_key(raw_key)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO api_keys (key_hash, owner, tier, created_at, is_active)
            VALUES (?, ?, ?, ?, ?)
        """, (hashed_key, owner_name, tier, datetime.now().isoformat(), True))
        conn.commit()
        print(f"API Key created for {owner_name}")
        return raw_key
    except Exception as e:
        print(f"Error creating API key: {e}")
        return None
    finally:
        conn.close()

def validate_api_key(api_key):
    """
    Validate an API key against the database.
    Returns the key record if valid, None otherwise.
    """
    if not api_key:
        return None
        
    hashed_key = hash_key(api_key)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT owner, tier, is_active 
        FROM api_keys 
        WHERE key_hash = ? AND is_active = 1
    """, (hashed_key,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "owner": result[0],
            "tier": result[1],
            "is_active": bool(result[2])
        }
    return None

def get_all_keys():
    """
    Get all API keys (masked) for admin display.
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT id, owner, tier, created_at, is_active FROM api_keys ORDER BY created_at DESC", conn)
    conn.close()
    return df

if __name__ == "__main__":
    # Test
    key = create_api_key("Test User")
    print(f"Generated Key: {key}")
    print(f"Validation: {validate_api_key(key)}")
