import os

def get_env_id(string_name: str) -> int:
  return int(os.getenv(string_name))