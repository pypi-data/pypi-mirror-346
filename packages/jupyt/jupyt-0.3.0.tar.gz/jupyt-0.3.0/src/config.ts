import { IApiConfig, IModelConfig } from './types/api';
import { IUser } from './types/auth';

// Base URL for API
export const API_BASE_URL = 'https://juno-242959672448.us-central1.run.app';
// Default API config without authentication
export const API_CONFIG: IApiConfig = {
  baseUrl: API_BASE_URL,
  apiKey: '' // Will be populated from user authentication
};

// Initialize API key from localStorage when module is loaded
(function initializeApiKey() {
  // Only run in browser environment with localStorage available
  if (typeof localStorage !== 'undefined') {
    const storedApiKey = localStorage.getItem('jupyt_api_key');
    if (storedApiKey) {
      API_CONFIG.apiKey = storedApiKey;
      console.log('API key loaded from storage');
    }
  }
})();

// Default model configuration
export const DEFAULT_MODEL_CONFIG: IModelConfig = {
  provider: 'openai',
  model: 'gpt-4.1',
  temperature: 0.2,
  stream: true
};

// Local storage keys
const USER_STORAGE_KEY = 'jupyt_user';
const API_KEY_STORAGE_KEY = 'jupyt_api_key';
const MODEL_CONFIG_STORAGE_KEY = 'jupyt_model_config';

// User state management
export function saveUserToStorage(user: IUser): void {
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
  // Update API key in the config
  updateApiKey(user.api_key);
}

export function getUserFromStorage(): IUser | null {
  const userJson = localStorage.getItem(USER_STORAGE_KEY);
  if (!userJson) {
    return null;
  }
  try {
    return JSON.parse(userJson);
  } catch (e) {
    console.error('Failed to parse user from storage', e);
    return null;
  }
}

export function updateApiKey(apiKey: string): void {
  localStorage.setItem(API_KEY_STORAGE_KEY, apiKey);
  API_CONFIG.apiKey = apiKey;
}

export function getApiKey(): string | null {
  return localStorage.getItem(API_KEY_STORAGE_KEY);
}

export function clearUserData(): void {
  localStorage.removeItem(USER_STORAGE_KEY);
  localStorage.removeItem(API_KEY_STORAGE_KEY);
  API_CONFIG.apiKey = '';
}

// Model configuration management
export function saveModelConfig(config: IModelConfig): void {
  // Validate the model configuration before saving
  if (
    !config.model ||
    typeof config.model !== 'string' ||
    config.model.trim() === ''
  ) {
    console.warn('Attempted to save invalid model configuration');
    return;
  }

  // Ensure we're storing the exact model string as selected
  console.log('Saving model configuration:', config.model);
  localStorage.setItem(MODEL_CONFIG_STORAGE_KEY, JSON.stringify(config));
}

export function getModelConfig(): IModelConfig {
  const configJson = localStorage.getItem(MODEL_CONFIG_STORAGE_KEY);
  if (!configJson) {
    return DEFAULT_MODEL_CONFIG;
  }
  try {
    // Parse stored configuration and ensure model is valid
    const config = JSON.parse(configJson) as IModelConfig;

    // Verify that the model is a non-empty string
    if (
      !config.model ||
      typeof config.model !== 'string' ||
      config.model.trim() === ''
    ) {
      console.warn('Invalid model in stored config, using default model');
      return DEFAULT_MODEL_CONFIG;
    }

    return config;
  } catch (e) {
    console.error('Failed to parse model config from storage', e);
    return DEFAULT_MODEL_CONFIG;
  }
}
