import React from 'react';
import { Box, Button, Tooltip, IconButton } from '@mui/material';
// We're not using react-diff-view anymore, remove this import
import { JupytPendingOperation } from '../types/cell-metadata';
import { styled } from '@mui/material/styles';

// Simple implementation of diffLines to handle basic case
type DiffPart = {
  value: string;
  added?: boolean;
  removed?: boolean;
};

function diffLines(oldStr: string, newStr: string): DiffPart[] {
  const result: DiffPart[] = [];
  
  if (oldStr === newStr) {
    result.push({ value: oldStr });
    return result;
  }
  
  // Super basic diff implementation for simple cases
  result.push({ value: oldStr, removed: true });
  result.push({ value: newStr, added: true });
  
  return result;
}

// Styled components
const ApprovalControlsContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  width: '100%',
  marginTop: '8px',
  borderRadius: '4px',
  overflow: 'hidden'
}));

const ButtonsContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'flex-end',
  gap: '8px',
  padding: '8px'
}));

const DiffContainer = styled(Box)(({ theme }) => ({
  width: '100%',
  maxHeight: '300px',
  overflow: 'auto',
  borderRadius: '4px',
  border: '1px solid',
  borderColor: theme.palette.divider,
  backgroundColor: theme.palette.background.paper,
  padding: '8px',
  fontFamily: 'monospace',
  fontSize: '0.85rem',
  whiteSpace: 'pre-wrap'
}));

// The props interface for the CellApprovalControls component
interface ICellApprovalControlsProps {
  originalCode: string;
  pendingOperation: JupytPendingOperation;
  onApprove: () => void;
  onReject: () => void;
}

// The CellApprovalControls component
export const CellApprovalControls: React.FC<ICellApprovalControlsProps> = ({
  originalCode,
  pendingOperation,
  onApprove,
  onReject
}) => {
  
  // Function to render the diff between old and new code
  const renderDiff = () => {
    if (pendingOperation.type === 'update_cell' && pendingOperation.code) {
      const newCode = pendingOperation.code || '';
      // const diffResult = diffLines(originalCode, newCode);
      
      return (
        <DiffContainer>
          {/* {diffResult.map((part, index) => {
            return (
              <div 
                key={index} 
                style={{ 
                  backgroundColor: part.added ? 'rgba(0, 255, 0, 0.1)' : part.removed ? 'rgba(255, 0, 0, 0.1)' : 'transparent',
                  padding: '2px 0'
                }}
              >
                {part.value}
              </div>
            );
          })} */}
          <div style={{ backgroundColor: 'rgba(255, 0, 0, 0.1)', padding: '2px 0' }}>
            {originalCode}
          </div>
          <div style={{ backgroundColor: 'rgba(0, 255, 0, 0.1)', padding: '2px 0' }}>
            {newCode}
          </div>
        </DiffContainer>
      );
    }
    
    return null;
  };
  
  // Function to get a description of the operation
  const getOperationDescription = (): string => {
    switch (pendingOperation.type) {
      case 'create_cell':
        return `Create new cell ${pendingOperation.originalIndex !== undefined ? 'at position ' + (pendingOperation.originalIndex + 1) : ''}`;
      case 'update_cell':
        return `Update cell ${pendingOperation.originalIndex !== undefined ? 'at position ' + (pendingOperation.originalIndex + 1) : ''}`;
      case 'delete_cell':
        return `Delete cell ${pendingOperation.originalIndex !== undefined ? 'at position ' + (pendingOperation.originalIndex + 1) : ''}`;
      default:
        return 'Unknown operation';
    }
  };
  
  return (
    <ApprovalControlsContainer>
      <Box
        sx={{
          p: 1,
          bgcolor: 'info.main',
          color: 'info.contrastText',
          fontWeight: 'bold'
        }}
      >
        {getOperationDescription()}
      </Box>
      
      {renderDiff()}
      
      <ButtonsContainer>
        <Button
          variant="outlined"
          color="error"
          size="small"
          onClick={onReject}
        >
          Reject
        </Button>
        <Button
          variant="contained"
          color="success"
          size="small"
          onClick={onApprove}
        >
          Approve
        </Button>
      </ButtonsContainer>
    </ApprovalControlsContainer>
  );
} 