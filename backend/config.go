package backend

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
)

// Config represents the application configuration structure.
type Config struct {
	Lang  string `json:"lang"`
	Theme string `json:"theme"`
}

const (
	// AppDirName is the directory name used to store application configurations.
	AppDirName = "MorphoTheConverter"
	// ConfigFileName is the configuration file name.
	ConfigFileName = "config.json"
)

// getConfigPathFn is a package-level variable that holds the function to retrieve
// the configuration file path. This allows overriding it during unit testing.
var getConfigPathFn = GetConfigPath

// GetConfigPath returns the platform-specific absolute path to the configuration file.
// It detects the operating system using runtime.GOOS:
// - Windows: %APPDATA%/MorphoTheConverter/config.json
// - Linux: ~/.config/MorphoTheConverter/config.json (or XDG_CONFIG_HOME)
// - macOS: ~/Library/Application Support/MorphoTheConverter/config.json
func GetConfigPath() (string, error) {
	var baseDir string

	switch runtime.GOOS {
	case "windows":
		baseDir = os.Getenv("APPDATA")
		if baseDir == "" {
			return "", fmt.Errorf("APPDATA environment variable is empty or not defined")
		}
	case "darwin": // macOS
		home := os.Getenv("HOME")
		if home == "" {
			return "", fmt.Errorf("HOME environment variable is empty or not defined")
		}
		baseDir = filepath.Join(home, "Library", "Application Support")
	default: // Linux and other Unix-like systems
		xdgConfig := os.Getenv("XDG_CONFIG_HOME")
		if xdgConfig != "" {
			baseDir = xdgConfig
		} else {
			home := os.Getenv("HOME")
			if home == "" {
				return "", fmt.Errorf("HOME environment variable is empty or not defined")
			}
			baseDir = filepath.Join(home, ".config")
		}
	}

	return filepath.Join(baseDir, AppDirName, ConfigFileName), nil
}

// ConfigExists checks whether the configuration file exists on the system.
// It dynamically resolves the file path based on the operating system.
func ConfigExists() bool {
	path, err := getConfigPathFn()
	if err != nil {
		return false
	}

	info, err := os.Stat(path)
	if err != nil {
		return false
	}

	return !info.IsDir()
}

// CreateDefaultConfig creates the configuration file with default values:
// lang = "es" and theme = "dracula".
// It creates the parent directory structure if it does not exist.
func CreateDefaultConfig() (*Config, error) {
	path, err := getConfigPathFn()
	if err != nil {
		return nil, fmt.Errorf("failed to determine config path: %w", err)
	}

	// Ensure the parent directory structure exists
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create config directory: %w", err)
	}

	defaultConfig := &Config{
		Lang:  "es",
		Theme: "dracula",
	}

	data, err := json.MarshalIndent(defaultConfig, "", "  ")
	if err != nil {
		return nil, fmt.Errorf("failed to marshal default configuration: %w", err)
	}

	if err := os.WriteFile(path, data, 0644); err != nil {
		return nil, fmt.Errorf("failed to write default config file: %w", err)
	}

	return defaultConfig, nil
}

// ReadConfig reads the configuration file and returns its values.
// If the configuration file does not exist, it automatically creates it
// with default values.
func ReadConfig() (*Config, error) {
	if !ConfigExists() {
		return CreateDefaultConfig()
	}

	path, err := getConfigPathFn()
	if err != nil {
		return nil, fmt.Errorf("failed to determine config path: %w", err)
	}

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("failed to parse config file JSON: %w", err)
	}

	return &config, nil
}

// UpdateConfig updates the configuration file with the new language and theme.
// If the file does not exist, it will be initialized first.
func UpdateConfig(lang string, theme string) error {
	path, err := getConfigPathFn()
	if err != nil {
		return fmt.Errorf("failed to determine config path: %w", err)
	}

	// Check if file exists, if not ensure directory is created
	if !ConfigExists() {
		dir := filepath.Dir(path)
		if err := os.MkdirAll(dir, 0755); err != nil {
			return fmt.Errorf("failed to create config directory: %w", err)
		}
	}

	config := &Config{
		Lang:  lang,
		Theme: theme,
	}

	data, err := json.MarshalIndent(config, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal updated configuration: %w", err)
	}

	if err := os.WriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("failed to write updated config file: %w", err)
	}

	return nil
}
