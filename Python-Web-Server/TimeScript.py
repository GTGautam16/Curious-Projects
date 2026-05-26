from datetime import datetime

print("<html>")
print("<body style='background-color: black; color: green;'>")
print("<h1>Dynamic CGI Test</h1>")
print(f"<p>The live time is right now: <b>{datetime.now()}</b></p>")
print("</body>")
print("</html>")
