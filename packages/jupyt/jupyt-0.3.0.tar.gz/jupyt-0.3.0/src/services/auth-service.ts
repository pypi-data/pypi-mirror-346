import { API_CONFIG } from '../config';
import {
  IRegisterRequest,
  IRegisterResponse,
  ILoginRequest,
  ILoginResponse,
  IModelsResponse,
  IUserResponse
} from '../types/auth';

export class AuthService {
  private static instance: AuthService;
  private baseUrl = API_CONFIG.baseUrl;

  private constructor() {}

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  /**
   * Get the base URL used for API requests
   */
  public getBaseUrl(): string {
    return this.baseUrl;
  }

  /**
   * Register a new user
   */
  public async register(
    userData: IRegisterRequest
  ): Promise<IRegisterResponse> {
    const response = await fetch(`${this.baseUrl}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `Registration failed: ${response.status}`
      );
    }

    return await response.json();
  }

  /**
   * Login a user and get access token
   */
  public async login(credentials: ILoginRequest): Promise<ILoginResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${this.baseUrl}/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData.toString()
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `Login failed: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Get available models
   */
  public async getAvailableModels(apiKey: string): Promise<IModelsResponse> {
    const response = await fetch(`${this.baseUrl}/models`, {
      method: 'GET',
      headers: {
        'X-API-Key': apiKey
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `Failed to fetch models: ${response.status}`
      );
    }

    return await response.json();
  }

  /**
   * Get current user's profile information
   */
  public async getCurrentUser(apiKey: string): Promise<IUserResponse> {
    const response = await fetch(`${this.baseUrl}/users/me`, {
      method: 'GET',
      headers: {
        'X-API-Key': apiKey
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `Failed to fetch user profile: ${response.status}`
      );
    }

    return await response.json();
  }
}
