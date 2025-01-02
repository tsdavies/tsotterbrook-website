from dotenv import load_dotenv
import os

load_dotenv()

print(os.environ.get('MAIL_PASSWORD'))  # Should print the full password
