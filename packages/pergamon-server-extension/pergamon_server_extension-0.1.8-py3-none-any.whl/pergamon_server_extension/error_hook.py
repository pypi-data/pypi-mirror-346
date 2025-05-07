import traceback
from IPython.display import display, HTML
import os
import re

AI_MODEL = os.environ.get("CALLIOPE_ERROR_MODEL", "gpto")

def custom_exc(shell, etype, evalue, tb, tb_offset=None):
    display(HTML(f"""
    <div>
        <h3>An error has ocurred in this cell</h3>
        <p>Calliope has detected the error and will attempt to fix it.</p>
        <p>The error was: {evalue}</p>
    </div>
    """))

    current_cell = shell.user_ns.get('_ih', [""])[len(shell.user_ns.get('_ih', [""])) - 1]
    
    error_line = None
    try:
        for frame in traceback.extract_tb(tb):
            if frame.filename.startswith('<ipython-input-'):
                error_line = frame.lineno
                break
    except:
        pass
    
    error_message = str(evalue)
    error_type = etype.__name__
    
    ai_prompt = f"""\
    Please fix the following Python code that resulted in a {error_type} error: {error_message}
    
    ---CODE WITH ERROR---
    {current_cell}
    ---END CODE---
    
    Provide ONLY the fixed code without any explanations or markdown formatting. The error occurred on line {error_line if error_line is not None else 'unknown'}.
    """
    
    ai_magic = f"%%ai {AI_MODEL} \n{ai_prompt}"
    res = shell.run_cell(ai_magic)
    fixed_code = None
    
    if hasattr(res.result, '_repr_markdown_'):
        markdown_content = res.result._repr_markdown_()
        code_blocks = re.findall(r'```(?:python)?\n(.*?)```', markdown_content[0], re.DOTALL)
        if code_blocks:
            fixed_code = code_blocks[0].strip()
        else:
            fixed_code = markdown_content.strip()
    
    if fixed_code:
        display(HTML(f"""
        <div>
            <h3>Fixed Code:</h3>
            <pre>{fixed_code.replace('<', '&lt;').replace('>', '&gt;')}</pre>
        </div>
        """))
    else:
        display(HTML(f"""
        <div>
            <h3>Error: {error_type}</h3>
            <p>{error_message}</p>
            <p>Unable to generate fixed code automatically.</p>
            <p>Here is the traceback:</p>
        </div>
        """))
        shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)
    
    return None

def load_ipython_extension(ipython):
    ipython.set_custom_exc((Exception,), custom_exc)

def unload_ipython_extension(ipython):
    ipython.set_custom_exc((), None)