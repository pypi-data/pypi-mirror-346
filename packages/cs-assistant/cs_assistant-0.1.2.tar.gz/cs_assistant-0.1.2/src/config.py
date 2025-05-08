from dataclasses import dataclass, asdict, field
from typing import List, Any, Dict, Optional, Union
import json

@dataclass(frozen=True)
class VerbalAlgorithmConfig:
    """Configuration for the verbal algorithm feature."""
    languages: List[str] = field(default_factory=lambda: ["en"])
    include_pseudocode: bool = True

@dataclass(frozen=True)
class CodeImplementationsConfig:
    """Configuration for code implementations feature."""
    languages: List[str] = field(default_factory=lambda: ["Python"])

@dataclass(frozen=True)
class SolveIssueConfig:
    """Configuration specific to the 'solve_issue' functionality."""
    llm_model: str = "google/models/gemini-2.5-pro-exp-03-25"
    temperature: float = 0.7
    verbal_algorithm: Optional[VerbalAlgorithmConfig] = field(default_factory=VerbalAlgorithmConfig)
    include_mermaid_diagram: bool = True
    code_implementations: Optional[CodeImplementationsConfig] = field(default_factory=CodeImplementationsConfig)

@dataclass(frozen=True)
class Config:
    """
    Represents the overall application configuration.
    It is strongly-typed and immutable after initialization.
    """
    solve_issue: SolveIssueConfig = field(default_factory=SolveIssueConfig)
    output_directory: str = "cs-assistant-output"

    @classmethod
    def create_default(cls) -> 'Config':
        """
        Creates a Config object with default values.

        Returns:
            An immutable Config object with recommended default settings.
        """
        verbal_algo_config = VerbalAlgorithmConfig(
            languages=["en"]
        )

        code_impl_config = CodeImplementationsConfig(
            languages=["Python"]
        )

        solve_issue_config = SolveIssueConfig(
            llm_model="google/models/gemini-2.5-pro-exp-03-25",
            temperature=0.7,
            verbal_algorithm=verbal_algo_config,
            include_mermaid_diagram=True,
            code_implementations=code_impl_config
        )

        return cls(
            solve_issue=solve_issue_config,
            output_directory="cs-assistant-output"
        )

    @classmethod
    def from_json(cls, json_data: Union[str, Dict[str, Any]]) -> 'Config':
        """
        Creates a Config object from JSON data.

        Args:
            json_data: Either a JSON string or a dictionary representing the configuration.
                      Expected structure:
                      {
                          "solve_issue": {
                              "llm_model": str,
                              "temperature": float,
                              "verbal_algorithm": {
                                  "languages": List[str]
                              } | null,
                              "include_mermaid_diagram": bool,
                              "code_implementations": {
                                  "languages": List[str]
                              } | null
                          },
                          "output_directory": str
                      }

        Returns:
            An immutable Config object.

        Raises:
            json.JSONDecodeError: If json_data is a string and is not valid JSON.
            ValueError: If the JSON structure doesn't match the expected configuration format.
        """
        # Convert string to dict if necessary
        if isinstance(json_data, str):
            try:
                config_dict = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(
                    f"Invalid JSON string provided: {str(e)}", e.doc, e.pos
                )
        else:
            config_dict = json_data

        # Validate required top-level keys
        if not isinstance(config_dict, dict):
            raise ValueError("JSON data must be an object")
        
        if "solve_issue" not in config_dict:
            raise ValueError("Missing required 'solve_issue' configuration")
        
        if "output_directory" not in config_dict:
            raise ValueError("Missing required 'output_directory' configuration")

        solve_issue_data = config_dict["solve_issue"]

        # Create verbal algorithm config if present
        verbal_algo_config = None
        if (verbal_algo_data := solve_issue_data.get("verbal_algorithm")) is not None:
            if not isinstance(verbal_algo_data, dict):
                raise ValueError("verbal_algorithm must be an object or null")
            if "languages" not in verbal_algo_data:
                raise ValueError("verbal_algorithm must contain 'languages' list")
            if not isinstance(verbal_algo_data["languages"], list):
                raise ValueError("verbal_algorithm.languages must be a list")
            verbal_algo_config = VerbalAlgorithmConfig(
                languages=list(verbal_algo_data["languages"]),
                include_pseudocode=bool(verbal_algo_data.get("include_pseudocode", True))
            )

        # Create code implementations config if present
        code_impl_config = None
        if (code_impl_data := solve_issue_data.get("code_implementations")) is not None:
            if not isinstance(code_impl_data, dict):
                raise ValueError("code_implementations must be an object or null")
            if "languages" not in code_impl_data:
                raise ValueError("code_implementations must contain 'languages' list")
            if not isinstance(code_impl_data["languages"], list):
                raise ValueError("code_implementations.languages must be a list")
            code_impl_config = CodeImplementationsConfig(
                languages=list(code_impl_data["languages"])
            )

        # Create solve issue config
        try:
            solve_issue_config = SolveIssueConfig(
                llm_model=str(solve_issue_data["llm_model"]),
                temperature=float(solve_issue_data["temperature"]),
                verbal_algorithm=verbal_algo_config,
                include_mermaid_diagram=bool(solve_issue_data["include_mermaid_diagram"]),
                code_implementations=code_impl_config
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in solve_issue config: {e}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid value in solve_issue config: {e}")

        # Create and return the complete config
        return cls(
            solve_issue=solve_issue_config,
            output_directory=str(config_dict["output_directory"])
        )

    @classmethod
    def from_args(cls, args: Any) -> 'Config':
        """
        Creates a Config object from an args-like object (e.g., argparse.Namespace).

        Args:
            args: An object with attributes corresponding to the configuration values.
                  Expected attributes:
                  - llm_model: str
                  - temperature: float
                  - verbal_algorithm: bool (toggles the verbal algorithm feature)
                  - verbal_algorithm_languages: List[str]
                  - verbal_algorithm_include_pseudocode: bool
                  - include_mermaid_diagram: bool
                  - code_implementations: bool (toggles the code implementations feature)
                  - code_implementations_languages: List[str]
                  - output_directory: str
        Returns:
            An immutable Config object.
        """
        verbal_algo_config: Optional[VerbalAlgorithmConfig] = None
        if hasattr(args, 'verbal_algorithm') and args.verbal_algorithm:
            verbal_algo_config = VerbalAlgorithmConfig(
                languages=list(args.verbal_algorithm_languages if hasattr(args, 'verbal_algorithm_languages') else []),
                include_pseudocode=args.verbal_algorithm_include_pseudocode if hasattr(args, 'verbal_algorithm_include_pseudocode') else True
            )

        code_impl_config: Optional[CodeImplementationsConfig] = None
        if hasattr(args, 'code_implementations') and args.code_implementations:
            code_impl_config = CodeImplementationsConfig(
                languages=list(args.code_implementations_languages if hasattr(args, 'code_implementations_languages') else [])
            )

        solve_issue_config = SolveIssueConfig(
            llm_model=args.llm_model,
            temperature=float(args.temperature),
            verbal_algorithm=verbal_algo_config,
            include_mermaid_diagram=args.include_mermaid_diagram,
            code_implementations=code_impl_config
        )
        return cls(
            solve_issue=solve_issue_config,
            output_directory=str(args.output_directory)
        )

    def as_dict(self) -> Dict[str, Any]:
        """
        Converts the Config object to a dictionary.

        Returns:
            A dictionary representation of the configuration.
        """
        def dict_factory(data):
            d = {}
            for k, v in data:
                if isinstance(v, list):
                    d[k] = list(v)
                elif v is not None:
                    d[k] = v
            return d
        return asdict(self, dict_factory=dict_factory)

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Converts the Config object to a JSON string.

        Args:
            indent: Number of spaces to indent JSON output for pretty printing.
                   If None, the output will be compact. Default is None.

        Returns:
            A JSON string representation of the configuration.
        """
        return json.dumps(self.as_dict(), indent=indent) 