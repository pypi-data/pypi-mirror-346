import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { useTheme } from '../theme-provider';
import { ThemeMode } from '../theme';
import { ModelSelector } from './model-selector';
import { getUserFromStorage } from '../config';
import { IUser } from '../types/auth';

/**
 * JupytSettings
 * Settings page for Jupyt AI. Contains model selection and appearance/theme settings.
 * User authentication has been moved to the UserProfile component.
 */
const JupytSettings: React.FC = () => {
  const { themeMode, setThemeMode, currentTheme } = useTheme();
  const [user, setUser] = useState<IUser | null>(null);

  // Initialize user from storage
  useEffect(() => {
    const storedUser = getUserFromStorage();
    if (storedUser) {
      setUser(storedUser);
    }
  }, []);

  // Handle theme change
  const handleThemeChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setThemeMode(event.target.value as ThemeMode);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600, margin: '0 auto' }}>
      <Typography variant="h4" sx={{ mb: 2, fontWeight: 600 }}>
        Jupyt Settings
      </Typography>

      {/* Model Selection */}
      <Paper sx={{ p: 2, mb: 3 }} elevation={2}>
        <Typography variant="h6" sx={{ mb: 1 }}>
          Model Selection
        </Typography>
        {user ? (
          <ModelSelector />
        ) : (
          <FormControl fullWidth size="small">
            <InputLabel id="model-select-label">Model</InputLabel>
            <Select
              labelId="model-select-label"
              label="Model"
              value=""
              disabled
            >
              <MenuItem value="">(Login to select models)</MenuItem>
            </Select>
          </FormControl>
        )}
      </Paper>

      {/* Theme Settings */}
      <Paper sx={{ p: 2 }} elevation={2}>
        <Typography variant="h6" sx={{ mb: 1 }}>
          Appearance & Theme
        </Typography>
        <FormControl fullWidth size="small">
          <InputLabel id="theme-select-label">Theme</InputLabel>
          <Select
            labelId="theme-select-label"
            label="Theme"
            value={themeMode}
            onChange={handleThemeChange as any}
          >
            <MenuItem value="light">Light</MenuItem>
            <MenuItem value="dark">Dark</MenuItem>
            <MenuItem value="system">
              System (
              {currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1)})
            </MenuItem>
          </Select>
        </FormControl>
        <Typography variant="body2" sx={{ mt: 1, color: 'text.secondary' }}>
          Current theme:{' '}
          {currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1)}
        </Typography>
      </Paper>
    </Box>
  );
};

export default JupytSettings;
