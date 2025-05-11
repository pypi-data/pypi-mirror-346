
import os
import sys
import re
import time
import datetime
import math
import random
import uuid
import json

VERBOSE_LOG = True  # Set to True to enable verbose logging
EVAL_FUNCTIONS = {
    "BitOR": lambda x, y: x | y,
    "Space": " ",
    "Tab": "\t",
    "NewLine": "\n",

    "timeStamp": lambda: time.time(),
    "currentTime": lambda: datetime.datetime.now().strftime("%H:%M:%S"),
    "currentDate": lambda: datetime.datetime.now().strftime("%m/%d/%Y"),
    "currentDateTime": lambda: datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
    "UUID": lambda: str(uuid.uuid4()),
    "randomNumber": lambda x = 0, y = 100000000: random.randint(x, y),

    "time": time,
    "datetime": datetime,
    "math": math,
    "random": random,
    "uuid": uuid,
    "json": json,
    "re": re,
    "os": os,
}
SAFE_MODE = False
ALLOW_NONE_EVAL_RESULT = False

# Parameter format:
# <NecessaryExpression |-> AssignToVariable | DefaultValue>
# [OptionalExpression |-> AssignToVariable | DefaultValue]
# <$NecesaryVariable | DefaultValue>
# [$OptionalVariable | DefaultValue]

class Argument:
    def __init__(self, value: str, isVariable: bool = False, optional: bool = False, defaultValue: str | None = None, callback = None):
        self.value: str = value
        self.variableName = value if isVariable else None
        self.isVariable: bool = isVariable
        self.optional: bool = optional
        self.defaultValue: str | None = defaultValue
        self.callbackFunction = callback

        print(f"- Argument initialized with value: {value}, isVariable: {isVariable}, optional: {optional}") if VERBOSE_LOG else None
        if not isVariable:
            print(f"- Warning: eval() will be used to calculate this argument. Please ensure that the expression is safe.")
            print(f"- Expression: {value}")
            if SAFE_MODE:
                input("- If you trust the author of this template, press Enter to continue.")

    @staticmethod
    def from_string(arg_str: str, callback = lambda: None) -> 'Argument':
        print("\nArgument string:", arg_str) if VERBOSE_LOG else None
        # Analyze a string like "<xxx>" "[$xxx]" "<time.time()|default_value_when_error_happens>" "<$xxx|defaultValue>"
        arg_str = arg_str.strip()

        # Verify if the string starts and ends with <> or [].
        if arg_str.startswith('<') and arg_str.endswith('>'):
            is_optional = False
        elif arg_str.startswith('[') and arg_str.endswith(']'):
            is_optional = True
        else:
            raise ValueError(f"Invalid argument format: {arg_str}")
        
        # Remove the brackets
        arg_str = arg_str[1:-1].strip()

        # Check if it's a variable or an expression
        if arg_str.startswith('$'):
            is_variable = True
            arg_str = arg_str[1:].strip()
        else:
            is_variable = False
        
        # Check for default value and store actions
        # The original | should follow after one \.
        # Store action can be defined with expression |-> new_variable_name
        # for future using.
        # The combined syntax is like: UUID() |-> result | 0000
        default_value = None
        value = arg_str
        char_count = len(arg_str)
        for i in range(char_count-1, 0, -1):
            if arg_str[i] == '|':
                # Check if the | is escaped
                if i > 0 and arg_str[i - 1] == '\\':
                    continue
                
                # Check if is "store grammar"
                if i <= char_count - 3 and arg_str[i:i+3] == "|->":
                    continue

                # Split the string into value and default value
                value = arg_str[:i].strip()
                default_value = arg_str[i + 1:].strip().replace("\\|", "|")
                break
        
        value2 = value
        char_count = len(value)
        callback_function = None
        for i in range(char_count-3, 0, -1):
            if i <= char_count - 3 and value[i:i+3] == "|->":
                value2 = value[:i].strip()
                callback_variable = value[i + 3:].strip()
                callback_function = lambda x: callback(callback_variable, x)
                break
        
        # Return an Argument object
        return Argument(value2.replace("\\|", "|"), isVariable=is_variable, optional=is_optional, defaultValue=default_value, callback=callback_function)

    def evaluate(self, getVariableFunc = lambda x: "", variableValue = None) -> str:
        # Evaluate the argument value
        if self.isVariable:
            if variableValue is not None:
                return variableValue
            elif self.defaultValue is not None:
                return self.defaultValue
            elif self.optional:
                return ""
            else:
                raise ValueError(f"Variable value not provided for {self.value}")
            
        else:
            try:
                # Evaluate the expression using eval
                # Provide several functions to the eval function
                result = eval(self.value, {"__builtins__": __builtins__}, {**EVAL_FUNCTIONS, "get": getVariableFunc})
                if result is None and not ALLOW_NONE_EVAL_RESULT:
                    raise ValueError("value is None")
                if self.callbackFunction:
                    self.callbackFunction(result)
                return str(result)
            
            except (Exception, KeyboardInterrupt) as e:
                if self.defaultValue is not None:
                    if self.callbackFunction:
                        self.callbackFunction(self.defaultValue)
                    return self.defaultValue
                elif self.optional:
                    if self.callbackFunction:
                        self.callbackFunction("")
                    return ""
                else:
                    raise ValueError(f"Error evaluating expression '{self.value}': {e}")
                
    def __repr__(self):
        return f"Argument(value={self.value}, isVariable={self.isVariable}, optional={self.optional}, defaultValue={self.defaultValue})"

