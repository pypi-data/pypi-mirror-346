import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from claudette import Chat, models
from .context_manager import ContextManager
import ast
from dataguy.utils import LLMResponseCache
import builtins


class DataGuy:
    def __init__(self, max_code_history=100):
        self.context = ContextManager(max_code_history=max_code_history)
        self.data = None
        self._data_description = None

        self.chat_code = Chat(self._select_model("code"), sp="You write Python code for pandas and matplotlib tasks.")
        self.chat_text = Chat(self._select_model("text"), sp="You explain datasets and their structure clearly.")
        self.chat_image = Chat(self._select_model("image"), sp="You describe uploaded data visualizations clearly, so plot can be recreated based on that.")

        self.cache=LLMResponseCache()

    def _select_model(self, mode):
        if mode == "image":
            return next((m for m in models if "opus" in m), models[-1])
        elif mode == "text":
            return next((m for m in models if "sonnet" in m or "haiku" in m), models[-1])
        else:
            return models[-1]

    def _generate_code(self, task: str) -> str:
        prompt = self.context.get_context_summary() + "\n# Task: " + task + "The dataset you're using is named data, trying with other names will likely error."
        resp = self.chat_code(prompt)

        # Safely extract LLM response
        try:
            raw = resp.content[0].text
        except (AttributeError, IndexError, TypeError) as e:
            raise ValueError(f"Invalid LLM response format: {resp}") from e

        match = re.search(r'```(?:python)?\n(.*?)```', raw, re.S)
        if match:
            extracted_code = match.group(1).strip()
        else:
            extracted_code = raw.strip()

        if not extracted_code:
            raise ValueError("No code found in LLM response.")

        return extracted_code

    def _is_safe_code(self, code_str):
        SAFE_MODULES = {"numpy", "pandas", "matplotlib", "sklearn","math","random","seaborn",
                        "scipy","pyPCG","imblearn","xgboost","signal"}#would need a lot of expanding
        BLOCKED_MODULES = {"os", "sys", "subprocess", "builtins", "shutil"}

        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        if module_name in BLOCKED_MODULES:
                            print(f"Blocked unsafe import: {module_name}")
                            return False
                        if module_name not in SAFE_MODULES:
                            print(f"Import of unknown module {module_name} blocked.")
                            return False

                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module.split('.')[0] if node.module else ""
                    if module_name in BLOCKED_MODULES:
                        print(f"Blocked unsafe from-import: {module_name}")
                        return False
                    if module_name not in SAFE_MODULES:
                        print(f"From-import of unknown module {module_name} blocked.")
                        return False

                elif isinstance(node, (ast.Global, ast.Nonlocal)):
                    print(f"Blocked unsafe node: {type(node).__name__}")
                    return False
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'exec':
                    print("Blocked unsafe function call: exec()")
                    return False

            return True

        except SyntaxError as e:
            print(f"Syntax error during AST check: {e}")
            return False

    def _exec_code(self, code: str, retries_left=3) -> dict:
        print("Executing code:\n", code)

        safe_globals = {
            "__builtins__": builtins,
            "pd": pd,
            "np": np,
            "plt": plt,
        }
        local_ns = {"data": self.data}
        base = set(local_ns)

        if not self._is_safe_code(code):
            print("Unsafe code detected. Execution aborted.")
            return {"error": "Unsafe code detected and blocked."}

        try:
            exec(code, safe_globals, local_ns)
        except (SyntaxError, Exception) as e:
            print(f"Error during code execution: {e}")

            if retries_left <= 0:
                return {"error": f"Execution failed after retries: {e}"}

            fix_task = (
                "The following code failed with this error:\n"
                f"{e}\n\n"
                "Original code:\n"
                f"{code}\n\n"
                "Please fix the code."
                "Ensure all variables are defined in the code."
                "Include all necessary imports and data loading."
                "Do not assume any variables exist beforehand."
            )

            # Re-generate code using error feedback
            new_code = self._generate_code(fix_task)
            print(f"Retrying with corrected code (retries left: {retries_left-1})...")
            return self._exec_code(new_code, retries_left=retries_left - 1)
        else:
            self.context.add_code(code)
            self.context.update_from_globals(local_ns)
        finally:
            self.context.update_from_globals(local_ns)

        new_keys = set(local_ns) - base
        return {k: local_ns[k] for k in new_keys if not k.startswith('__')} | \
               {'data': local_ns['data']} if 'data' in local_ns else {}

    def set_data(self, obj):
        if isinstance(obj, pd.DataFrame):
            self.data = obj.copy()

        elif isinstance(obj, (dict, list, np.ndarray)):
            self.data = pd.DataFrame(obj)

        elif isinstance(obj, str) and obj.endswith('.csv'):
            self.data = pd.read_csv(obj)

        elif isinstance(obj, bytes):
            from io import BytesIO
            self.data = pd.read_csv(BytesIO(obj))

        elif hasattr(obj, 'to_pandas'):  # fallback for other dataframes
            self.data = obj.to_pandas()

        else:
            raise TypeError(f"Unsupported data type: {type(obj)}")

        self.context.update_from_globals({"data": self.data})
        return self.data

    def summarize_data(self):
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'missing_counts': self.data.isna().sum().to_dict(),
            'means': self.data.mean(numeric_only=True).to_dict()
        }


    def describe_data(self) -> str:
        summary = self.summarize_data()
        prompt = (
            "Describe the dataset in a few sentences based on the following summary:\n"
            f"{summary}"
        )

        cached_resp = self.cache.get(prompt)
        if cached_resp:
            resp_text = cached_resp
        else:
            resp = self.chat_text(prompt)
            resp_text = resp.content[0].text
            self.cache.set(prompt, resp_text)

        self.context.add_code(f"# Description: {resp_text}")
        self._data_description=resp_text
        return resp_text

    def wrangle_data(self) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        summary = self.summarize_data()
        desc = self.describe_data()
        task = (
            "Write a lambda function named `wrangler` that takes a pandas DataFrame and wrangles it for analysis.\n"
            f"Summary: {summary}\n"
            f"Description: {desc}"
        )
        code = self._generate_code(task)
        ns = self._exec_code(code)
        wrangler = ns.get('wrangler')
        if callable(wrangler):
            self.data = wrangler(self.data)
        return self.data

    def analyze_data(self):
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")

        task = "Analyze the pandas DataFrame `data` and return a dict `result` with shape, columns, and descriptive stats."
        code = self._generate_code(task)
        ns = self._exec_code(code)

        result = ns.get('result')
        if result is None:
            print("Warning: LLM-generated code did not return a 'result'.")
            result = {"error": "No result returned by analysis code."}

        return result

    def plot_data(self, column_x: str, column_y: str):
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        task = f"Create a scatter plot of `data` with x='{column_x}' and y='{column_y}'. Use matplotlib."
        code = self._generate_code(task)
        self._exec_code(code)

    def describe_plot(self, img_bytes: bytes) -> str:
        resp = self.chat_image([img_bytes, "Please describe this plot in detail so that it can be faithfully recreated in Python using matplotlib.Include ALL of the following in your description: 1. The type of plot (scatter, line, bar, etc.) 2. The variables plotted on X and Y axes (including units if visible) 3. The number of data points shown 4. The axis ranges (min and max for X and Y) 5. Any grouping or color coding used (legend categories) 6. Any markers, shapes, or line styles used 7. Any annotations or text present 8. The general pattern or trend visible 9. Figure size or aspect ratio if visible 10. Anything else visible that affects interpretation. Be precise and exhaustive. Do not assume anything; describe only what is visible.This description will be used to write Python code to recreate the plot as closely as possible."])
        desc = resp.content[0].text
        self.context.add_code(f"# Plot description: {desc}")
        return desc

    def recreate_plot(self, plot_description: str):
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        # incorporate wrangled summary and dataset description
        summary = self.summarize_data()
        desc = self._data_description or ""
        task = (
            "Write Python code using pandas and matplotlib to create a plot for 'data' similar to the description below. It is a different dataset.\n"
            f"the data is in the variable data_to_plot\n"
            f"Dataset summary: {summary}\n"
            f"Dataset description: {desc}\n"
            f"Plot description: {plot_description}"
        )
        code = self._generate_code(task)
        self._exec_code(code)
