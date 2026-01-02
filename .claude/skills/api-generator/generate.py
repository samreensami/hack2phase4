import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load root .env
load_dotenv(os.path.join(os.getcwd(), '.env'))

def generate_api():
    print("Generating API Types...")

    auth_code = """
// Generated Auth API Types
export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserRead {
  id: number;
  email: string;
  created_at: string;
}

export interface UserCreate {
  email: string;
  password: string;
}
"""
    task_code = """
// Generated Task API Types
export interface TaskRead {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  status: boolean;
  category: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: boolean;
  category?: string;
}
"""

    gen_dir = Path("frontend/lib/generated")
    gen_dir.mkdir(parents=True, exist_ok=True)

    (gen_dir / "auth_types.ts").write_text(auth_code)
    (gen_dir / "task_types.ts").write_text(task_code)

    print(f"API types generated in {gen_dir}")

if __name__ == "__main__":
    generate_api()
