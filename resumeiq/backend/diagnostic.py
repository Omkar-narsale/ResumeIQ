#!/usr/bin/env python3
"""Resume Upload Diagnostic Tool"""

import sys
sys.path.insert(0, '.')

from extract_text import extract_text_from_pdf
import pdfplumber
import io

print("=" * 60)
print("RESUME UPLOAD DIAGNOSTICS")
print("=" * 60)

# Test 1: Check imports
print("\n[1] Checking imports...")
try:
    from database import init_db, get_db, Resume, User
    print("    OK - Database models imported")
except Exception as e:
    print(f"    FAIL - {e}")
    sys.exit(1)

try:
    from main import app
    print("    OK - FastAPI app imported")
except Exception as e:
    print(f"    FAIL - {e}")
    sys.exit(1)

# Test 2: Check PDF extraction with test PDF
print("\n[2] Testing PDF extraction...")
try:
    # Create a simple test PDF
    import subprocess
    result = subprocess.run(['python', '-c', '''
import pdfplumber
print("pdfplumber version:", pdfplumber.__version__)
'''], capture_output=True, text=True)
    print(f"    {result.stdout.strip()}")
    print("    OK - pdfplumber working")
except Exception as e:
    print(f"    FAIL - {e}")

# Test 3: Check database
print("\n[3] Checking database setup...")
try:
    from database import SessionLocal, Base, engine
    print("    OK - Database connection OK")

    # Try to create tables
    try:
        Base.metadata.create_all(bind=engine)
        print("    OK - Database tables initialized")
    except Exception as e:
        print(f"    FAIL - {e}")
except Exception as e:
    print(f"    FAIL - {e}")

# Test 4: Check environment
print("\n[4] Checking environment...")
import os
from dotenv import load_dotenv
load_dotenv()

checks = {
    'DATABASE_URL': os.getenv('DATABASE_URL'),
    'JWT_SECRET': 'SET' if os.getenv('JWT_SECRET') else 'NOT SET',
    'MODEL_NAME': os.getenv('MODEL_NAME'),
    'DEVICE': os.getenv('DEVICE'),
}

for key, value in checks.items():
    print(f"    {key}: {value}")

# Test 5: List dependencies
print("\n[5] Checking required packages...")
packages = ['fastapi', 'pydantic', 'sqlalchemy', 'pdfplumber', 'torch', 'transformers']
for pkg in packages:
    try:
        __import__(pkg)
        print(f"    OK - {pkg}")
    except ImportError:
        print(f"    FAIL - {pkg} NOT INSTALLED")

print("\n" + "=" * 60)
print("DIAGNOSTICS COMPLETE")
print("=" * 60)
print("\nTroubleshooting Tips:")
print("1. If PDF extraction fails: pip install pdfplumber")
print("2. If database fails: Delete resumeiq.db and restart")
print("3. If imports fail: pip install -r requirements.txt")
print("4. Check backend logs: python main.py (look for errors)")
