import React from 'react';
import { Box, Typography, IconButton, Tooltip } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { ModelSelector } from './model-selector';
import { ChatHeaderProps } from '../types/chat-header';

export function ChatHeader({
  isStreaming,
  currentType,
  onNewChat,
  onModelConfigChange
}: ChatHeaderProps): JSX.Element {
  return (
    <Box sx={{ py: 2 }}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 1
        }}
      >
        <Typography
          variant="h4"
          component="h1"
          sx={{
            fontWeight: 600,
            color: 'text.primary',
            letterSpacing: '-0.5px',
            fontSize: {
              xs: '1.75rem',
              sm: '2rem'
            }
          }}
        >
          Jupyt
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Tooltip title="Start new chat">
            <IconButton
              color="primary"
              onClick={onNewChat}
              disabled={isStreaming}
              sx={{
                backgroundColor: 'primary.main',
                color: 'primary.contrastText',
                '&:hover': {
                  backgroundColor: 'primary.dark'
                },
                '&.Mui-disabled': {
                  backgroundColor: 'action.disabledBackground',
                  color: 'action.disabled'
                }
              }}
            >
              <AddIcon />
            </IconButton>
          </Tooltip>
          <ModelSelector onChange={onModelConfigChange} />
        </Box>
      </Box>
      {isStreaming && currentType && (
        <Typography
          variant="body2"
          sx={{
            color: 'text.secondary',
            mt: 0.5,
            fontWeight: 400
          }}
        >
          {currentType === 'simple_query'
            ? 'Processing Query'
            : 'Agent Planning'}
        </Typography>
      )}
    </Box>
  );
} 