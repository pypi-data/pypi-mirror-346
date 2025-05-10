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
import { IRegisterRequest } from '../../types/auth';
import { AuthService } from '../../services/auth-service';
import { saveUserToStorage } from '../../config';

interface IRegisterProps {
  onSuccess: () => void;
  onLoginClick: () => void;
}

export function Register({
  onSuccess,
  onLoginClick
}: IRegisterProps): JSX.Element {
  const [formData, setFormData] = useState<IRegisterRequest>({
    name: '',
    email: '',
    password: ''
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === 'confirmPassword') {
      setConfirmPassword(value);
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validate passwords match
    if (formData.password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const authService = AuthService.getInstance();
      const response = await authService.register(formData);

      // Save user data with API key
      saveUserToStorage({
        user_id: response.user_id,
        name: formData.name,
        email: formData.email,
        api_key: response.api_key
      });

      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
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
        Create Jupyt Account
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        <TextField
          label="Full Name"
          type="text"
          name="name"
          fullWidth
          margin="normal"
          variant="outlined"
          value={formData.name}
          onChange={handleChange}
          required
          disabled={loading}
        />
        <TextField
          label="Email"
          type="email"
          name="email"
          fullWidth
          margin="normal"
          variant="outlined"
          value={formData.email}
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
        <TextField
          label="Confirm Password"
          type="password"
          name="confirmPassword"
          fullWidth
          margin="normal"
          variant="outlined"
          value={confirmPassword}
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
          {loading ? <CircularProgress size={24} /> : 'Register'}
        </Button>
      </form>

      <Box sx={{ textAlign: 'center', mt: 2 }}>
        <Typography variant="body2">
          Already have an account?{' '}
          <Link
            component="button"
            variant="body2"
            onClick={onLoginClick}
            disabled={loading}
          >
            Sign in
          </Link>
        </Typography>
      </Box>
    </Box>
  );
}
