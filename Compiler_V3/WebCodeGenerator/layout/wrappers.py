import os


def html_wrapper(html_content: str) -> str:
    """Wrap HTML content in a basic HTML template."""
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>DSL Example</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
    {html_content}
    </body>
    </html>"""
def css_wrapper(css_content)->str:
    return """
    *{
  margin: 0;
}

body{
  padding: 24px;
  box-sizing: border-box;
  background-color: white;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  margin-right: 2%;
}

.row {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.box{
  width: 100%;
  background-color: rgb(227, 226, 226);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
  border-radius: 8px;
}

.button{
  padding: 12px 24px;
  background-color: grey;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
}

select, input{
  padding: 8px;
  border-radius: 8px;
  border: 1px solid black;
  background-color: white;
  outline: none;
}
.img{
height : 75px;
width : 75px;
}
    """+css_content