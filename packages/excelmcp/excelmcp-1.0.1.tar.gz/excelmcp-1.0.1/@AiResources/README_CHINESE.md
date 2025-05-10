# ExcelMCP

ExcelMCP server is designed for AI to Automate Microsoft Excel Application in Windows OS. Not working on Linux/MacOS.

## Installation
There are two ways or two modes to install ExcelMCP (They also can be used in the same time):

### 1. User ExcelMCP as stdio server: 
- One ExcelMCP server for One MCP Client mode
- Put following setting to MCP.json file for vscode or some proper place for other AI IDE:

```json
{
    "servers": {
        "ExcelMCP": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "excelmcp"
            ]
        }
    }
}
```

### 2. User ExcelMCP as sse server: 
- One ExcelMCP server for multi MCP Client mode
- You can change port and host as you like
#### step 1:  
**Run one command in shell or power shell:**
>uvx excelmcp sse

With "url": "http//127.0.0.1:8000/sse"

or
>uvx excelmcp sse --port 8009

or
>uvx excelmcp sse 8009

or
>uvx excelmcp sse --port 8009 --host 127.0.0.1

With "url": "http//127.0.0.1:8009/sse"
#### setp 2: 
**Put following setting to MCP.json file for vscode or some proper place for other AI IDE:**

```json
{
    "servers": {
        "ExcelMCP": {
            "url": "http//127.0.0.1:8009/sse"
        }
    }
}
```
## Usage
On AI IDE, you can ask AI modle to control Excel Application by ExcelMCP server:
- You ask AI modle to open a new Excel Application.
    AI modle will send a request to ExcelMCP server, and ExcelMCP server will open a new Excel Application.

- You ask AI modle to do whatever you want to do in the current Excel Application.
    AI modle will analye your request, and call ExcelMCP server's tool to accomplish your request.

## Tools Reference
Tools:
- Installed(): chedk if Excel Application is installed on your computer.
- Launch(...): launch a new Excel Application and set it's visibility.
- Visible(): set the current Excel Application's visibility to True or False.
- Quit(): quit the current Excel Application.
- WorkBook(BookPath:=None): create a new Excel WorkBook if BootPath is None or empty and open or save an Excel WorkBook as the BookPath refer to.
- There're some other tools not mentioned here.

- RunPython(...): run python code in the current Excel Application.
    - This is most powerful tool in ExcelMCP server. AI can use this tool to do whatever you want to do in the current Excel Application.
    - There's an Global variable named class instance "The" in the python code, "The.Excel" hold the current Excel Application, 
    - The openpyxl library is imported in the python code, so you can use openpyxl to manipulate excel files.

- More other tools will be added in the future.


## Development
```bash
git clone https://github.com/officemcp/excelmcp
```