export interface IUser {
  user_id: string;
  name: string;
  email: string;
  api_key: string;
}

export interface IRegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface IRegisterResponse {
  user_id: string;
  name: string;
  email: string;
  api_key: string;
}

export interface ILoginRequest {
  username: string; // email is used as username
  password: string;
}

export interface ILoginResponse {
  access_token: string;
  token_type: string;
  api_key: string;
}

export interface IModelsResponse {
  available_models: {
    openai: string[];
    anthropic: string[];
  };
  user_preferences: {
    model: string;
    temperature: number;
    max_tokens: number;
  };
}

export interface IUserResponse {
  name: string | null;
  email: string | null;
  request_count: number;
  max_requests: number;
}
