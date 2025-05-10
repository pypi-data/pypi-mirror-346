import { Box, Button, Typography, Paper } from '@mui/material';
import { parseDiff, Diff } from 'react-diff-view';
import 'react-diff-view/style/index.css';
import { JupytPendingOperation } from '../types/cell-metadata';
import { useTheme } from '@mui/material/styles';
import React from 'react';
interface ICellApprovalControlsProps {
  pendingOperation: JupytPendingOperation;
  onApprove: () => void;
  onReject: () => void;
}

/**
 * React component rendered within a cell to show pending operation details (diff/preview)
 * and provide Approve/Reject buttons.
 */
export function CellApprovalControls({
  pendingOperation,
  onApprove,
  onReject
}: ICellApprovalControlsProps) {
  const theme = useTheme();
  const { type, code, oldCode, runNeeded } = pendingOperation;

  const renderDiff = () => {
    if (type === 'update_cell' && typeof code === 'string') {
      const currentOldCode = oldCode || '';
      const newLines = code.split('\n');
      const oldLines = currentOldCode.split('\n');

      const diffText = [
        '--- a/Original',
        '+++ b/Proposed',
        '@@ -1,' + oldLines.length + ' +1,' + newLines.length + ' @@',
        ...oldLines.map(line => '-' + line),
        ...newLines.map(line => '+' + line)
      ].join('\n');

      try {
        const files = parseDiff(diffText);
        if (!files?.[0]) {
          return null;
        }

        return (
          <Box
            sx={{
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1,
              overflow: 'hidden',
              mb: 1,
              '& .diff': {
                fontSize: '0.9em',
                color: theme.palette.text.primary,
                backgroundColor:
                  theme.palette.mode === 'dark'
                    ? '#1a1a1a'
                    : theme.palette.background.paper
              },
              '& .diff-gutter': {
                backgroundColor:
                  theme.palette.mode === 'dark' ? '#252525' : '#f0f0f0',
                color: theme.palette.mode === 'dark' ? '#888' : '#666',
                padding: '0 8px'
              },
              '& .diff-code': {
                color: theme.palette.text.primary,
                padding: '0 8px'
              },
              '& .diff-code-delete': {
                backgroundColor:
                  theme.palette.mode === 'dark'
                    ? 'rgba(255, 100, 100, 0.15)'
                    : '#ffeef0',
                color: theme.palette.mode === 'dark' ? '#ff9999' : '#cc0000'
              },
              '& .diff-code-insert': {
                backgroundColor:
                  theme.palette.mode === 'dark'
                    ? 'rgba(133, 255, 133, 0.15)'
                    : '#e6ffec',
                color: theme.palette.mode === 'dark' ? '#85ff85' : '#007700'
              },
              '& .diff-gutter-delete': {
                backgroundColor:
                  theme.palette.mode === 'dark' ? '#402020' : '#fff0f0'
              },
              '& .diff-gutter-insert': {
                backgroundColor:
                  theme.palette.mode === 'dark' ? '#204020' : '#f0fff0'
              },
              '& .diff-hunk-header': {
                backgroundColor:
                  theme.palette.mode === 'dark' ? '#303030' : '#f8f8f8',
                color: theme.palette.mode === 'dark' ? '#888' : '#666'
              }
            }}
          >
            <Diff
              viewType="unified"
              diffType={files[0].type}
              hunks={files[0].hunks}
              optimizeSelection
              gutterType="anchor"
            />
          </Box>
        );
      } catch (error) {
        console.error('Error parsing diff for cell approval:', error);
        return (
          <Typography color="error" variant="body2">
            Error displaying diff. Please check console.
          </Typography>
        );
      }
    }
    return null;
  };

  const renderCodePreview = () => {
    if (type === 'create_cell' && code) {
      return (
        <Box
          component={Paper}
          variant="outlined"
          sx={{
            p: 1.5,
            mb: 1,
            bgcolor:
              theme.palette.mode === 'dark'
                ? 'rgba(133, 255, 133, 0.1)'
                : '#e6ffec',
            fontFamily: 'monospace',
            whiteSpace: 'pre-wrap',
            overflowX: 'auto',
            fontSize: '0.9em',
            color: theme.palette.mode === 'dark' ? '#85ff85' : '#007700',
            border: '1px solid',
            borderColor:
              theme.palette.mode === 'dark'
                ? 'rgba(133, 255, 133, 0.2)'
                : '#b0eab5'
          }}
        >
          {code}
        </Box>
      );
    }
    return null;
  };

  const renderDeleteOverlay = () => {
    if (type === 'delete_cell') {
      return (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            bgcolor:
              theme.palette.mode === 'dark'
                ? 'rgba(255, 100, 100, 0.15)'
                : '#ffeef0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            p: 2,
            border: '1px dashed',
            borderColor: theme.palette.mode === 'dark' ? '#ff9999' : '#cc0000',
            borderRadius: 1,
            zIndex: 5
          }}
        >
          <Typography
            color={theme.palette.mode === 'dark' ? '#ff9999' : '#cc0000'}
            variant="h6"
          >
            Marked for Deletion
          </Typography>
        </Box>
      );
    }
    return null;
  };

  const getOperationTitle = () => {
    switch (type) {
      case 'create_cell':
        return 'Approve Cell Creation?';
      case 'update_cell':
        return 'Approve Cell Update?';
      case 'delete_cell':
        return 'Approve Cell Deletion?';
      default:
        return 'Approve Operation?';
    }
  };

  return (
    <Box
      sx={{
        border: '2px dashed',
        borderColor: 'primary.main',
        p: 1.5,
        borderRadius: 1,
        position: 'relative',
        mb: 1,
        bgcolor:
          theme.palette.mode === 'dark'
            ? 'rgba(255, 255, 255, 0.03)'
            : 'rgba(0, 0, 0, 0.02)',
        color: theme.palette.text.primary
      }}
    >
      {renderDeleteOverlay()}
      <Typography
        variant="subtitle1"
        gutterBottom
        sx={{
          fontWeight: 'bold',
          color:
            theme.palette.mode === 'dark'
              ? theme.palette.primary.light
              : theme.palette.primary.main
        }}
      >
        {getOperationTitle()}
      </Typography>

      {type === 'update_cell' ? renderDiff() : renderCodePreview()}

      {runNeeded && (
        <Typography
          variant="caption"
          display="block"
          sx={{
            mb: 1,
            fontStyle: 'italic',
            color:
              theme.palette.mode === 'dark'
                ? theme.palette.grey[400]
                : theme.palette.grey[700]
          }}
        >
          Note: This cell will be executed after approval.
        </Typography>
      )}

      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
        <Button
          size="small"
          variant="contained"
          color="primary"
          onClick={onApprove}
        >
          Approve
        </Button>
        <Button
          size="small"
          variant="outlined"
          color="error"
          onClick={onReject}
        >
          Reject
        </Button>
      </Box>
    </Box>
  );
}
