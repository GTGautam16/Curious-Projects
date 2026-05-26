# 🌐 Python Web Server from Scratch

## 📌 Problem Statement
Modern web frameworks (like Django or Next.js) abstract away the underlying mechanics of how computers communicate over the internet. The goal of this project was to peel back those layers and build a fully functional HTTP web server entirely from scratch using Python's standard library. 

Instead of relying on black-box tools, this project demonstrates a deep understanding of TCP/IP sockets, HTTP request parsing, status codes, and server-side routing.

## ✨ Core Features Built
* **Static File Serving:** Intelligently reads and serves local files (HTML, PDF, images) in binary mode, automatically attaching the correct MIME types to HTTP headers.
* **Directory Listing:** Dynamically generates an HTML bulleted list of folder contents if no `index.html` file is present.
* **The CGI Protocol:** Executes external Python scripts dynamically in a subprocess and routes the printed output directly back to the client's browser.
* **Custom Error Handling:** Actively intercepts missing files or bad requests and serves custom 404 Error HTML pages instead of crashing.
* **Firewall Tunneling:** Successfully configured to route local traffic to the public internet using Ngrok for global accessibility.

## 🧠 Technical Architecture & Refactoring
Initially, the server relied on nested `if/else` statements for routing. To make the system extensible, I refactored the codebase using the **Chain of Responsibility** design pattern. 

Requests are now passed down an object-oriented assembly line of specialized "Case Handlers" (e.g., `case_existing_file`, `case_cgi_file`). Each handler inherits from a `base_case` class, ensuring clean, modular code where new routing features can be added without modifying the core server logic.

## 🚀 How to Run the Server

1. Clone this repository to your local machine.
2. Open a terminal in the project directory.
3. Start the server by running:
   ```bash
   python server.py
