import os
import json
import argparse
import re  # Added for sanitization
from enum import Enum
from typing import Dict, Callable, Optional, List, Any, Set
from pathlib import Path
from dataclasses import dataclass # Import dataclass
import api_clients
from config import Config, SolveIssueConfig

# --- API Call Configuration ---
@dataclass
class ApiCallConfig:
    model_name: str
    system_prompt: str
    user_prompt: str
    temperature: float
    requested_fields: List[str]

# --- Constants ---
# Model provider enum
class ModelProvider(Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"

# Field descriptions for system prompt
SYSTEM_PROMPT_FIELD_DESCRIPTIONS = {
    "problem_name": '`"problem_name"`: (String) A concise, filesystem-friendly name for the programming problem (e.g., "fibonacci_sequence", "two_sum_problem", "binary_search"). Use snake_case.',
    "verbal_algorithm": '`"verbal_algorithm"`: (String) Start with a brief overall explanation of the approach. Then, clearly outline the step-by-step logic required to solve the problem in the language specified in the request. Explain what needs to be done conceptually from start to finish. Accompany the step-by-step explanations with one consistent example throughout to illustrate key concepts.',
    "pseudocode": '`"pseudocode"`: (String) Translate the verbal algorithm into clear, language-agnostic pseudocode. This should accurately represent the core logic, control flow, and data structures involved, formatted nicely (e.g., using markdown code blocks or similar within the string).',
    "code_implementations": '`"code_implementations"`: (Object/Dictionary) Contains the code solutions.\n    *   The keys should be the lowercase names of the programming languages requested (e.g., "python", "java").\n    *   The values should be **objects**, each containing two keys:\n        *   `"filename"`: (String) The appropriate filename for the code, **including the correct file extension** (e.g., "fibonacci.py", "TwoSum.java"). The filename should ideally relate to the `problem_name`.\n        *   `"code"`: (String) The complete, working code for that language. Ensure the code is clean, well-commented where necessary for clarity, efficient, and directly solves the stated problem according to the algorithm and pseudocode.',
    "mermaid_diagram": '`"mermaid_diagram"`: (String) A Mermaid diagram string representing the solution visually. For object-oriented problems, provide a UML class diagram. For algorithmic problems, provide a state diagram (deterministic finite automaton) or flowchart illustrating the logic and state transitions. Use standard Mermaid syntax (https://mermaid.js.org/syntax/classDiagram.html, https://mermaid.js.org/syntax/stateDiagram.html). Enclose the diagram definition within a `\\`mermaid\\n...\\n``` block.'
}

# JSON schema field descriptions
JSON_SCHEMA_FIELD_DESCRIPTIONS = {
    "problem_name": {
        "type": "string",
        "description": "A concise, filesystem-friendly name for the programming problem in snake_case"
    },
    "verbal_algorithm": {
        "type": "string", 
        "description": "A step-by-step explanation of the approach to solve the problem in English, with an example"
    },
    "pseudocode": {
        "type": "string",
        "description": "Language-agnostic pseudocode representation of the algorithm"
    },
    "code_implementations": {
        "type": "object",
        "description": "Contains the code solutions, with keys as lowercase programming language names.",
        "patternProperties": {
            "^[a-z]+$": {
                "type": "object", 
                "description": "Code implementation for a specific language.",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The appropriate filename for the code, including the correct file extension. Should ideally relate to the problem_name."
                    },
                    "code": {
                        "type": "string",
                        "description": "The complete, working code for that language. Should be clean, well-commented, efficient, and directly solve the stated problem."
                    }
                },
                "required": [
                    "filename",
                    "code"
                ],
                "additionalProperties": False
            }
        },
        "additionalProperties": False
    },
    "mermaid_diagram": {
        "type": "string",
        "description": "A Mermaid diagram string representing the solution visually, enclosed in a mermaid code block"
    }
}