# Define the template class
class Template:
    
    '''
# **Templating Syntax Documentation**
## **Introduction**
The templating system is designed to **generate standardized output text** from a template. The template files are **plain text** with built-in placeholders and scripting syntax that allow **dynamic replacements and computations**. Below are the syntax rules and usage instructions.

---

## **1. Placeholder Markers**
Template files use **two main types of placeholders** to specify areas for substitution:

- **Required parameters**: Enclosed in angle brackets `<...>`
- **Optional parameters**: Enclosed in square brackets `[...]`

These markers differentiate between **mandatory** values and **optional** ones that can be left empty.

---

## **2. Parameter Content**
Placeholders can contain **expressions** or **variables**, and they can also specify **default values** and **storage operations**.

### **2.1 Expression Parameters**
- Written as `<expression>`, the template engine evaluates the expression using `eval()`.
- Example: `<time.strftime("%m/%d/%Y")>` → Outputs the current date.

### **2.2 Variable Parameters**
- Written as `<$variable_name>`, referring to a **stored variable** without `eval()`.
- Example: `<$stored_uuid>` → Outputs the stored UUID.

---

## **3. Default Values and Storage Operations**
Placeholders support **default values**, **result storage**, and **additional processing**.

### **3.1 Default Values**
- **Syntax**: Separate the expression and default value with a vertical bar `|`.
- Format: `<expression | default_value>` or `[$variable_name | default_value]`
- Example: `<$author | DefaultAuthor>` → Uses "DefaultAuthor" if `$author` is undefined.

### **3.2 Result Storage (Variable Caching)**
- **Syntax**: `|-> variable_name` stores the computed result for later reference.
- Example: `<UUID() |-> stored_uuid>` → Generates a UUID and saves it as `$stored_uuid`.

### **3.3 Escape Characters**
- If a vertical bar `|` is needed in an expression, **escape** it with a backslash: `\\|`.

### **3.4 Example of Combined Syntax**
- `<UUID() |-> stored_uuid | 0000>` → Generates a UUID, stores it as `$stored_uuid`, and uses "0000" as the default value if the UUID generation fails.

---

## **4. Built-in Functions and Execution Environment**
The template system **supports several modules and functions**, including:

- **Time-related**: `time`, `datetime` (`timeStamp()`, `currentTime()`, `currentDate()`, `currentDateTime()`)
- **Math operations**: `math`
- **Random generation**: `random`, `randomNumber()`
- **UUID generation**: `uuid`, `UUID()`
- **JSON handling**: `json`
- **Regex operations**: `re`
- **File and OS utilities**: `os`

Additionally, built-in variables **`get()` and `store()`** allow direct access to stored values.

---

## **5. Embedded Script Mechanism**
Template files **can contain pre-processing script sections** to execute logic before parsing the template.

### **Script Syntax**
```
|>ScriptBeforeTemplate
(Python code here, such as variable assignments and store() calls)
|>EndScript
```

This script **runs before template parsing**, allowing global variables and precomputed values.

---

## **6. Template Example**
Below is a **sample template for archive password documentation**, showcasing key syntax features:
```plaintext
|>ScriptBeforeTemplate
# Set author
AUTHOR = "DefaultAuthor"

# Generate a new UUID and store variables
store("author", AUTHOR)
store("stored_uuid", UUID())

|>EndScript
Archive Password <get("stored_uuid")[0:8]>
UUID: <$stored_uuid>
Template version 1.0.0 - Type A - 20250419

The password(s) included in this text file are for:
[$appliedFiles]

Possible passwords for all files:
[$allPasswords]

Passwords for specific files:
[$particularPasswords]

Do not share the archives or passwords without permission from [$author | DefaultAuthor].

Source of the archive: <$ArchiveFrom | SomeWebsite...>
File generated on <time.strftime("%m/%d/%Y")>.
Written by [$author | DefaultAuthor]
```

---

## **7. Important Notes**
- Using `eval()` and `exec()` for dynamic computations **poses security risks**, so ensure template sources are safe.  
- The template engine **scans text character by character**, meaning syntax must strictly follow defined rules.  
- This system is designed for **batch processing** and **standardized text generation**, suitable for archives, configuration files, and structured documents.  

AI Generated Documentation
'''

    def __init__(self, template_str: str):
        self.template = template_str
        self.applyingTemplate: list[str | Argument] = []
        self.variables = {}
        self.scriptBeforeFilling: str | None = None

    @staticmethod
    def load_template(template_file) -> 'Template':
        try:
            with open(template_file, 'r') as file:
                template = file.read()
            return Template(template)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Template file '{template_file}' not found.")

        except Exception as e:
            raise Exception(f"Error loading template file '{template_file}': {e}")

    def analyze_template(self):
        # Analyze the template to find variables and parameters

        # Find if "|>ScriptBeforeTemplate" exists
        script_pattern = r"\|\>ScriptBeforeTemplate[\s\S]*\n\|\>EndScript\n"
        match = re.match(script_pattern, self.template)
        if match:
            self.template = re.sub(script_pattern, "", self.template, 1)
            # if len(match) > 1:
            #     print("Warning: Multiple scripts detected before template. Will only execute the first one.")
            script = match.group(0).removeprefix("|>ScriptBeforeTemplate\n").removesuffix("\n|>EndScript\n")
            print("Detected a script utilized in this template:")
            print(script)
            if SAFE_MODE:
                result = input("\nDo you trust this script? Enter Y to execute before filling, or press enter to ignore it.")
                if result.capitalize().strip() == "Y":
                    self.scriptBeforeFilling = script
            else:
                self.scriptBeforeFilling = script

        optimized_template = []  # Store the optimized template, as [str, Argument, str, Argument, ...].
        last_block = ""
        in_angle_brackets = False
        in_square_brackets = False
        block_start = 0
        current_char = 0

        line_count = len(self.template)

        for char in self.template:
            # print(char, end="")
            if char == "<" and not in_square_brackets and not in_angle_brackets:
                in_angle_brackets = True
                last_block = last_block + self.template[block_start:current_char]
                block_start = current_char

            elif char == "[" and not in_angle_brackets and not in_square_brackets:
                in_square_brackets = True
                last_block = last_block + self.template[block_start:current_char]
                block_start = current_char

            elif char == ">":
                if in_angle_brackets:
                    if current_char > 2 and self.template[current_char-2:current_char+1] == "|->":
                        current_char += 1
                        continue

                    in_angle_brackets = False
                    optimized_template.append(last_block)
                    optimized_template.append(Argument.from_string(self.template[block_start:current_char+1], self.update_variable))
                    last_block = ""
                    block_start = current_char + 1

                elif not in_square_brackets:
                    print(f"Warning: Unmatched '>' at position {current_char} in template.")

            elif char == "]":
                if in_square_brackets:
                    in_square_brackets = False
                    optimized_template.append(last_block)
                    optimized_template.append(Argument.from_string(self.template[block_start:current_char+1], self.update_variable))
                    last_block = ""
                    block_start = current_char + 1

                elif not in_angle_brackets:
                    print(f"Warning: Unmatched ']' at position {current_char} in template.")

            elif char == "\n":
                if in_angle_brackets or in_square_brackets:
                    print(f"Warning: Unmatched newline at position {current_char} in template.")
                    last_block = last_block + self.template[block_start:current_char] + "\n"
                    self.applyingTemplate.append(last_block)
                    in_angle_brackets = False
                    in_square_brackets = False
                    block_start = current_char + 1

                else:
                    last_block = last_block + self.template[block_start:current_char] + "\n"
                    block_start = current_char + 1

            current_char += 1
        
        optimized_template.append(last_block + self.template[block_start:])
        self.applyingTemplate = optimized_template

    def fill_template(self, variable_values: dict = {}) -> str:
        if variable_values is None:
            variable_values = {}

        if self.scriptBeforeFilling:
            print("Executing script before filling.")
            exec(self.scriptBeforeFilling, {"__builtins__": __builtins__}, EVAL_FUNCTIONS | {"store": self.update_variable, "get": self.get_variable})

        self.variables |= variable_values
        self.output = ""

        for block in self.applyingTemplate:
            if isinstance(block, str):
                self.output += block
            elif isinstance(block, Argument):
                # Evaluate the argument and add it to the output
                evaluated_value = block.evaluate(self.get_variable, self.variables.get(block.variableName))
                self.output += evaluated_value
        
        return self.output
    
    def update_variable(self, variable: str, value: str) -> str:
        self.variables[variable] = value
        print("- Updated", variable, "to", value)
        return value

    def get_variable(self, variable: str) -> str:
        return self.variables[variable]

if __name__ == "__main__":
    ...
