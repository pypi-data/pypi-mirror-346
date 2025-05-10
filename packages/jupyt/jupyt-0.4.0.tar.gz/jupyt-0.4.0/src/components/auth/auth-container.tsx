import React, { useState } from 'react';
import { Box, Paper } from '@mui/material';
import { Login } from './login';
import { Register } from './register';

interface IAuthContainerProps {
  onAuthSuccess: () => void;
}

enum AuthView {
  LOGIN,
  REGISTER
}

export function AuthContainer({
  onAuthSuccess
}: IAuthContainerProps): JSX.Element {
  const [currentView, setCurrentView] = useState<AuthView>(AuthView.LOGIN);

  const handleViewChange = (view: AuthView) => {
    setCurrentView(view);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        bgcolor: 'background.default',
        p: 2
      }}
    >
      <Paper
        elevation={3}
        sx={{ width: '100%', maxWidth: 450, borderRadius: 2 }}
      >
        {currentView === AuthView.LOGIN ? (
          <Login
            onSuccess={onAuthSuccess}
            onRegisterClick={() => handleViewChange(AuthView.REGISTER)}
          />
        ) : (
          <Register
            onSuccess={onAuthSuccess}
            onLoginClick={() => handleViewChange(AuthView.LOGIN)}
          />
        )}
      </Paper>
    </Box>
  );
}
