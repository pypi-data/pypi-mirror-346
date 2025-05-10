import excelmcp as mcp
import openpyxl
mcp.Visible(True)
mcp.Demostrate()
def test():
    if mcp.Installed():
        print("Excel is installed")
    else:
        print("Excel is not installed")
    try:
        mcp.Launch(False)
        print(mcp.Demostrate())
        #mcp.Visible(True)

        if mcp.WorkBook(r"D:\test.xlsx"):
            print(mcp.ActiveWorkbook())
            print(mcp.ActiveSheet())

        print(mcp.WorkBooks())
        print(mcp.Sheets(r"D:\test.xlsx"))

        # for i in range(10):
        #     task = mcp.AiTask()
        #     if task:
        #         print(task)

        mcp.RunPython('''
        print(The.Excel.Name)
        ''')

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print(f"Successed")
        #mcp.Visible(False)
        #mcp.Quit()

