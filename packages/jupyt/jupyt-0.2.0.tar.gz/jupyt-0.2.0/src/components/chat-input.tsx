import React from 'react';
import { Box, TextField, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import CircularProgress from '@mui/material/CircularProgress';
import StopIcon from '@mui/icons-material/Stop';
import { useEffect, useRef } from 'react';
import { ChatInputProps } from '../types/chat-input';

export function ChatInput({
  value,
  isStreaming,
  onChange,
  onSubmit,
  isAgenticLooping,
  onStopAgenticLoop
}: ChatInputProps): JSX.Element {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleCellSelected = (event: CustomEvent<any>) => {
      const cellInfo = event.detail;
      const cellRef = `@cell${cellInfo.cellNumber} `;
      
      // If there's already text, add the cell reference at the cursor position
      if (inputRef.current) {
        const cursorPos = inputRef.current.selectionStart || 0;
        const currentValue = value;
        const newValue = 
          currentValue.slice(0, cursorPos) +
          cellRef +
          currentValue.slice(cursorPos);
        onChange(newValue);
        
        // Set cursor position after the cell reference
        setTimeout(() => {
          if (inputRef.current) {
            const newCursorPos = cursorPos + cellRef.length;
            inputRef.current.focus();
            inputRef.current.setSelectionRange(newCursorPos, newCursorPos);
          }
        }, 0);
      }
    };

    document.addEventListener(
      'jupyt:cell-selected',
      handleCellSelected as EventListener
    );
    return () => {
      document.removeEventListener(
        'jupyt:cell-selected',
        handleCellSelected as EventListener
      );
    };
  }, [value, onChange]);

  return (
    <Box
      component="form"
      onSubmit={onSubmit}
      sx={{
        display: 'flex',
        gap: 1,
        p: 1,
        bgcolor: theme => 
          theme.palette.mode === 'dark' ? 'background.paper' : 'grey.50',
        borderRadius: 2,
        border: '1px solid',
        borderColor: theme => 
          theme.palette.mode === 'dark' ? 'grey.800' : 'grey.200'
      }}
    >
      <TextField
        fullWidth
        multiline
        maxRows={5}
        variant="outlined"
        placeholder="Ask a question or reference a cell with @cell1..."
        value={value}
        onChange={e => onChange(e.target.value)}
        // Using InputProps instead of onKeyDown for compatibility
        InputProps={{
          onKeyDown: e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              onSubmit(e as any);
            }
          }
        }}
        disabled={isStreaming || isAgenticLooping}
        inputRef={inputRef}
        sx={{
          '& .MuiOutlinedInput-root': {
            borderRadius: 2,
            bgcolor: theme => 
              theme.palette.mode === 'dark' ? 'background.default' : 'white'
          }
        }}
      />

      {isAgenticLooping ? (
        <IconButton
          color="warning"
          onClick={onStopAgenticLoop}
          disabled={isStreaming}
          sx={{
            alignSelf: 'flex-end',
            bgcolor: 'warning.main',
            color: 'warning.contrastText',
            '&:hover': {
              bgcolor: 'warning.dark'
            }
          }}
        >
          <StopIcon />
        </IconButton>
      ) : (
        <IconButton
          color="primary"
          type="submit"
          disabled={isStreaming || !value.trim() || isAgenticLooping}
          sx={{
            alignSelf: 'flex-end',
            bgcolor: 'primary.main',
            color: 'primary.contrastText',
            '&:hover': {
              bgcolor: 'primary.dark'
            }
          }}
        >
          {isStreaming ? 
            (
              <CircularProgress size={24} color="inherit" />
            ) : (
              <SendIcon />
            )}
        </IconButton>
      )}
    </Box>
  );
} 