# Field examples for system prompt
SYSTEM_PROMPT_FIELD_EXAMPLES = {
    "problem_name": '"problem_name": "fibonacci_sequence"',
    "verbal_algorithm": '"verbal_algorithm": "Overall approach: The Fibonacci sequence is defined recursively. Each number is the sum of the two preceding ones, starting from 0 and 1. We can compute the nth Fibonacci number using this recursive definition directly.\\n\\nStep-by-step:\\n1. Define base cases: If n is 0, the result is 0. If n is 1, the result is 1. (Example: For fibonacci(0), return 0. For fibonacci(1), return 1.)\\n2. Recursive step: For n > 1, calculate the Fibonacci number by summing the (n-1)th and (n-2)th Fibonacci numbers. (Example: For fibonacci(3), calculate fibonacci(2) + fibonacci(1)).\\n3. Return the calculated value."',
    "pseudocode": '"pseudocode": "```\\nFUNCTION fibonacci(n)\\n  IF n <= 0 RETURN 0\\n  IF n == 1 RETURN 1\\n  RETURN fibonacci(n-1) + fibonacci(n-2)\\nENDFUNCTION\\n```"',
    "code_implementations": '"code_implementations": {\n    "python": {\n      "filename": "fibonacci.py",\n      "code": "def fibonacci(n):\\n  if n <= 0:\\n    return 0\\n  elif n == 1:\\n    return 1\\n  else:\\n    return fibonacci(n-1) + fibonacci(n-2)"\n    },\n    "java": {\n      "filename": "Fibonacci.java",\n      "code": "public class Fibonacci {\\n    public static int fib(int n) {\\n        if (n <= 0) return 0;\\n        if (n == 1) return 1;\\n        return fib(n-1) + fib(n-2);\\n    }\\n}"\n    }\n  }',
    "mermaid_diagram": '"mermaid_diagram": "```mermaid\\nstateDiagram-v2\\n    [*] --> BaseCaseCheck\\n    BaseCaseCheck --> IsZero : n == 0?\\n    IsZero --> ReturnZero : Yes\\n    BaseCaseCheck --> IsOne : n == 1?\\n    IsOne --> ReturnOne : Yes\\n    BaseCaseCheck --> RecursiveStep : n > 1\\n    RecursiveStep --> ComputeFib1 : fib(n-1)\\n    RecursiveStep --> ComputeFib2 : fib(n-2)\\n    ComputeFib1 --> SumResults\\n    ComputeFib2 --> SumResults\\n    SumResults --> ReturnSum\\n    ReturnZero --> [*]\\n    ReturnOne --> [*]\\n    ReturnSum --> [*]\\n```"'
}

# User prompt field building blocks
USER_PROMPT_FIELDS = {
    "base_instruction": "Solve this programming problem",
    "code_implementations": "Provide code implementations in the following language(s): {languages}",
    "verbal_algorithm": "The verbal algorithm explanation MUST be in the following language(s): {languages}",
    "problem_statement": "Problem: {problem}"
}

# Map provider strings to ModelProvider enum values
PROVIDER_MAP: Dict[str, ModelProvider] = {
    "openai": ModelProvider.OPENAI,
    "google": ModelProvider.GOOGLE,
    "anthropic": ModelProvider.ANTHROPIC
}

