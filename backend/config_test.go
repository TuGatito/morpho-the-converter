package backend

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func TestConfigManagement(t *testing.T) {
	// Create a temporary directory for testing
	tempDir, err := os.MkdirTemp("", "morpho-test-*")
	if err != nil {
		t.Fatalf("failed to create temp directory for testing: %v", err)
	}
	defer os.RemoveAll(tempDir)

	// Mock the config path function to point to our temp directory
	testConfigPath := filepath.Join(tempDir, AppDirName, ConfigFileName)
	getConfigPathFn = func() (string, error) {
		return testConfigPath, nil
	}

	// Ensure we restore the original function after test finishes
	defer func() {
		getConfigPathFn = GetConfigPath
	}()

	// 1. Test ConfigExists when file does not exist
	if ConfigExists() {
		t.Errorf("ConfigExists() should be false initially, but was true")
	}

	// 2. Test ReadConfig (triggers default creation when not existing)
	config, err := ReadConfig()
	if err != nil {
		t.Fatalf("ReadConfig() failed on non-existing config: %v", err)
	}

	if config == nil {
		t.Fatalf("ReadConfig() returned nil config")
	}

	if config.Lang != "es" {
		t.Errorf("Expected default lang 'es', got '%s'", config.Lang)
	}

	if config.Theme != "dracula" {
		t.Errorf("Expected default theme 'dracula', got '%s'", config.Theme)
	}

	// 3. Test ConfigExists now that the default has been created
	if !ConfigExists() {
		t.Errorf("ConfigExists() should be true after default config creation")
	}

	// Verify the file actually exists and has correct permissions/content
	data, err := os.ReadFile(testConfigPath)
	if err != nil {
		t.Fatalf("failed to read created config file: %v", err)
	}

	var parsedConfig Config
	if err := json.Unmarshal(data, &parsedConfig); err != nil {
		t.Fatalf("failed to parse config JSON: %v", err)
	}

	if parsedConfig.Lang != "es" || parsedConfig.Theme != "dracula" {
		t.Errorf("Written JSON does not match defaults: %+v", parsedConfig)
	}

	// 4. Test UpdateConfig
	err = UpdateConfig("en", "nord")
	if err != nil {
		t.Fatalf("UpdateConfig() failed: %v", err)
	}

	// Verify update via ReadConfig
	updatedConfig, err := ReadConfig()
	if err != nil {
		t.Fatalf("ReadConfig() failed after update: %v", err)
	}

	if updatedConfig.Lang != "en" {
		t.Errorf("Expected updated lang 'en', got '%s'", updatedConfig.Lang)
	}

	if updatedConfig.Theme != "nord" {
		t.Errorf("Expected updated theme 'nord', got '%s'", updatedConfig.Theme)
	}
}

func TestGetConfigPath(t *testing.T) {
	path, err := GetConfigPath()
	if err != nil {
		t.Fatalf("GetConfigPath() returned unexpected error: %v", err)
	}

	if path == "" {
		t.Errorf("GetConfigPath() returned empty path")
	}

	// Verify config file path ends with the expected folder structure
	expectedSuffix := filepath.Join(AppDirName, ConfigFileName)
	if len(path) < len(expectedSuffix) || path[len(path)-len(expectedSuffix):] != expectedSuffix {
		t.Errorf("Expected config path to end with '%s', got '%s'", expectedSuffix, path)
	}
}
