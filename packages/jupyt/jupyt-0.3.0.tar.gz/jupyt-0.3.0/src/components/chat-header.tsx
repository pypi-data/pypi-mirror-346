import React from 'react';
import { Box, Typography, IconButton, Tooltip } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
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
          mb: 2
        }}
      >
        <Typography
          variant="h4"
          component="h1"
          sx={{
            fontWeight: 600,
            color: 'text.primary',
            letterSpacing: '-0.5px',
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}
        >
          Jupyt
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Tooltip title="Start new chat">
            <IconButton
              onClick={onNewChat}
              disabled={isStreaming}
              size="small"
              sx={{
                bgcolor: 'primary.main',
                color: 'primary.contrastText',
                '&:hover': {
                  bgcolor: 'primary.dark'
                },
                '&.Mui-disabled': {
                  bgcolor: 'action.disabledBackground',
                  color: 'action.disabled'
                }
              }}
            >
              <AddIcon />
            </IconButton>
          </Tooltip>
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
