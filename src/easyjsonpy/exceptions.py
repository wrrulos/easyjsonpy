class LanguageAlreadyLoadedError(Exception):
    """Raised when the language is already loaded"""
    pass

class LanguageNotLoadedError(Exception):
    """Raised when the language is not loaded but an attempt is made to use it"""
    pass

class LanguageFileNotFoundError(FileNotFoundError):
    """Raised when the language file is not found"""
    pass

class ConfigurationAlreadyLoadedError(Exception):
    """Raised when the configuration is already loaded"""
    pass

class ConfigurationNotLoadedError(Exception):
    """Raised when the configuration is not loaded but an attempt is made to use it"""
    pass

class ConfigurationFileNotFoundError(Exception):
    """Raised when the configuration file is not found"""
    pass
