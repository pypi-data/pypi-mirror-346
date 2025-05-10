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
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
          stroke="currentColor"
          strokeWidth="2"
        />
        <path
          d="M11 8L15 12L11 16"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </Button>
  );
} 