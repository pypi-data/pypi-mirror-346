import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Link,
  Alert,
  CircularProgress
} from '@mui/material';
import { ILoginRequest } from '../../types/auth';
import { AuthService } from '../../services/auth-service';
import { saveUserToStorage } from '../../config';

interface ILoginProps {
  onSuccess: () => void;
  onRegisterClick: () => void;
}

export function Login({
  onSuccess,
  onRegisterClick
}: ILoginProps): JSX.Element {
  const [formData, setFormData] = useState<ILoginRequest>({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const authService = AuthService.getInstance();
      const response = await authService.login(formData);

      // Save user data with API key
      saveUserToStorage({
        user_id: '', // We don't receive this in login response
        name: '', // We don't receive this in login response
        email: formData.username, // Email is used as username
        api_key: response.api_key
      });

      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: 400, mx: 'auto' }}>
      <Typography
        variant="h5"
        component="h1"
        sx={{ mb: 3, textAlign: 'center' }}
      >
        Login to Jupyt
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        <TextField
          label="Email"
          type="email"
          name="username"
          fullWidth
          margin="normal"
          variant="outlined"
          value={formData.username}
          onChange={handleChange}
          required
          disabled={loading}
        />
        <TextField
          label="Password"
          type="password"
          name="password"
          fullWidth
          margin="normal"
          variant="outlined"
          value={formData.password}
          onChange={handleChange}
          required
          disabled={loading}
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          sx={{ mt: 3, mb: 2 }}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Sign In'}
        </Button>
      </form>

      <Box sx={{ textAlign: 'center', mt: 2 }}>
        <Typography variant="body2">
          Don't have an account?{' '}
          <Link
            component="button"
            variant="body2"
            onClick={onRegisterClick}
            disabled={loading}
          >
            Register now
          </Link>
        </Typography>
      </Box>
    </Box>
  );
}
