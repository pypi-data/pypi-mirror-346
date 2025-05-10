import React from 'react';
import { Button } from '@mui/material';
import { ICellAIButtonProps } from '../types/ai-button';

export function CellAIButton({
  cell,
  onCellSelect
}: ICellAIButtonProps): JSX.Element {
  const handleClick = () => {
    onCellSelect(cell);
  };

  return (
    <Button
      size="small"
      onClick={handleClick}
      sx={{
        minWidth: 'auto',
        padding: '4px',
        marginLeft: '4px',
        '&:hover': {
          backgroundColor: 'action.hover'
        }
      }}
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{ marginRight: '4px' }}
      >
        <path
          d="M8 0C3.6 0 0 3.6 0 8C0 12.4 3.6 16 8 16C12.4 16 16 12.4 16 8C16 3.6 12.4 0 8 0ZM8 14C4.7 14 2 11.3 2 8C2 4.7 4.7 2 8 2C11.3 2 14 4.7 14 8C14 11.3 11.3 14 8 14Z"
          fill="currentColor"
        />
        <path
          d="M8 4C6.3 4 5 5.3 5 7C5 8.7 6.3 10 8 10C9.7 10 11 8.7 11 7C11 5.3 9.7 4 8 4ZM8 8C7.4 8 7 7.6 7 7C7 6.4 7.4 6 8 6C8.6 6 9 6.4 9 7C9 7.6 8.6 8 8 8Z"
          fill="currentColor"
        />
      </svg>
      AI
    </Button>
  );
}
