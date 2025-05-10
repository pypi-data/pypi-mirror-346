# insta-ui

<div align="center">

English| [简体中文](./README.md)

</div>

 
## 📖 Introduction
insta-ui is a Python-based UI library for rapidly building user interfaces.


## ⚙️ Features

Three modes are provided:

- Zero mode: Generates pure HTML files, requiring no dependencies. Simply open in a browser to run.
- Web mode: Generates web applications.
- Web view mode: Generates web view applications that can be packaged into local applications (without needing to start a web server).

 
## 📦 Installation

For zero mode:

```
pip install instaui -U
```

For web mode:

```
pip install instaui[web] -U
```

For web view mode:
```
pip install instaui[webview] -U
```



## 🖥️ Quick Start

Here's a Counter example where clicking the button will display the current count value on the button text.

zore mode:

```python
from instaui import ui, html, zero

with zero():
    count = ui.ref(0)
    text = ui.str_format("Count: {}", count)

    html.button(text).on_click(
        "()=> count.value++", bindings={"count": count}
    )

    ui.to_html("./test.html")

```

Running the above code will generate a test.html file, which you can open in a browser to see the effect.



Web mode:

```python
from instaui import ui, html

@ui.page("/")
def counter():
    count = ui.ref(0)
    text = ui.str_format("Count: {}", count)

    html.button(text).on_click("()=> count.value++", bindings={"count": count})


ui.server().run()
```

In web mode, we can define interaction functions for complex computations.

```python
from instaui import ui, html

@ui.page("/")
def counter():
    count = ui.ref(0)
    # text = ui.str_format("Count: {}", count)

    @ui.computed(inputs=[count])
    def text(count: int):
        # Any Python operation
        return f"Current Count: {count}"


    html.button(text).on_click("()=> count.value++", bindings={"count": count})


ui.server().run()
```

- The computation of `text` will generate network requests.
- Button clicks, due to using JS binding, do not require network requests.

You can choose to handle any computation with either Python or JavaScript. Below is an example of handling the button click event using Python.

```python
@ui.page("/")
def counter():
    count = ui.ref(0)

    @ui.computed(inputs=[count])
    def text(count: int):
        return f"Current Count: {count}"

    @ui.event(inputs=[count], outputs=[count])
    def add_count(count: int):
        return count + 1

    html.button(text).on_click(add_count)

```
