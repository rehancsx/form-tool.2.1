"""
==========================================
                FORM-TOOL
==========================================
A simple local web form to collect basic
contact information (name, email, address,
city, country) and save it to data.txt.

Runs a local server on your own machine.
No data leaves your device.
==========================================
"""

import http.server
import socketserver
import urllib.parse
from datetime import datetime

PORT = 8000
DATA_FILE = "data.txt"

RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

BANNER = r"""
 _____ ___  ____  __  __       _____ ___   ___  _     
|  ___/ _ \|  _ \|  \/  |     |_   _/ _ \ / _ \| |    
| |_ | | | | |_) | |\/| |______| || | | | | | | |    
|  _|| |_| |  _ <| |  | |______| || |_| | |_| | |___ 
|_|   \___/|_| \_\_|  |_|      |_| \___/ \___/|_____|
"""

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Contact Information Form</title>
<style>
  body {
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    display: flex;
    justify-content: center;
    padding: 40px 15px;
  }
  .card {
    background: #fff;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 420px;
  }
  h2 {
    text-align: center;
    color: #c0392b;
    margin-bottom: 20px;
  }
  label {
    display: block;
    margin-top: 12px;
    font-weight: bold;
    font-size: 14px;
    color: #333;
  }
  input {
    width: 100%;
    padding: 8px;
    margin-top: 4px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
  }
  button {
    width: 100%;
    margin-top: 20px;
    padding: 10px;
    background: #c0392b;
    color: #fff;
    border: none;
    border-radius: 5px;
    font-size: 15px;
    cursor: pointer;
  }
  button:hover {
    background: #a93226;
  }
</style>
</head>
<body>
  <div class="card">
    <h2>Contact Information</h2>
    <form method="POST" action="/submit">
      <label>First Name</label>
      <input type="text" name="first_name" required>

      <label>Last Name</label>
      <input type="text" name="last_name" required>

      <label>Email</label>
      <input type="email" name="email" required>

      <label>Address</label>
      <input type="text" name="address" required>

      <label>City</label>
      <input type="text" name="city" required>

      <label>Province / State</label>
      <input type="text" name="province">

      <label>Country</label>
      <input type="text" name="country" required>

      <button type="submit">Submit</button>
    </form>
  </div>
</body>
</html>
"""

THANK_YOU_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Thank You</title>
<style>
  body { font-family: Arial, sans-serif; background: #f4f4f4;
         display: flex; justify-content: center; align-items: center;
         height: 100vh; margin: 0; }
  .box { background: #fff; padding: 30px; border-radius: 10px;
         box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
  h2 { color: #27ae60; }
</style>
</head>
<body>
  <div class="box">
    <h2>Thank you!</h2>
    <p>Your information has been submitted successfully.</p>
  </div>
</body>
</html>
"""


class FormHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Keep the terminal clean; skip default request logging
        pass

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_FORM.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/submit":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            fields = urllib.parse.parse_qs(body)

            first_name = fields.get("first_name", [""])[0]
            last_name = fields.get("last_name", [""])[0]
            email = fields.get("email", [""])[0]
            address = fields.get("address", [""])[0]
            city = fields.get("city", [""])[0]
            province = fields.get("province", [""])[0]
            country = fields.get("country", [""])[0]

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            entry = (
                f"----- Submitted: {timestamp} -----\n"
                f"First Name : {first_name}\n"
                f"Last Name  : {last_name}\n"
                f"Email      : {email}\n"
                f"Address    : {address}\n"
                f"City       : {city}\n"
                f"Province   : {province}\n"
                f"Country    : {country}\n\n"
            )

            with open(DATA_FILE, "a", encoding="utf-8") as f:
                f.write(entry)

            print(f"{RED}[+] New submission saved from {first_name} {last_name} ({email}){RESET}")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(THANK_YOU_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def main():
    print(f"{RED}{BOLD}{BANNER}{RESET}")
    print(f"{RED}Please use for legal activities only.{RESET}")
    print(f"{RED}This tool is for educational purposes only. We are not responsible for misuse.{RESET}")
    print()

    choice = input("Do you want to generate a link for your form? (y/n): ").strip().lower()

    if choice != "y":
        print("Exiting. Goodbye!")
        return

    with socketserver.TCPServer(("127.0.0.1", PORT), FormHandler) as httpd:
        print(f"\nYour form is ready. Open this link in your browser:")
        print(f"{BOLD}http://127.0.0.1:{PORT}{RESET}")
        print(f"\nSubmitted data will be saved to: {DATA_FILE}")
        print("Press Ctrl+C to stop the server.\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped. Goodbye!")


if __name__ == "__main__":
    main()
