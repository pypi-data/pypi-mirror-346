import argparse
import sys
import json
import os
from typing import Any, Dict, Optional
from issue_solver import IssueSolver
from dotenv import load_dotenv
from pathlib import Path
from config import Config

# ANSI color codes
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def load_config_from_file(config_path: str) -> Config:
    if not config_path or not os.path.exists(config_path):
        raise ValueError(f"Configuration file not found or provided: {config_path}")
    
    try:
        with open(config_path, "r") as f:
            config_data = f.read()
        return Config.from_json(config_data)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading config file {config_path}: {e}")
        raise ValueError(f"Failed to load configuration file: {e}")

def create_default_config(args: argparse.Namespace) -> None:
    """
    Creates a default configuration file at the specified path using Config class.
    
    Args:
        args: Command line arguments containing the output path.
    """
    try:
        # Create a Config object with default values
        config = Config()
        
        # Ensure proper path handling for both relative and absolute paths
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
            
        # Create parent directories if they don't exist and path is not in current directory
        if output_path.parent != Path.cwd():
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the configuration file with pretty printing
        with open(output_path, 'w') as f:
            f.write(config.to_json(indent=2))
            
        print(f"{GREEN}Successfully created configuration file at: {output_path}{RESET}")
    except Exception as e:
        print(f"{RED}Error creating configuration file: {e}{RESET}")
        sys.exit(1)

def setup_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CS Assistant")
    parser.add_argument(
        "-c", "--config", type=str,
        help="Path to the configuration file (config.json). If provided, command-line arguments will be ignored."
    )
    parser.add_argument(
        "-o", "--output-directory",
        type=str,
        default="cs-assistant-output",
        help="Directory where solution files will be saved.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- create-config command ---
    create_config_parser = subparsers.add_parser(
        "create-config", 
        help="Create a new configuration file with default settings."
    )
    create_config_parser.add_argument(
        "-o", "--output", 
        type=str, 
        default="config.json",
        help="Path where the configuration file should be created (default: config.json)"
    )

    # --- solve-issue command ---
    solve_parser = subparsers.add_parser(
        "solve-issue", help="Solve a given coding issue."
    )
    solve_parser.add_argument(
        "issue_description", type=str, help="The description of the coding issue."
    )

    # Arguments mirroring config.schema.json structure
    solve_parser.add_argument(
        "-m", "--llm-model",
        type=str,
        default="google/models/gemini-2.5-pro-exp-03-25",
        help="The identifier for the large language model to be used. Format: 'vendor/model_name' where vendor (e.g., 'google', 'openai') represents the company providing the LLM.",
    )
    solve_parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.7,
        help="Controls the randomness of the model's output (0.0 to 1.0).",
    )

    verbal_group = solve_parser.add_argument_group("Verbal Algorithm Options")
    verbal_group.add_argument(
        "-v", "--verbal-algorithm",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable/disable verbal algorithm explanations.",
    )
    verbal_group.add_argument(
        "-l", "--verbal-algorithm-languages",
        nargs="+",
        default=["en"],
        help="List of languages for verbal explanations.",
    )
    verbal_group.add_argument(
        "-p", "--verbal-algorithm-include-pseudocode",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include/exclude pseudocode in the output.",
    )

    solve_parser.add_argument(
        "-d", "--include-mermaid-diagram",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include/exclude a Mermaid diagram in the output.",
    )

    code_impl_group = solve_parser.add_argument_group("Code Implementation Options")
    code_impl_group.add_argument(
        "-i", "--code-implementations",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable/disable code implementation generation.",
    )
    code_impl_group.add_argument(
        "-L", "--code-implementations-languages",
        nargs="+",
        default=["Python"],
        help="List of programming languages for code implementations.",
    )
    
    # Add other subparsers here if needed in the future
    # e.g., review_parser = subparsers.add_parser("review-code", help="Review a code snippet.")
    
    return parser

def load_config_from_cli_args(args: argparse.Namespace) -> Config:
    """Convert CLI arguments to Config object using Config.from_args."""
    return Config.from_args(args)

def _load_environment_variables():
    """Loads environment variables from user-specific .csarc file.
    Creates the file with placeholders if it doesn't exist."""
    # Try loading user-specific .csarc
    csarc_path = Path.home() / ".config" / "cs_assistant" / ".csarc"
    
    if csarc_path.is_file():
        print(f"Loading environment variables from: {csarc_path}")
        load_dotenv(dotenv_path=csarc_path)
    else:
        print(f"Configuration file not found at {csarc_path}.")
        print("Creating a template configuration file...")
        
        try:
            # Create parent directory if it doesn't exist
            csarc_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Define default content
            default_content = """\\
# Please replace the placeholder values below with your actual API keys.
# Example:
# OPENAI_API_KEY="sk-..."
# GOOGLE_API_KEY="..."
# ANTHROPIC_API_KEY="sk-ant-..."

OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY_HERE"
"""
            
            # Write the default content to the file
            with open(csarc_path, "w") as f:
                f.write(default_content)
                
            print(f"{YELLOW}Successfully created template configuration file at: {csarc_path}")
            print(f"Please edit this file and add your API keys.{RESET}")
            
            # Exit after creating the template, as it needs user intervention.
            print("Exiting. Please populate the configuration file and run the tool again.")
            sys.exit(0) # Exit gracefully after creating the file
            
        except IOError as e:
            print(f"{RED}Error creating configuration file {csarc_path}: {e}{RESET}")
            sys.exit(1) # Exit if we cannot create the config file
        except Exception as e: # Catch other potential errors like permission issues
            print(f"{RED}An unexpected error occurred during configuration file creation: {e}{RESET}")
            sys.exit(1)

def resolve_config(args: argparse.Namespace) -> Config:
    """
    Resolve configuration from either config file or command line arguments.
    Config file takes precedence if provided and valid.
    
    Args:
        args: Command line arguments.
        
    Returns:
        Config object with resolved configuration.
    """
    # Try config file first if provided
    if args.config:
        return load_config_from_file(args.config)
            
    # Fall back to CLI args if no config file is provided
    print("Using command-line arguments for configuration.")
    return load_config_from_cli_args(args)

def handle_create_config(args: argparse.Namespace) -> None:
    """Handles the create-config command."""
    create_default_config(args)

def handle_solve_issue(args: argparse.Namespace, config: Config) -> None:
    """Handles the solve-issue command."""
    solver = IssueSolver(config=config)
    solution_path = solver.solve(args.issue_description)
    # Print success message in green
    print(f"{GREEN}Success!🎉 Solution saved to: {solution_path}{RESET}")

def main():
    # Load environment variables
    _load_environment_variables()

    parser = setup_arg_parser()
    args = parser.parse_args()

    command_handlers = {
        "create-config": lambda: handle_create_config(args),
        "solve-issue": lambda: handle_solve_issue(args, resolve_config(args))
    }

    if args.command in command_handlers:
        command_handlers[args.command]()
    elif args.command is None:
        # No command was provided
        parser.print_help()
    else:
        # Handle other commands if/when they are added
        print(f"Command '{args.command}' does not exist.")
        parser.print_help()

if __name__ == "__main__":
    main() 