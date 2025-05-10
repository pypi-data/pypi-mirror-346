import React, { useEffect, useRef } from 'react';
import { Box, TextField, IconButton, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import StopIcon from '@mui/icons-material/Stop';
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
            inputRef.current.setSelectionRange(newCursorPos, newCursorPos);
            inputRef.current.focus();
          }
        }, 0);
      } else {
        onChange(cellRef);
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
        maxRows={4}
        variant="outlined"
        placeholder="Ask Jupyt AI anything... Use @cell to reference cells and @search to find datasets"
        value={value}
        onChange={e => onChange(e.target.value)}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSubmit(e);
          }
        }}
        disabled={isStreaming}
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
          color="error"
          onClick={onStopAgenticLoop}
          sx={{
            bgcolor: 'error.main',
            color: 'white',
            '&:hover': {
              bgcolor: 'error.dark'
            }
          }}
        >
          <StopIcon />
        </IconButton>
      ) : (
        <IconButton
          color="primary"
          onClick={onSubmit}
          disabled={!value.trim() || isStreaming}
          sx={{
            bgcolor: 'primary.main',
            color: 'white',
            '&:hover': {
              bgcolor: 'primary.dark'
            },
            '&.Mui-disabled': {
              bgcolor: 'grey.300',
              color: 'grey.500'
            }
          }}
        >
          {isStreaming ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            <SendIcon />
          )}
        </IconButton>
      )}
    </Box>
  );
}
