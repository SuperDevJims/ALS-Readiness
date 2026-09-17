from app.core.config import settings
from app.storage import build_key, get_read_url, get_upload_url, s3_client

read_url = get_read_url("test-assets/e5a45f63-7a11-4f4a-b679-9476f0992e34_math-01.png")
print("Read URL:", read_url)
