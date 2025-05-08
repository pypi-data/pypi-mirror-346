***Some tool.***

# Install
>>> pip install htyy

# request
>>> from htyy import request
>>> response = request.get('https://www.example.com', timeout=5)
>>> print(response.text)

Print out the content you get and decode.

# message
>>> from htyy import message
>>> message.showinfo("title","message")

A tooltip box appears.

# path
About the content of the path.

# ...