class IssueSolver:
    # --- Class Constants ---
    VERBAL_ALGORITHM_FILENAME = "verbal_algorithm.md"

    def __init__(self, config: Config):
        """
        Initialize the IssueSolver with configuration settings.
        
        Args:
            config (Config): The configuration object containing all settings.
        """
        self.config = config
        self.api_callers: Dict[ModelProvider, Callable] = {
            ModelProvider.OPENAI: self._call_openai_api,
            ModelProvider.GOOGLE: self._call_google_api,
            ModelProvider.ANTHROPIC: self._call_anthropic_api
        }
        
    # --- Internal API Call Wrappers ---
    def _call_openai_api(self, api_config: ApiCallConfig) -> Optional[str]:
        return api_clients.call_openai_api(
            model_name=api_config.model_name,
            system_prompt=api_config.system_prompt,
            user_prompt=api_config.user_prompt,
            temperature=api_config.temperature
        )

    def _call_google_api(self, api_config: ApiCallConfig) -> Optional[str]:
        return api_clients.call_google_api(
            model_name=api_config.model_name,
            system_prompt=api_config.system_prompt,
            user_prompt=api_config.user_prompt,
            temperature=api_config.temperature
        )

    def _call_anthropic_api(self, api_config: ApiCallConfig) -> Optional[str]:
        # Create a dynamic JSON schema based on requested fields
        dynamic_schema = {
            "type": "object",
            "required": list(api_config.requested_fields),
            "properties": {
                field: JSON_SCHEMA_FIELD_DESCRIPTIONS[field]
                for field in api_config.requested_fields
            }
        }
        return api_clients.call_anthropic_api(
            model_name=api_config.model_name,
            system_prompt=api_config.system_prompt,
            user_prompt=api_config.user_prompt,
            temperature=api_config.temperature,
            dynamic_schema=dynamic_schema
        )

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Removes or replaces characters unsafe for filenames/directory names."""
        # Remove leading/trailing whitespace
        name = name.strip()
        # Replace spaces and unsafe characters with underscores
        name = re.sub(r'[\s\\/:*?\"<>|]+', '_', name)
        # Limit length (optional, adjust as needed)
        max_len = 100
        if len(name) > max_len:
            name = name[:max_len]
            # Ensure it doesn't end with an underscore if truncated
            while name.endswith('_') and len(name) > 0:
                name = name[:-1]
        if not name: # Handle case where name becomes empty
            return "unnamed_solution"
        return name

    @staticmethod
    def _get_model_provider(model_name: str) -> ModelProvider:
        """
        Determines the appropriate provider based on the given model name.
        
        Args:
            model_name (str): The name of the model or provider to use.
            
        Returns:
            ModelProvider: The determined provider for the model.
            
        Raises:
            ValueError: If the model provider cannot be determined from the model name.
        """
        # For models that start with provider prefixes
        # Handle potential full model paths like "google/gemini-pro"
        provider_part = model_name.split('/')[0].lower()

        # Try to get provider from mapping
        if provider_part in PROVIDER_MAP:
            return PROVIDER_MAP[provider_part]

        # Raise an exception for unknown models
        raise ValueError(f"Unknown model provider: {model_name}. Cannot determine the appropriate API provider.")

    @staticmethod
    def _build_requested_fields(config: SolveIssueConfig) -> List[str]:
        # Build requested fields list - problem_name is always included
        requested_fields = ["problem_name"]
        
        # Add optional fields based on boolean flags in config
        if config.verbal_algorithm is not None:
            requested_fields.append("verbal_algorithm")
        
        if config.verbal_algorithm is not None and config.verbal_algorithm.include_pseudocode:
            requested_fields.append("pseudocode")
        
        # Add code_implementations field if enabled
        if config.code_implementations is not None:
            requested_fields.append("code_implementations")
        
        # Add mermaid_diagram field if enabled
        if config.include_mermaid_diagram:
            requested_fields.append("mermaid_diagram")

        return requested_fields

    @staticmethod
    def _build_system_prompt(fields: List[str]) -> str:
        """
        Dynamically builds a system prompt containing only the specified fields.
        
        Args:
            fields: List of field names to include in the prompt
        
        Returns:
            A string containing the complete system prompt with only the requested fields
        """
        # Validate the requested fields
        valid_fields = set(SYSTEM_PROMPT_FIELD_DESCRIPTIONS.keys())
        requested_fields = [field for field in fields if field in valid_fields]
        
        if not requested_fields:
            raise ValueError(f"No valid fields provided. Valid fields are: {', '.join(valid_fields)}")
        
        # Introductory text
        intro = """
