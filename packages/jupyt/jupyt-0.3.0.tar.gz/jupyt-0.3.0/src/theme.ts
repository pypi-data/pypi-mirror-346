import { createTheme, Theme, ThemeOptions } from '@mui/material/styles';

export type ThemeMode = 'light' | 'dark' | 'system';

// Helper function to read JupyterLab CSS variables
const getJupyterLabColor = (varName: string, fallback: string): string => {
  if (typeof window === 'undefined' || !document) {
    return fallback;
  }
  // Try to get the color from JupyterLab CSS variables
  const computedStyle = window.getComputedStyle(document.documentElement);
  return computedStyle.getPropertyValue(varName).trim() || fallback;
};

// Light theme configuration that integrates with JupyterLab
export const lightThemeOptions: ThemeOptions = {
  palette: {
    mode: 'light',
    primary: {
      main: getJupyterLabColor('--jp-brand-color1', '#1976d2')
    },
    secondary: {
      main: getJupyterLabColor('--jp-warn-color0', '#dc004e')
    },
    background: {
      default: getJupyterLabColor('--jp-layout-color0', '#f5f5f5'),
      paper: getJupyterLabColor('--jp-layout-color1', '#ffffff')
    },
    text: {
      primary: getJupyterLabColor('--jp-content-font-color0', '#212121'),
      secondary: getJupyterLabColor('--jp-content-font-color2', '#757575')
    },
    divider: getJupyterLabColor('--jp-border-color1', '#e0e0e0')
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          color: getJupyterLabColor('--jp-content-font-color0', '#212121'),
          backgroundColor: 'transparent'
        }
      }
    }
  }
};

// Dark theme configuration that integrates with JupyterLab
export const darkThemeOptions: ThemeOptions = {
  palette: {
    mode: 'dark',
    primary: {
      main: getJupyterLabColor('--jp-brand-color1', '#90caf9')
    },
    secondary: {
      main: getJupyterLabColor('--jp-warn-color0', '#f48fb1')
    },
    background: {
      default: getJupyterLabColor('--jp-layout-color0', '#121212'),
      paper: getJupyterLabColor('--jp-layout-color1', '#1e1e1e')
    },
    text: {
      primary: getJupyterLabColor('--jp-content-font-color0', '#e0e0e0'),
      secondary: getJupyterLabColor('--jp-content-font-color2', '#a0a0a0')
    },
    divider: getJupyterLabColor('--jp-border-color1', '#424242')
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          color: getJupyterLabColor('--jp-content-font-color0', '#e0e0e0'),
          backgroundColor: 'transparent'
        }
      }
    }
  }
};

// Create theme based on the mode
export const createAppTheme = (mode: 'light' | 'dark'): Theme => {
  return createTheme(mode === 'light' ? lightThemeOptions : darkThemeOptions);
};

// Get system color scheme preference
export const getSystemThemePreference = (): 'light' | 'dark' => {
  if (typeof window !== 'undefined' && window.matchMedia) {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }
  return 'light'; // Default to light if matchMedia is not available
};
