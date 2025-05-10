import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode
} from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { ThemeMode, createAppTheme } from './theme';
import { CommandRegistry } from '@lumino/commands';

// Define known JupyterLab theme names
const JUPYTERLAB_LIGHT_THEME = 'JupyterLab Light';
const JUPYTERLAB_DARK_THEME = 'JupyterLab Dark';

type ThemeContextType = {
  themeMode: ThemeMode;
  setThemeMode: (mode: ThemeMode) => void;
  currentTheme: 'light' | 'dark';
};

// Create context with default values
const ThemeContext = createContext<ThemeContextType>({
  themeMode: 'system',
  setThemeMode: () => {},
  currentTheme: 'light'
});

// Hook to use the theme context
export const useTheme = () => useContext(ThemeContext);

type ThemeProviderProps = {
  children: ReactNode;
  commands: CommandRegistry;
};

// Function to get JupyterLab's theme
const getJupyterLabTheme = (): 'light' | 'dark' => {
  if (typeof document === 'undefined') {
    return 'light'; // Default in SSR/non-browser
  }
  // Check for JupyterLab theme attribute on body or html
  const themeLight =
    document.body.getAttribute('data-jp-theme-light') === 'true' ||
    document.documentElement.getAttribute('data-jp-theme-light') === 'true';
  return themeLight ? 'light' : 'dark';
};

// Theme provider component
export const ThemeProvider: React.FC<ThemeProviderProps> = ({
  children,
  commands
}) => {
  // Get initial theme mode from localStorage or default to system
  const [themeMode, _setThemeMode] = useState<ThemeMode>(() => {
    if (typeof window !== 'undefined') {
      const savedMode = localStorage.getItem('jupyt-theme-mode');
      return (savedMode as ThemeMode) || 'system';
    }
    return 'system';
  });

  // Calculate the actual theme based on mode and JupyterLab/system preference
  const [currentTheme, setCurrentTheme] = useState<'light' | 'dark'>(() =>
    themeMode === 'system'
      ? getJupyterLabTheme()
      : (themeMode as 'light' | 'dark')
  );

  // New setThemeMode function that includes command execution
  const setThemeMode = async (mode: ThemeMode) => {
    _setThemeMode(mode); // Update internal state

    // Save preference to localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('jupyt-theme-mode', mode);
    }

    // Change JupyterLab theme if mode is light or dark
    if (mode === 'light' || mode === 'dark') {
      const targetTheme =
        mode === 'light' ? JUPYTERLAB_LIGHT_THEME : JUPYTERLAB_DARK_THEME;
      try {
        if (commands.hasCommand('apputils:change-theme')) {
          await commands.execute('apputils:change-theme', {
            theme: targetTheme
          });
          console.log(`Jupyt AI: Changed JupyterLab theme to ${targetTheme}`);
        } else {
          console.warn('Jupyt AI: Command apputils:change-theme not found.');
        }
      } catch (error) {
        console.error(
          `Jupyt AI: Failed to change JupyterLab theme to ${targetTheme}:`,
          error
        );
      }
    }
  };

  // Update the theme when internal themeMode state changes
  useEffect(() => {
    // Removed localStorage setting here, handled in setThemeMode

    // If theme is set to system, sync from JupyterLab's theme
    if (themeMode === 'system') {
      setCurrentTheme(getJupyterLabTheme());
    }
  }, [themeMode]); // Depends on internal themeMode

  // Listen for JupyterLab theme changes when in system mode
  useEffect(() => {
    if (themeMode !== 'system' || typeof document === 'undefined') {
      return;
    }

    // Use MutationObserver to detect changes in JupyterLab theme attribute
    const observer = new MutationObserver(mutations => {
      mutations.forEach(mutation => {
        if (
          mutation.type === 'attributes' &&
          (mutation.attributeName === 'data-jp-theme-light' ||
            mutation.attributeName === 'data-jp-theme-name')
        ) {
          const newJupyterLabTheme = getJupyterLabTheme();

          // Always update the visual theme
          setCurrentTheme(newJupyterLabTheme);

          // Get the current setting value *before* potentially changing it
          const currentSetting = themeMode; // Access the state variable directly

          // If the setting is not 'system' and it mismatches the new theme,
          // update the setting itself to reflect the change.
          if (
            currentSetting !== 'system' &&
            currentSetting !== newJupyterLabTheme
          ) {
            _setThemeMode(newJupyterLabTheme); // Update the state controlling the dropdown
            // Also update localStorage to persist this externally triggered change
            if (typeof window !== 'undefined') {
              localStorage.setItem('jupyt-theme-mode', newJupyterLabTheme);
            }
            console.log(
              `Jupyt AI: Setting changed to ${newJupyterLabTheme} to match external JupyterLab theme change.`
            );
          }
        }
      });
    });

    // Observe changes on body and html attributes
    observer.observe(document.body, { attributes: true });
    observer.observe(document.documentElement, { attributes: true });

    // Initial check in case the theme changed before observer was set up
    setCurrentTheme(getJupyterLabTheme());

    // Clean up observer on unmount or when mode changes
    return () => {
      observer.disconnect();
    };
  }, [themeMode]); // Re-run effect if themeMode changes

  // Create theme based on current mode
  const theme = createAppTheme(currentTheme);

  // Use the new setThemeMode in the context provider value
  return (
    <ThemeContext.Provider value={{ themeMode, setThemeMode, currentTheme }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};
