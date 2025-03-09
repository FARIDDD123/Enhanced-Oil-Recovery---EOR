import json
import os
import pandas as pd
import nbformat
from io import StringIO

notebook_path = os.path.join(".." , "Enhanced-Oil-Recovery---EOR" , "daatasets" , "oil1.ipynb")
output_csv_path = os.path.join(os.getcwd(), "notebook_output.csv")

if not os.path.exists(notebook_path):
    print("❌ [ERROR] Notebook file 'oil1.ipynb' not found in the current directory!")
    exit(1)

def extract_dataframe_from_notebook(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"❌ [ERROR] Failed to read the notebook: {e}")
        return None
    
    for cell in notebook_data.cells:
        if cell.cell_type == "code" and "outputs" in cell:
            for output in cell.outputs:
                if "data" in output and "text/html" in output["data"]:
                    html_output = output["data"]["text/html"]
                    try:
                        dfs = pd.read_html(StringIO(html_output))
                        if len(dfs) > 0:
                            return dfs[0]
                    except Exception:
                        pass
                
                if "data" in output and "text/plain" in output["data"]:
                    text_output = output["data"]["text/plain"]
                    try:
                        result = eval(text_output, {"pd": pd, "__builtins__": {}})
                        if isinstance(result, pd.DataFrame):
                            return result
                    except Exception:
                        try:
                            df = pd.read_fwf(StringIO(text_output))
                            if not df.empty:
                                return df
                        except Exception:
                            pass
                
                if output.get("output_type") == "stream" and "text" in output:
                    stream_text = output["text"]
                    try:
                        result = eval(stream_text, {"pd": pd, "__builtins__": {}})
                        if isinstance(result, pd.DataFrame):
                            return result
                    except Exception:
                        try:
                            df = pd.read_fwf(StringIO(stream_text))
                            if not df.empty:
                                return df
                        except Exception:
                            pass
    return None

df = extract_dataframe_from_notebook(notebook_path)

if df is not None:
    print("✅ 🎉 Extracted DataFrame from Notebook!")   
    num_cols = df.shape[1]
    new_row = {}
    for i in range(0, num_cols - 1, 2):
        col_synthetic = df.columns[i]
        col_real = df.columns[i+1]
        match_count = (df[col_synthetic] == df[col_real]).sum()
        total_count = len(df)
        match_percentage = (match_count / total_count) * 100 if total_count > 0 else 0
        new_row[col_synthetic] = ""
        new_row[col_real] = f"{match_percentage:.2f}%"
    if num_cols % 2 != 0:
        new_row[df.columns[-1]] = "N/A"
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(output_csv_path, index=False)
    print(f"📂 💾 Saved extracted DataFrame to `{output_csv_path}`")
    os.startfile(output_csv_path)
else:
    print("⚠️ 🚨 No valid DataFrame found in the notebook!")
