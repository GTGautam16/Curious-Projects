# Learning Notes: Python Web Server From Scratch

## 1. What this project is about

This project is a small web server built in Python to understand how the web works at a low level. Instead of using a big framework, the server is built step by step using Python’s standard library. That makes the main ideas easier to see:

* how a browser sends a request
* how the server finds a file on disk
* how the server sends the response back
* how directory listing works
* how dynamic Python scripts can run through CGI
* how to keep the code clean using classes and inheritance

The goal is not only to make the server work, but also to understand the logic behind it.

## 2. Big picture: how a request moves

When a user opens a URL like `http://localhost:8080/GT_Resume.pdf`, the browser sends a request to the server. The server then:

1. reads the URL path
2. converts it into a file path on the computer
3. checks what kind of thing it is
4. decides which class should handle it
5. sends the result back to the browser

This flow is the heart of the whole project.

## 3. Core networking ideas

### IP address

An IP address is like the address of a house. It tells the network which machine should receive the data.

### Port number

A port is like a room number or extension number inside that machine. A single computer can run many programs, so the port tells the system which program should receive the request.

### Socket

A socket combines the IP address and port number. It is the full connection point used for communication.

### HTTP

HTTP is the language browsers and servers use to talk. A browser might send a request like:

```http
GET /GT_Resume.pdf HTTP/1.1
Host: localhost:8080
```

The server must understand this request, find the file, and send the correct response.

## 4. Why classes were used

At first, the server logic can be written using many `if`, `elif`, and `else` statements. That works for a small program, but it becomes hard to read and hard to extend.

To improve that, the project uses the **Chain of Responsibility** design pattern.

This means:

* each class handles one specific job
* the main server asks each class in order
* the first class that matches handles the request
* if no class matches, the server shows an error

This makes the program easier to expand later.

## 5. The case-handler idea

Each request is passed through a list of case classes.

### `case_no_file`

This class checks whether the requested file or folder exists.

If it does not exist, the class handles the request by raising an error.

Important idea:

```python
return not os.path.exists(handler.full_path)
```

* `os.path.exists(...)` returns `False` when the file is missing
* `not False` becomes `True`
* that means this class says, “Yes, this request is mine to handle”

So the `not` operator flips the result and helps the server move into the error path.

### `case_existing_file`

This class checks whether the requested path is a normal file.

If the path points to a PDF, image, HTML file, or other file, this class serves it.

### `case_directory_index_file`

This class checks whether the path is a folder that contains `index.html`.

If yes, the server opens and serves that file instead of showing the folder name.

### `case_directory_no_index_file`

This class checks whether the path is a folder but does not contain `index.html`.

If yes, the server builds a directory listing page.

### `case_cgi_file`

This class checks whether the requested file is a Python script.

If the file ends in `.py`, the server runs it and sends the printed output back to the browser.

### `case_always_fail`

This is the backup class.

If nothing else matches, this class throws an error.

## 6. Why the order of cases matters

The order of the case list is important.

For example:

* if `case_existing_file` comes before `case_cgi_file`, then a `.py` file may be treated like a normal file
* if `case_no_file` comes first, missing files are caught early
* if `case_directory_index_file` comes before `case_directory_no_index_file`, the server can show a welcome page when available

So the case order is part of the logic.

## 7. Directory listing and list comprehension

When the server opens a folder without `index.html`, it needs to show the files inside it.

The code often looks like this:

```python
bullets = ["<li><a href='{0}/{1}'>{1}</a></li>".format(self.path.rstrip('/'), e)
           for e in entries if not e.startswith('.')]
```

This is called a **list comprehension**.

A list comprehension is a short way to build a list.

To read it, break it into 3 parts:

### 1. Loop

`for e in entries`

This means: go through every item in the folder.

### 2. Condition

`if not e.startswith('.')`

This means: ignore hidden files that begin with a dot.

### 3. Action

`"<li><a href=...>".format(...)`

This means: make each file name into a clickable HTML link.

So the whole line means:

> Build a new list of HTML links from the folder items, but only include visible files.

## 8. How to read a list comprehension slowly

When reading a comprehension, do not read it all at once.

Read it like this:

1. Find the loop in the middle
2. Check the filter on the right
3. Read the output on the left

