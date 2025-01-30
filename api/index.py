from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse

# Load the student marks data
try:
    with open("q-vercel-python.json", "r") as file:
        student_data = json.load(file)
except FileNotFoundError:
    student_data = []  # Default to an empty list if the file is not found

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        # Add CORS header
        self.send_header("Access-Control-Allow-Origin", "*")
        
        # Parse the query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get("name", [])
        
        # Fetch marks for the requested names
        marks = []
        for name in names:
            student = next((student for student in student_data if student["name"] == name), None)
            marks.append(student["marks"] if student else None)
        
        # Prepare the response
        response = {"marks": marks}
        response_json = json.dumps(response)
        
        # Send response headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Send the response body
        self.wfile.write(response_json.encode("utf-8"))

