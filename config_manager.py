"""
Configuration Manager - Learning Version

This teaches you how to manage user preferences, settings, and configuration files.
Focus: Config files, environment variables, user defaults, and settings persistence.

Learning Goals:
- Configuration file formats (JSON, YAML, TOML)
- User settings and preferences
- Environment variable management
- XDG Base Directory specification
- Configuration validation and migration

Time: 30 minutes to implement the TODOs
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enums import LLMClient, DocumentationFormat


@dataclass
class AgentConfig:
    """
    Configuration data structure

    Learning Point: Use dataclasses for type-safe configuration
    Benefits: Validation, auto-completion, clear structure
    """

    # User preferences
    default_llm: str = "openai"
    default_format: str = "markdown"

    # Output preferences
    verbose: bool = False
    save_by_default: bool = False
    default_output_dir: str = "./docs"

    # API settings
    openai_model: str = "gpt-3.5-turbo"
    anthropic_model: str = "claude-3-5-sonnet-20240620"
    max_tokens: int = 300

    # Advanced settings
    auto_save: bool = True
    backup_original: bool = True
    batch_size: int = 10

    def validate(self) -> list[str]:
        """
        Validate configuration values

        Learning Point: Always validate user-provided configuration
        """
        errors = []

        # TODO: Validate LLM client choice
        # Hint: Check if default_llm is in LLMClient enum values
        # Learning: Enum validation patterns

        # TODO: Validate documentation format
        # Hint: Check DocumentationFormat enum
        # Learning: Cross-validation between related settings

        # TODO: Validate paths and directories
        # Hint: Check if default_output_dir can be created
        # Learning: File system validation

        # TODO: Validate numeric ranges
        # Hint: Check max_tokens is reasonable (e.g., 1-4000)
        # Learning: Numeric constraint validation

        return errors


class ConfigManager:
    """
    Manages user configuration across CLI sessions

    Learning Point: Configuration management patterns
    - Where to store config files
    - How to handle defaults vs user overrides
    - Configuration file format selection
    """

    def __init__(self, app_name: str = "ai-doc-agent"):
        self.app_name = app_name

        # TODO: Implement XDG Base Directory specification
        # Hint: Use os.environ.get("XDG_CONFIG_HOME") with fallback
        # Learning: Cross-platform configuration directories
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"

        # TODO: Initialize user data directory
        # Hint: Similar to config_dir but for user data
        # Learning: Separating config from data

        self._ensure_directories()

    def _get_config_dir(self) -> Path:
        """
        Get platform-appropriate configuration directory

        Learning Point: Cross-platform file system conventions
        - Linux: ~/.config/app-name
        - macOS: ~/Library/Application Support/app-name
        - Windows: %APPDATA%/app-name
        """
        # TODO: Implement XDG Base Directory spec
        # Linux: $XDG_CONFIG_HOME/app-name or ~/.config/app-name
        # macOS: ~/Library/Application Support/app-name
        # Windows: %APPDATA%/app-name

        # Simplified version for learning:
        home = Path.home()
        if os.name == "nt":  # Windows
            return home / "AppData" / "Roaming" / self.app_name
        elif os.uname().sysname == "Darwin":  # macOS
            return home / "Library" / "Application Support" / self.app_name
        else:  # Linux/Unix
            return home / ".config" / self.app_name

    def _ensure_directories(self):
        """
        Create configuration directories if they don't exist

        Learning Point: Graceful directory creation
        """
        # TODO: Create config directory with proper permissions
        # Hint: Use Path.mkdir(parents=True, exist_ok=True)
        # Learning: Safe directory creation patterns

        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ Warning: Could not create config directory: {e}")

    def load_config(self) -> AgentConfig:
        """
        Load configuration from file, with fallback to defaults

        Learning Point: Graceful degradation in configuration loading
        """
        if not self.config_file.exists():
            # TODO: Create default config file on first run
            # Learning: First-run experience design
            return self._create_default_config()

        try:
            # TODO: Load and parse JSON configuration
            # Hint: Use json.loads() with proper error handling
            # Learning: Configuration file parsing

            with open(self.config_file, "r") as f:
                data = json.load(f)

            # TODO: Convert dict to AgentConfig dataclass
            # Hint: Use **data to unpack dictionary
            # Learning: Dictionary to dataclass conversion

            config = AgentConfig(**data)

            # TODO: Validate loaded configuration
            # Learning: Runtime configuration validation
            errors = config.validate()
            if errors:
                print("⚠️  Configuration validation errors:")
                for error in errors:
                    print(f"   • {error}")
                print("Using defaults for invalid settings.")

            return config

        except json.JSONDecodeError as e:
            print(f"❌ Invalid configuration file: {e}")
            print("Using default configuration.")
            return AgentConfig()

        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return AgentConfig()

    def save_config(self, config: AgentConfig):
        """
        Save configuration to file

        Learning Point: Configuration persistence strategies
        """
        try:
            # TODO: Convert dataclass to dictionary
            # Hint: Use asdict() from dataclasses
            # Learning: Dataclass serialization

            data = asdict(config)

            # TODO: Write JSON with pretty formatting
            # Hint: Use json.dump() with indent parameter
            # Learning: Human-readable configuration files

            with open(self.config_file, "w") as f:
                json.dump(data, f, indent=2)

            print(f"✅ Configuration saved to {self.config_file}")

        except Exception as e:
            print(f"❌ Error saving configuration: {e}")

    def _create_default_config(self) -> AgentConfig:
        """
        Create and save default configuration

        Learning Point: First-run configuration setup
        """
        config = AgentConfig()

        # TODO: Save default config to file
        # Learning: Persisting defaults for user modification
        self.save_config(config)

        print(f"📝 Created default configuration at {self.config_file}")
        print("💡 Edit this file to customize your preferences")

        return config

    def update_config(self, **kwargs):
        """
        Update specific configuration values

        Learning Point: Partial configuration updates
        """
        config = self.load_config()

        # TODO: Update config attributes from kwargs
        # Hint: Use setattr() to update attributes dynamically
        # Learning: Dynamic attribute updating

        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
                print(f"✅ Updated {key} = {value}")
            else:
                print(f"⚠️  Unknown setting: {key}")

        # TODO: Validate and save updated configuration
        # Learning: Update-time validation
        self.save_config(config)

    def reset_config(self):
        """
        Reset configuration to defaults

        Learning Point: Configuration reset functionality
        """
        # TODO: Create backup of current config
        # Hint: Copy current file to config.json.backup
        # Learning: Safe configuration operations

        if self.config_file.exists():
            backup_path = self.config_file.with_suffix(".json.backup")
            # TODO: Copy file to backup location
            print(f"📦 Backed up current config to {backup_path}")

        # TODO: Create fresh default configuration
        # Learning: Reset workflows
        config = AgentConfig()
        self.save_config(config)
        print("🔄 Configuration reset to defaults")

    def show_config(self):
        """
        Display current configuration

        Learning Point: Configuration introspection
        """
        config = self.load_config()

        print("⚙️  Current Configuration:")
        print("-" * 30)

        # TODO: Display configuration in organized sections
        # Hint: Group related settings together
        # Learning: User-friendly configuration display

        # Basic settings
        print("📋 Basic Settings:")
        print(f"   Default LLM: {config.default_llm}")
        print(f"   Default Format: {config.default_format}")
        print(f"   Verbose Output: {config.verbose}")

        # Output settings
        print("\n📁 Output Settings:")
        print(f"   Save by Default: {config.save_by_default}")
        print(f"   Output Directory: {config.default_output_dir}")
        print(f"   Auto Save: {config.auto_save}")

        # TODO: Add more sections for API settings, advanced settings
        # Learning: Organized information presentation

        print(f"\n📍 Config file: {self.config_file}")

    def get_env_overrides(self) -> Dict[str, Any]:
        """
        Get configuration overrides from environment variables

        Learning Point: Environment variables vs config files
        Precedence: env vars > config file > defaults
        """
        overrides = {}

        # TODO: Check for AI_DOC_* environment variables
        # Hint: Use os.environ.get() with AI_DOC_ prefix
        # Learning: Environment variable naming conventions

        env_mappings = {
            "AI_DOC_LLM": "default_llm",
            "AI_DOC_FORMAT": "default_format",
            "AI_DOC_VERBOSE": "verbose",
            "AI_DOC_OUTPUT_DIR": "default_output_dir",
            # TODO: Add more mappings
        }

        for env_var, config_key in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                # TODO: Type conversion based on config_key
                # Hint: Convert string values to appropriate types
                # Learning: Environment variable type handling

                if config_key == "verbose":
                    overrides[config_key] = value.lower() in ("true", "1", "yes")
                else:
                    overrides[config_key] = value

        return overrides

    def merge_config(
        self, base_config: AgentConfig, overrides: Dict[str, Any]
    ) -> AgentConfig:
        """
        Merge configuration with overrides

        Learning Point: Configuration precedence and merging
        """
        # TODO: Create new config with overrides applied
        # Hint: Use dataclass.replace() or manual attribute setting
        # Learning: Immutable configuration updates

        config_dict = asdict(base_config)
        config_dict.update(overrides)

        return AgentConfig(**config_dict)


def demo_config_manager():
    """
    Demonstrate configuration management

    Learning Point: Configuration testing and examples
    """
    print("🔧 Configuration Manager Demo")
    print("=" * 40)

    # TODO: Create config manager and show initial state
    # Learning: Configuration lifecycle

    manager = ConfigManager()

    print("\n1. Loading configuration...")
    config = manager.load_config()
    manager.show_config()

    print("\n2. Updating a setting...")
    manager.update_config(verbose=True, default_format="numpy")

    print("\n3. Environment override example...")
    # TODO: Show how environment variables override config
    # Learning: Configuration precedence demonstration

    print("\n4. Configuration validation...")
    # TODO: Show validation errors
    # Learning: Error handling examples


if __name__ == "__main__":
    print("🔧 Configuration Manager - Learning Version")
    print("📝 Implement the TODOs to create robust config management")
    print()
    print("🎯 Learning Goals:")
    print("   • Configuration file formats and locations")
    print("   • Environment variable integration")
    print("   • Configuration validation and errors")
    print("   • User preference persistence")
    print("   • Cross-platform compatibility")
    print()

    # TODO: Uncomment when ready to test
    # demo_config_manager()
