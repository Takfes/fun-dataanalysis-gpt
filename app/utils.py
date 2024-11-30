from pyprojroot import here

file_path = here("app/static/styles.css")


def load_css(file_path: str = file_path):
    with open(file_path) as f:
        css = f.read()
    return f"<style>{css}</style>"
