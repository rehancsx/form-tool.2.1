# Form-Tool

A simple local web server that displays a contact information form (First Name, Last Name, Email, Address, City, Province, Country) in the browser and saves submissions to `data.txt`.

## ⚠️ Disclaimer

This tool is intended for **educational purposes only**. Please use it for legal activities only. The author is not responsible for any misuse of this tool.

This tool runs **only on localhost (127.0.0.1)** — it is not designed or intended to be exposed to the public internet. It is meant for collecting information from people you interact with directly (e.g. onboarding a team member, a client, a collaborator) with their full knowledge and consent.

## Features

- Simple, clean HTML contact form served locally
- Collects: First Name, Last Name, Email, Address, City, Province, Country
- Submitted data is saved to `data.txt` with a timestamp
- No external dependencies — uses only the Python standard library
- Works on Linux, macOS, and Termux (Android)

## Requirements

- Python 3.x

## Usage

```bash
python3 form-tool.py
```

1. The tool will show a banner and a short disclaimer
2. It will ask: `Do you want to generate a link for your form? (y/n)`
   - `n` — exits immediately
   - `y` — starts a local server and gives you a link: `http://127.0.0.1:8000`
3. Open that link in a browser to see and fill out the form
4. On submit, the data is appended to `data.txt` in the same folder
5. Press `Ctrl+C` to stop the server

## Important Notes

- The server only binds to `127.0.0.1` (localhost), so it is only reachable from the same device it runs on.
- Always inform anyone filling out this form what the information will be used for.
- Do not modify this tool to bind to a public address or tunnel it (e.g. via ngrok/Cloudflare Tunnel) to collect data from people without their knowledge or consent.

## License

This project is released under the [MIT License](LICENSE).