That makes it much easier to understand.

## 9. CGI protocol

CGI means **Common Gateway Interface**.

It is a way for a web server to run an external program and send the output back to the browser.

This is useful when the page must be generated dynamically.

For example, a Python script can print the current time into HTML:

```python
from datetime import datetime
print("<html>")
print("<body>")
print(f"<p>Generated {datetime.now()}</p>")
print("</body>")
print("</html>")
```

The server can run this script, capture what it prints, and send that result to the browser.

## 10. Why CGI is powerful

CGI allows the server to do more than serve saved files.

It can:

* generate live content
* show current time
* calculate values
* respond to user input
* display different output each time

That is why CGI is an important idea in web systems.

## 11. Security warning for CGI

Running any `.py` file from a URL is dangerous.

Why?

Because if the server runs random scripts without checking them, someone could accidentally or intentionally run harmful code.

That is why real servers use strict rules, safe folders, and permission checks.

For learning, CGI helps explain the concept. For production, it must be secured properly.

## 12. Refactoring with inheritance

As the project grew, the code started to repeat itself.

For example:

* several case classes needed file handling
* several classes needed `index.html` path logic
* some helper methods belonged in more than one place

To solve this, a parent class called `base_case` was created.

A parent class is like a toolbox. Child classes can inherit shared methods from it.

### Example

* `handle_file()` can be shared by many case classes
* `index_path()` can be shared by directory-related cases

This keeps the code cleaner and easier to maintain.

## 13. What `assert False, 'Not implemented.'` means

Inside the parent class, the methods `test()` and `act()` may contain:

```python
assert False, 'Not implemented.'
```

This is a warning.

It means:

* this method is only a placeholder
* every child class must write its own version
* if a child forgets, the program should fail loudly

That is useful because it prevents silent mistakes.

## 14. How to think about the whole project

The project can be seen as a small decision machine.

### Request arrives

Browser sends a URL.

### Server builds a path

The server combines the current folder with the requested path.

### Server checks each case

Each case class tests whether it can handle the request.

### One case wins

The first matching case performs the action.

### Response is sent

The server sends either:

* a file
* a directory listing
* CGI output
* an error page

## 15. How to test the server

You can test the server using these cases:

### Test 1: Normal file

Open a real file like `GT_Resume.pdf`.

Expected result:

* file opens in browser or PDF viewer

### Test 2: Missing file

Open a fake name.

Expected result:

* custom 404 error page

### Test 3: Folder without `index.html`

Open a folder.

Expected result:

* directory listing appears

### Test 4: Folder with `index.html`

Put `index.html` inside the folder and open it again.

Expected result:

* the index page opens instead of the folder listing

### Test 5: CGI script

Open a `.py` file.

Expected result:

* the script runs and its output appears in the browser

## 16. What I learned from this project

This project taught me more than just Python syntax.

It taught me:

* how a browser talks to a server
* why file paths matter
* how errors should be handled cleanly
* how to use classes to keep logic organized
* how to think in reusable pieces
* how to explain code in a human way

## 17. Suggested repository structure

```text
Curious-Projects/
├── README.md
├── learning_notes.md
├── server.py
├── time_script.py
├── test_page.html
└── LICENSE
```

### What each file is for

* `README.md`: project overview and quick start
* `learning_notes.md`: deep explanation for learning
* `server.py`: main server code
* `time_script.py`: CGI demo script
* `test_page.html`: sample HTML file
* `LICENSE`: permission and reuse rules

## 18. Best GitHub repository description

A good repo description should sound curious, technical, and positive.

Example:

**"A collection of curiosity-driven engineering projects exploring how systems work under the hood."**

Other options:

* **"Curiosity-led projects built to understand the mechanics behind real-world software systems."**
* **"A hands-on playground for experimenting, breaking, rebuilding, and understanding engineering systems."**
* **"Engineer-minded explorations of code, systems, and the ideas that power them."**

## 19. Final note

This project is a good example of learning by building.

It starts from simple file serving, grows into directory handling, then reaches dynamic execution through CGI, and finally becomes cleaner through inheritance and refactoring.

That is exactly how real engineering growth looks: start simple, understand deeply, then improve structure step by step.
