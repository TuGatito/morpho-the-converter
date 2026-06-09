import json
import os
import platform

class Config:
    """
    Represents the application configuration structure.
    Stores user preferences such as language and theme.
    """
    def __init__(self, lang: str, theme: str):
        self.lang = lang
        self.theme = theme

    def to_dict(self) -> dict:
        """
        Serializes the Config instance to a dictionary.
        
        Returns:
            dict: The configuration as a dictionary.
        """
        return {"lang": self.lang, "theme": self.theme}

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a Config instance from a dictionary.
        Falls back to default values if keys are missing.
        
        Args:
            data (dict): The dictionary containing configuration data.
            
        Returns:
            Config: A new instance of Config.
        """
        return cls(lang=data.get("lang", "es"), theme=data.get("theme", "dracula"))

# Application directory and configuration file names
APP_DIR_NAME = "MorphoTheConverter"
CONFIG_FILE_NAME = "config.json"

def get_config_path() -> str:
    """
    Returns the platform-specific absolute path to the configuration file.
    
    It detects the operating system using platform.system():
    - Windows: %APPDATA%/MorphoTheConverter/config.json
    - Linux: ~/.config/MorphoTheConverter/config.json (or XDG_CONFIG_HOME)
    - macOS: ~/Library/Application Support/MorphoTheConverter/config.json
    
    Returns:
        str: The absolute path to the configuration file.
        
    Raises:
        ValueError: If required environment variables (like APPDATA or HOME) are not defined.
    """
    system = platform.system()
    base_dir = ""

    if system == "Windows":
        base_dir = os.environ.get("APPDATA")
        if not base_dir:
            raise ValueError("APPDATA environment variable is empty or not defined")
    elif system == "Darwin":
        home = os.environ.get("HOME")
        if not home:
            raise ValueError("HOME environment variable is empty or not defined")
        # macOS standard directory for application support files
        base_dir = os.path.join(home, "Library", "Application Support")
    else:
        # Linux and other Unix-like systems
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            base_dir = xdg_config
        else:
            home = os.environ.get("HOME")
            if not home:
                raise ValueError("HOME environment variable is empty or not defined")
            base_dir = os.path.join(home, ".config")
    
    return os.path.join(base_dir, APP_DIR_NAME, CONFIG_FILE_NAME)

# Function pointer for testing overrides
_get_config_path_fn = get_config_path

def config_exists() -> bool:
    """
    Checks whether the configuration file exists on the system.
    
    Returns:
        bool: True if the configuration file exists and is a file, False otherwise.
    """
    try:
        path = _get_config_path_fn()
        return os.path.isfile(path)
    except Exception:
        return False

def create_default_config() -> Config:
    """
    Creates the configuration file with default values: lang = "es" and theme = "dracula".
    It creates the parent directory structure if it does not exist.
    
    Returns:
        Config: The newly created default configuration object.
    """
    path = _get_config_path_fn()
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    
    default_config = Config(lang="es", theme="dracula")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(default_config.to_dict(), f, indent=2)
        
    return default_config

def read_config() -> Config:
    """
    Reads the configuration file and returns its values as a Config object.
    If the configuration file does not exist, it automatically creates it
    with default values.
    
    Returns:
        Config: The current configuration object.
    """
    if not config_exists():
        return create_default_config()
    
    path = _get_config_path_fn()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return Config.from_dict(data)

def update_config(lang: str, theme: str) -> None:
    """
    Updates the configuration file with the new language and theme.
    If the file or its parent directories do not exist, they will be initialized first.
    
    Args:
        lang (str): The language code to set (e.g., 'es').
        theme (str): The theme name to set (e.g., 'dracula').
    """
    path = _get_config_path_fn()
    if not config_exists():
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        
    config = Config(lang=lang, theme=theme)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config.to_dict(), f, indent=2)