You are an expert Computer Science programming assistant designed to solve problems systematically. Your primary task is to take a given programming problem and provide a comprehensive solution.

You MUST respond ONLY with a valid JSON object containing the following keys:
"""
        
        # Build the field descriptions section
        field_text = ""
        for i, field in enumerate(requested_fields, 1):
            field_text += f"{i}.  {SYSTEM_PROMPT_FIELD_DESCRIPTIONS[field]}\n"
        
        # Build the example JSON
        example_json = "{\n"
        for field in requested_fields:
            example_json += f"  {SYSTEM_PROMPT_FIELD_EXAMPLES[field]}"
            if field != requested_fields[-1]:  # Add comma if not the last field
                example_json += ","
            example_json += "\n"
        example_json += "}"
        
        # Example section
        example_section = f"""
Example JSON Structure:
```json
{example_json}
```
"""
        
        # Conclusion
        conclusion = """
Focus exclusively on delivering a single, valid JSON object adhering to this structure for every programming problem presented.
"""
        
        # Assemble the complete prompt
        return intro + field_text + example_section + conclusion

    @staticmethod
    def _build_user_prompt(
        issue_description: str,
        fields: List[str],
        verbal_algorithm_languages: Optional[List[str]],
        programming_languages: Optional[List[str]]
    ) -> str:
        """
        Dynamically builds a user prompt based on the requested fields.
        
        Args:
            issue_description: The problem description to solve
            fields: List of field names to include in the prompt
            verbal_algorithm_languages: List of languages for verbal algorithm explanation
            programming_languages: List of programming languages for code implementations
            
        Returns:
            A string containing the complete user prompt with only the requested fields
        """
        prompt_parts = [USER_PROMPT_FIELDS["base_instruction"]]
        
        # Add field-specific instructions based on requested fields
        if "code_implementations" in fields and programming_languages:
            code_language_string = ", ".join(lang.lower() for lang in programming_languages)
            prompt_parts.append(
                USER_PROMPT_FIELDS["code_implementations"].format(languages=code_language_string)
            )
        
        if "verbal_algorithm" in fields and verbal_algorithm_languages:
            verbal_language_string = ", ".join(lang.lower() for lang in verbal_algorithm_languages)
            prompt_parts.append(
                USER_PROMPT_FIELDS["verbal_algorithm"].format(languages=verbal_language_string)
            )
        
        # Join all parts and add the problem statement
        prompt = " ".join(prompt_parts) + ".\n\n"
        prompt += USER_PROMPT_FIELDS["problem_statement"].format(problem=issue_description)
        
        return prompt

    @staticmethod
    def _process_verbal_algorithm(solution_data: Dict, solution_path: Path) -> None:
        """
        Process the verbal algorithm field independently.
        
        Args:
            solution_data: The parsed solution data
            solution_path: Path to the solution directory
        """
        # Return immediately if verbal algorithm not present
        if "verbal_algorithm" not in solution_data:
            return
        
        verbal_algorithm = solution_data["verbal_algorithm"]
        
        # Use the class constant for the filename
        md_path = solution_path / IssueSolver.VERBAL_ALGORITHM_FILENAME
        
        # Write to file
        with open(md_path, 'a+') as f:
            # Seek to beginning to check if file has content
            f.seek(0)
            content = f.read()
            
            # If file is empty or doesn't exist, start with a clean slate
            if not content:
                f.seek(0)
                f.truncate()
            
            # Write verbal algorithm section
            f.write("# Verbal Algorithm\n\n")
            f.write(verbal_algorithm + "\n\n")
        
        print(f"Added verbal algorithm to {md_path.name}")

    @staticmethod
    def _process_pseudocode(solution_data: Dict, solution_path: Path) -> None:
        """
        Process the pseudocode field independently.
        
        Args:
            solution_data: The parsed solution data
            solution_path: Path to the solution directory
        """
        # Return immediately if pseudocode not present
        if "pseudocode" not in solution_data:
            return
        
        pseudocode = solution_data["pseudocode"]
        
        # Format pseudocode properly if needed
        if not pseudocode.strip().startswith("```"):
            pseudocode = f"```\\n{pseudocode}\\n```"
        
        # Use the class constant for the filename
        md_path = solution_path / IssueSolver.VERBAL_ALGORITHM_FILENAME
        
        # Write to file
        with open(md_path, 'a+') as f:
            # Seek to beginning to check if file has content
            f.seek(0)
            content = f.read()
            
            # If file is empty or doesn't exist, start with a clean slate
            if not content:
                f.seek(0)
                f.truncate()
            
            # Write pseudocode section
            f.write("# Pseudocode\n\n")
            f.write(pseudocode + "\n\n")
        
        print(f"Added pseudocode to {md_path.name}")

    @staticmethod
    def _process_code_implementations(solution_data: Dict, solution_path: Path) -> None:
        """
        Process the code implementations field independently.
        
        Args:
            solution_data: The parsed solution data
            solution_path: Path to the solution directory
        """
        # Return immediately if code implementations not present
        if "code_implementations" not in solution_data:
            return
        
        code_implementations = solution_data["code_implementations"]
        
        # Validate code_implementations is a dictionary
        if not isinstance(code_implementations, dict):
            print(f"Warning: 'code_implementations' is not a dictionary. Received: {type(code_implementations)}")
            return
        
        if not code_implementations:
            print("Warning: No code implementations found in the response.")
            return
        
        # Process each language implementation
        for lang_key, implementation_data in code_implementations.items():
            if not isinstance(implementation_data, dict) or 'filename' not in implementation_data or 'code' not in implementation_data:
                print(f"Warning: Skipping invalid implementation data for language '{lang_key}'. Expected dict with 'filename' and 'code'. Got: {implementation_data}")
                continue
            
            filename_raw = implementation_data.get('filename')
            code = implementation_data.get('code')
            
            if not filename_raw or not isinstance(filename_raw, str):
                print(f"Warning: Skipping implementation for '{lang_key}' due to invalid or missing filename.")
                continue
            if not isinstance(code, str):
                print(f"Warning: Skipping implementation for '{lang_key}' due to invalid code type (expected string).")
                continue
            
            # Sanitize the filename provided by the LLM
            filename = IssueSolver._sanitize_filename(filename_raw)
            if not filename: # Check if filename became empty
                print(f"Warning: Skipping implementation for '{lang_key}' because filename '{filename_raw}' became empty after sanitization.")
                continue
            if filename != filename_raw:
                print(f"Warning: Sanitized filename for '{lang_key}' from '{filename_raw}' to '{filename}'")
            
            file_path = solution_path / filename
            try:
                with open(file_path, 'w') as f:
                    f.write(code)
                print(f"Written: {file_path.name}")
            except IOError as e:
                print(f"Error writing file {file_path.name} for language '{lang_key}': {e}")

    @staticmethod
    def _process_mermaid_diagram(solution_data: Dict, solution_path: Path) -> None:
        """
        Process the mermaid diagram field independently.
        
        Args:
            solution_data: The parsed solution data
            solution_path: Path to the solution directory
        """
        # Return immediately if mermaid diagram not present
        if "mermaid_diagram" not in solution_data:
            return
        
        mermaid_diagram = solution_data["mermaid_diagram"]
        
        # Validate mermaid_diagram is a string
        if not isinstance(mermaid_diagram, str):
            print(f"Warning: 'mermaid_diagram' is not a string. Received: {type(mermaid_diagram)}")
            return
            
        if not mermaid_diagram.strip():
            print("Warning: Mermaid diagram content is empty.")
            return

        # Use the directory name (problem name) for the diagram file
        diagram_filename = f"{solution_path.name}-diagram.md"
        diagram_path = solution_path / diagram_filename
        
        try:
            with open(diagram_path, 'w') as f:
                f.write(mermaid_diagram)
            print(f"Written: {diagram_path.name}")
        except IOError as e:
            print(f"Error writing Mermaid diagram file {diagram_path.name}: {e}")

    @staticmethod
    def _clean_json_response(json_response_str: str) -> str:
        """
        Cleans the JSON response string by removing markdown code block markers.
        
        Args:
            json_response_str: The raw response string from the API
            
        Returns:
            The cleaned JSON string
        """
        if json_response_str.strip().startswith("```json"):
            return json_response_str.strip()[7:-3].strip()
        elif json_response_str.strip().startswith("```"):
            return json_response_str.strip()[3:-3].strip()
        return json_response_str

    def solve(self, issue_description: str) -> Optional[str]:
        """
        Generates a solution, parses the JSON response, determines the problem name,
        and saves the solution components into a directory named after the problem.

        Args:
            issue_description (str): The computer science issue/question to solve.

        Returns:
            Optional[str]: The path to the created solution directory if successful, None otherwise.
        """
        print(f"\nGenerating solution for: {issue_description}")
        
        solve_issue_config = self.config.solve_issue
        llm_model = solve_issue_config.llm_model
        temperature = solve_issue_config.temperature

        # Build the system prompt with the requested fields
        requested_fields = self._build_requested_fields(solve_issue_config)
        system_prompt = self._build_system_prompt(requested_fields)

        # Build the user prompt dynamically
        user_prompt = self._build_user_prompt(
            issue_description,
            requested_fields,
            solve_issue_config.verbal_algorithm.languages if solve_issue_config.verbal_algorithm is not None else [],
            solve_issue_config.code_implementations.languages if solve_issue_config.code_implementations is not None else []
        )

        provider = self._get_model_provider(llm_model)

        api_caller = self.api_callers[provider]
        api_model_name = llm_model.split('/')[-1]
        print(f"Using API model: {api_model_name} via {provider.value}")

        # Create ApiCallConfig instance
        api_config_instance = ApiCallConfig(
            model_name=api_model_name, 
            system_prompt=system_prompt, 
            user_prompt=user_prompt, 
            temperature=temperature,
            requested_fields=requested_fields
        )

        json_response_str = api_caller(api_config_instance) # Remove the self argument

        if not json_response_str:
            raise RuntimeError("Failed to get response from API.")

        # --- JSON Parsing and File Writing ---
        try:
            # Clean the response string
            json_response_str = self._clean_json_response(json_response_str)
            solution_data = json.loads(json_response_str)

            if "error" in solution_data:
                raise RuntimeError(f"API returned an error: {solution_data['error']}")

            # Validate ALL required keys including problem_name
            required_keys = requested_fields
            missing_keys = [k for k in required_keys if k not in solution_data]
            if missing_keys:
                raise ValueError(f"Received JSON does not contain all required keys: {missing_keys}. Received data structure: {list(solution_data.keys())}")

            # Get and sanitize the problem name for the directory
            problem_name_raw = solution_data.get("problem_name", "unnamed_problem")
            output_dir_name = self._sanitize_filename(problem_name_raw)
            if not output_dir_name:
                print("Error: Problem name became empty after sanitization.")
                output_dir_name = "sanitized_problem_name_error"

            # Create output directory using the sanitized problem name inside the configured output directory
            solution_path = Path(self.config.output_directory) / output_dir_name
            solution_path.mkdir(parents=True, exist_ok=True)
            print(f"Created solution directory: {solution_path.resolve()}")

            # Process each field with its own method
            self._process_verbal_algorithm(solution_data, solution_path)
            self._process_pseudocode(solution_data, solution_path)
            self._process_code_implementations(solution_data, solution_path)
            self._process_mermaid_diagram(solution_data, solution_path)

            return str(solution_path.resolve())

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON response from API: {e}\nReceived response string:\n{json_response_str}")
        except IOError as e:
            raise IOError(f"Error writing solution files: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred during response processing: {e}")