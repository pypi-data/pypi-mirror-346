import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  Alert,
  CircularProgress
} from '@mui/material';
import { AuthService } from '../services/auth-service';
import {
  getUserFromStorage,
  clearUserData,
  getApiKey,
  saveUserToStorage
} from '../config';
import {
  IUser,
  IUserResponse,
  ILoginRequest,
  IRegisterRequest
} from '../types/auth';

/**
 * UserProfile
 * Displays user profile information, including request usage and account details.
 * Allows login if not authenticated.
 */
const UserProfile: React.FC = () => {
  // Authentication state
  const [user, setUser] = useState<IUser | null>(null);
  const [userProfile, setUserProfile] = useState<IUserResponse | null>(null);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [loginData, setLoginData] = useState<ILoginRequest>({
    username: '',
    password: ''
  });
  const [registerData, setRegisterData] = useState<IRegisterRequest>({
    name: '',
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize user from storage and fetch profile data
  useEffect(() => {
    const storedUser = getUserFromStorage();
    if (storedUser) {
      setUser(storedUser);
      fetchUserProfile();
    }
  }, []);

  // Fetch user profile data from API
  const fetchUserProfile = async () => {
    const apiKey = getApiKey();
    if (!apiKey) {
      setError('No API key found. Please log in again.');
      return;
    }

    setLoading(true);
    try {
      const authService = AuthService.getInstance();
      console.log('Fetching user profile with API key length:', apiKey.length);
      console.log('API base URL:', authService.getBaseUrl());

      const profileData = await authService.getCurrentUser(apiKey);
      console.log('Profile data received:', profileData);
      setUserProfile(profileData);
      setLoading(false);
    } catch (err) {
      console.error('User profile fetch error:', err);
      let errorMessage = 'Failed to fetch user profile';

      if (err instanceof Error) {
        errorMessage = `${errorMessage}: ${err.message}`;
      } else if (typeof err === 'string') {
        errorMessage = err;
      }

      setError(errorMessage);
      setLoading(false);
    }
  };

  // Handle login
  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const authService = AuthService.getInstance();
      const response = await authService.login(loginData);

      // Create user object and save to storage
      const newUser: IUser = {
        user_id: '', // API doesn't return this in login response
        name: '', // API doesn't return this in login response
        email: loginData.username,
        api_key: response.api_key
      };

      // Save user to storage
      saveUserToStorage(newUser);

      // Update local state
      setUser(newUser);
      setLoginData({ username: '', password: '' });

      // Fetch user profile
      await fetchUserProfile();

      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
      setLoading(false);
    }
  };

  // Handle register
  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const authService = AuthService.getInstance();
      const response = await authService.register(registerData);

      // Create user object
      const newUser: IUser = {
        user_id: response.user_id,
        name: registerData.name,
        email: registerData.email,
        api_key: response.api_key
      };

      // Save user to storage
      saveUserToStorage(newUser);

      // Update local state
      setUser(newUser);
      setRegisterData({ name: '', email: '', password: '' });

      // Fetch user profile
      await fetchUserProfile();

      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
      setLoading(false);
    }
  };

  // Handle logout
  const handleLogout = () => {
    clearUserData();
    setUser(null);
    setUserProfile(null);
    setError(null);
  };

  // Handle form input changes
  const handleLoginChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLoginData(prev => ({ ...prev, [name]: value }));
  };

  const handleRegisterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setRegisterData(prev => ({ ...prev, [name]: value }));
  };

  // Switch between login and register forms
  const toggleAuthMode = () => {
    setAuthMode(prev => (prev === 'login' ? 'register' : 'login'));
    setError(null);
  };

  // Render usage bar
  const renderUsageBar = () => {
    if (!userProfile) {
      return null;
    }

    const usagePercentage = Math.min(
      Math.round((userProfile.request_count / userProfile.max_requests) * 100),
      100
    );

    return (
      <Box sx={{ mt: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
          <Typography variant="body2" color="text.secondary">
            API Usage
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {userProfile.request_count} / {userProfile.max_requests} requests
          </Typography>
        </Box>
        <Box
          sx={{
            width: '100%',
            height: 8,
            bgcolor: 'grey.200',
            borderRadius: 1,
            overflow: 'hidden'
          }}
        >
          <Box
            sx={{
              width: `${usagePercentage}%`,
              height: '100%',
              bgcolor: usagePercentage > 90 ? 'error.main' : 'primary.main',
              transition: 'width 0.5s ease-in-out'
            }}
          />
        </Box>
      </Box>
    );
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600, margin: '0 auto' }}>
      <Typography variant="h4" sx={{ mb: 2, fontWeight: 600 }}>
        User Profile
      </Typography>

      <Paper sx={{ p: 2 }} elevation={2}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
            <CircularProgress size={40} />
          </Box>
        )}

        {user && userProfile && !loading ? (
          // Logged in user with profile data
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="h6" gutterBottom>
              Account Information
            </Typography>

            <TextField
              label="Email"
              variant="outlined"
              size="small"
              value={userProfile.email || user.email}
              disabled
              fullWidth
            />

            {userProfile.name && (
              <TextField
                label="Name"
                variant="outlined"
                size="small"
                value={userProfile.name}
                disabled
                fullWidth
              />
            )}

            {renderUsageBar()}

            <Button
              variant="outlined"
              color="primary"
              onClick={handleLogout}
              disabled={loading}
              sx={{ mt: 1 }}
            >
              Logout
            </Button>
          </Box>
        ) : user && !userProfile && !loading ? (
          // Logged in but no profile data yet
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="body1">
              Loading profile information...
            </Typography>
            <Button
              variant="outlined"
              color="primary"
              onClick={fetchUserProfile}
            >
              Refresh Profile
            </Button>
            <Button variant="outlined" color="primary" onClick={handleLogout}>
              Logout
            </Button>
          </Box>
        ) : !loading ? (
          // Not logged in
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {authMode === 'login' ? (
              // Login form
              <form onSubmit={handleLogin}>
                <TextField
                  label="Email"
                  variant="outlined"
                  size="small"
                  fullWidth
                  margin="normal"
                  name="username"
                  type="email"
                  value={loginData.username}
                  onChange={handleLoginChange}
                  required
                  disabled={loading}
                />
                <TextField
                  label="Password"
                  variant="outlined"
                  size="small"
                  fullWidth
                  margin="normal"
                  name="password"
                  type="password"
                  value={loginData.password}
                  onChange={handleLoginChange}
                  required
                  disabled={loading}
                />
                <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    disabled={loading}
                  >
                    Login
                  </Button>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={toggleAuthMode}
                    disabled={loading}
                  >
                    Sign Up Instead
                  </Button>
                </Box>
              </form>
            ) : (
              // Register form
              <form onSubmit={handleRegister}>
                <TextField
                  label="Name"
                  variant="outlined"
                  size="small"
                  fullWidth
                  margin="normal"
                  name="name"
                  value={registerData.name}
                  onChange={handleRegisterChange}
                  required
                  disabled={loading}
                />
                <TextField
                  label="Email"
                  variant="outlined"
                  size="small"
                  fullWidth
                  margin="normal"
                  name="email"
                  type="email"
                  value={registerData.email}
                  onChange={handleRegisterChange}
                  required
                  disabled={loading}
                />
                <TextField
                  label="Password"
                  variant="outlined"
                  size="small"
                  fullWidth
                  margin="normal"
                  name="password"
                  type="password"
                  value={registerData.password}
                  onChange={handleRegisterChange}
                  required
                  disabled={loading}
                />
                <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    disabled={loading}
                  >
                    Sign Up
                  </Button>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={toggleAuthMode}
                    disabled={loading}
                  >
                    Login Instead
                  </Button>
                </Box>
              </form>
            )}
          </Box>
        ) : null}
      </Paper>
    </Box>
  );
};

export default UserProfile;
