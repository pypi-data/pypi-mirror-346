import React from 'react';
import { Box, Typography, IconButton, Button } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import EditIcon from '@mui/icons-material/Edit';
import ReactMarkdown from 'react-markdown';
import { Components } from 'react-markdown';
import CircularProgress from '@mui/material/CircularProgress';
import { CellOperation } from '../types/stream';
import { CodeCell } from '@jupyterlab/cells';
import ReplayIcon from '@mui/icons-material/Replay';
import { ChatMessageProps } from '../types/chat-message';

export function ChatMessage({
  role,
  content,
  onCopyCode,
  onExecuteCode,
  onModifyCell,
  referencedCells = new Set(),
  operations,
  showNotification,
  onRevertOperation,
  canRevertOperation,
  notebookPanel
}: ChatMessageProps): JSX.Element {
  const isUser = role === 'user';
  const hasOperationWithCode = !!operations?.some(
    op => op.code && op.code.trim()
  );

  console.log('operations', operations);

  const [revertStates, setRevertStates] = React.useState<
    Record<number, 'idle' | 'checking' | 'reverting' | 'disabled'>
  >({});
  const [canRevertFlags, setCanRevertFlags] = React.useState<
    Record<number, boolean>
  >({});

  React.useEffect(() => {
    if (
      role === 'assistant' &&
      operations &&
      operations.length > 0 &&
      canRevertOperation
    ) {
      const checkRevertStatus = async () => {
        const initialStates: Record<number, 'idle' | 'checking'> = {};
        const flags: Record<number, boolean> = {};
        operations.forEach((_, index) => {
          initialStates[index] = 'checking';
          flags[index] = false;
        });
        setRevertStates(initialStates);
        setCanRevertFlags(flags);

        for (let i = 0; i < operations.length; i++) {
          const op = operations[i];
          if (op.type !== 'delete_cell') {
            const canRevert = await canRevertOperation(op);
            setCanRevertFlags(prev => ({ ...prev, [i]: canRevert }));
            setRevertStates(prev => ({ ...prev, [i]: 'idle' }));
          } else {
            setRevertStates(prev => ({ ...prev, [i]: 'disabled' }));
          }
        }
      };
      checkRevertStatus();
    }
  }, [operations, canRevertOperation, role]);

  const handleRevertClick = async (op: CellOperation, index: number) => {
    if (!onRevertOperation || !notebookPanel) {
      return;
    }

    setRevertStates(prev => ({ ...prev, [index]: 'reverting' }));

    const notebook = notebookPanel.content;
    let targetCell: CodeCell | undefined = undefined;

    if (op.type === 'update_cell' && typeof op.cell_index === 'number') {
      targetCell = notebook.widgets[op.cell_index] as CodeCell;
    } else if (op.type === 'create_cell' && typeof op.cell_index === 'number') {
      targetCell = notebook.widgets[op.cell_index] as CodeCell;
    }

    if (targetCell) {
      try {
        await onRevertOperation(op, targetCell);
        const canStillRevert = await canRevertOperation?.(op);
        setCanRevertFlags(prev => ({ ...prev, [index]: !!canStillRevert }));
        setRevertStates(prev => ({ ...prev, [index]: 'idle' }));
      } catch (e) {
        console.error('Revert failed:', e);
        showNotification?.('Failed to revert operation.', 'error');
        setRevertStates(prev => ({ ...prev, [index]: 'idle' }));
      }
    } else {
      showNotification?.('Could not find target cell to revert.', 'error');
      setRevertStates(prev => ({ ...prev, [index]: 'idle' }));
    }
  };

  const renderSpecialState = () => {
    if (content.includes('[Processing cell operation...]')) {
      return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 2 }}>
          <CircularProgress size={18} color="info" />
          <Typography variant="body2" color="text.secondary">
            Processing cell operation...
          </Typography>
        </Box>
      );
    }
    if (content.includes('[Executing cell operation...]')) {
      return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 2 }}>
          <CircularProgress size={18} color="primary" />
          <Typography variant="body2" color="text.secondary">
            Executing cell operation...
          </Typography>
        </Box>
      );
    }
    if (content.includes('[Cell operation executed]')) {
      return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 2 }}>
          <Typography variant="body2" color="success.main">
            Cell operation executed.
          </Typography>
        </Box>
      );
    }
    return null;
  };

  const cleanedContent = content;

  const renderCodeBlockFromMarkdown = (code: string) => {
    let cleanCode = code;
    // const langMatch = code.match(/^```(\w+)\n?/);

    if (cleanCode.startsWith('```')) {
      cleanCode = cleanCode.replace(/^```(\w+)?\n?/, '');
    }
    if (cleanCode.endsWith('```')) {
      cleanCode = cleanCode.replace(/```$/, '');
    }
    cleanCode = cleanCode.trim();

    if (!cleanCode) {
      return null;
    }

    return (
      <Box
        sx={{
          position: 'relative',
          my: 1,
          backgroundColor: 'action.hover',
          borderRadius: 1,
          overflow: 'hidden'
        }}
      >
        <pre style={{ margin: 0, position: 'relative' }}>
          <code
            style={{
              display: 'block',
              padding: '12px',
              fontSize: '15px',
              lineHeight: '1.6',
              fontFamily: '"Fira Code", "Consolas", monospace',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }}
          >
            {cleanCode}
          </code>
        </pre>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            alignItems: 'center',
            gap: 1,
            p: 1,
            borderTop: '1px solid',
            borderColor: 'divider',
            backgroundColor: 'background.paper'
          }}
        >
          <IconButton
            size="small"
            onClick={() => onCopyCode?.(cleanCode)}
            title="Copy code"
          >
            <ContentCopyIcon fontSize="small" />
          </IconButton>
          {onExecuteCode && (
            <IconButton
              size="small"
              onClick={() => onExecuteCode(cleanCode)}
              title="Execute code in new cell"
            >
              <PlayArrowIcon fontSize="small" />
            </IconButton>
          )}
          {referencedCells.size > 0 && onModifyCell && (
            <Box sx={{ display: 'flex', gap: 1 }}>
              {Array.from(referencedCells).map(cellNumber => (
                <IconButton
                  key={cellNumber}
                  size="small"
                  onClick={() => onModifyCell(cleanCode, cellNumber - 1)}
                  title={`Modify cell ${cellNumber}`}
                  sx={{
                    bgcolor: 'background.paper',
                    '&:hover': { bgcolor: 'grey.100' },
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                    position: 'relative'
                  }}
                >
                  <EditIcon fontSize="small" />
                  <Typography
                    component="span"
                    sx={{
                      position: 'absolute',
                      top: -8,
                      right: -8,
                      fontSize: '0.75rem',
                      bgcolor: 'primary.main',
                      color: 'white',
                      width: 16,
                      height: 16,
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      lineHeight: '16px'
                    }}
                  >
                    {cellNumber}
                  </Typography>
                </IconButton>
              ))}
            </Box>
          )}
        </Box>
      </Box>
    );
  };

  const markdownComponents: Components = {
    code(props) {
      const { children, className, node, ...rest } = props;
      const match = /language-(\w+)/.exec(className || '');
      const isInline = !match && !className?.startsWith('language-');

      if (hasOperationWithCode && !isInline) {
        return null;
      }

      if (isInline) {
        return (
          <code
            {...rest}
            style={{
              backgroundColor: 'var(--jp-layout-color2, rgba(0,0,0,0.1))',
              padding: '0.2em 0.4em',
              margin: 0,
              fontSize: '85%',
              borderRadius: '3px',
              fontFamily: 'monospace'
            }}
          >
            {children}
          </code>
        );
      }

      return renderCodeBlockFromMarkdown(String(children).trim());
    },
    p(props) {
      const content = React.Children.toArray(props.children)
        .map(child => (typeof child === 'string' ? child : ''))
        .join('');
      if (content.trim() === '') {
        return null;
      }
      return (
        <Typography variant="body1" component="p" sx={{ mb: 1 }}>
          {props.children}
        </Typography>
      );
    },
    ul(props) {
      return (
        <Typography component="ul" sx={{ pl: 2, mb: 1 }}>
          {props.children}
        </Typography>
      );
    },
    ol(props) {
      return (
        <Typography component="ol" sx={{ pl: 2, mb: 1 }}>
          {props.children}
        </Typography>
      );
    },
    li(props) {
      return (
        <Typography component="li" sx={{ mb: 0.5 }}>
          {props.children}
        </Typography>
      );
    },
    pre({ children }) {
      const codeChild = React.Children.toArray(children).find(
        (child: any) => child?.type === 'code'
      );
      return codeChild ? <>{codeChild}</> : <pre>{children}</pre>;
    }
  };

  const renderIndividualOperation = (op: CellOperation, index: number) => {
    const cellDisplayIndex =
      typeof op.cell_index === 'number' ? op.cell_index + 1 : 'N/A';
    let title = '';
    let codeContent = op.code || '';

    switch (op.type) {
      case 'create_cell':
        title = `Create Cell (at index ${cellDisplayIndex})`;
        break;
      case 'update_cell':
        title = `Update Cell ${cellDisplayIndex}`;
        break;
      case 'delete_cell':
        title = `Delete Cell ${cellDisplayIndex}`;
        codeContent = `# Deleting cell ${cellDisplayIndex}`;
        break;
      default:
        title = `Unknown Operation on Cell ${cellDisplayIndex}`;
    }

    if (!codeContent.trim() && op.type !== 'delete_cell') {
      return null;
    }

    return (
      <Box
        key={`op-${index}`}
        sx={{
          my: 2,
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1,
          overflow: 'hidden',
          backgroundColor: 'action.hover'
        }}
      >
        <Typography
          variant="caption"
          sx={{
            display: 'block',
            p: 1,
            backgroundColor: 'background.paper',
            borderBottom: '1px solid',
            borderColor: 'divider',
            fontWeight: 'bold'
          }}
        >
          {title}
        </Typography>
        <pre style={{ margin: 0, position: 'relative' }}>
          <code
            style={{
              display: 'block',
              padding: '12px',
              fontSize: '15px',
              lineHeight: '1.6',
              fontFamily: '"Fira Code", "Consolas", monospace',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }}
          >
            {codeContent}
          </code>
        </pre>
        {role === 'assistant' && canRevertFlags[index] && (
          <Box
            sx={{
              p: 1,
              borderTop: '1px solid',
              borderColor: 'divider',
              textAlign: 'right'
            }}
          >
            <Button
              size="small"
              variant="outlined"
              color="secondary"
              onClick={() => handleRevertClick(op, index)}
              startIcon={<ReplayIcon />}
              disabled={
                revertStates[index] === 'checking' ||
                revertStates[index] === 'reverting' ||
                revertStates[index] === 'disabled'
              }
            >
              {revertStates[index] === 'reverting' ? 'Reverting...' : 'Revert'}
            </Button>
          </Box>
        )}
      </Box>
    );
  };

  const renderOperationBlocks = () => {
    if (!operations || operations.length === 0) {
      return null;
    }
    return operations.map(renderIndividualOperation);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
        gap: 1
      }}
    >
      <Box
        sx={{
          maxWidth: '85%',
          bgcolor: isUser ? 'primary.main' : 'background.paper',
          color: isUser ? 'primary.contrastText' : 'text.primary',
          borderRadius: 2,
          p: 2,
          boxShadow: theme =>
            `0 1px 2px ${theme.palette.mode === 'dark' ? 'rgba(0,0,0,0.4)' : 'rgba(0,0,0,0.1)'}`
        }}
      >
        {role === 'assistant' ? (
          <>
            {renderSpecialState()}
            <Box
              sx={{
                '& pre': {
                  position: 'relative',
                  bgcolor: theme =>
                    theme.palette.mode === 'dark' ? '#1E1E1E' : '#f5f5f5',
                  borderRadius: 1,
                  p: 2,
                  my: 2,
                  overflow: 'auto',
                  boxShadow: theme =>
                    `inset 0 0 8px ${theme.palette.mode === 'dark' ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.1)'}`,
                  border: theme =>
                    `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`
                },
                '& code': {
                  fontSize: '0.9rem',
                  fontFamily: '"Fira Code", "Consolas", monospace',
                  color: theme =>
                    theme.palette.mode === 'dark' ? '#D4D4D4' : '#333333',
                  lineHeight: '1.5'
                },
                '& p': {
                  m: 0,
                  color: 'text.primary',
                  '&:not(:last-child)': {
                    mb: 1.5
                  }
                },
                '& p > code': {
                  bgcolor: theme =>
                    theme.palette.mode === 'dark'
                      ? 'rgba(255,255,255,0.1)'
                      : 'rgba(0,0,0,0.1)',
                  color: 'text.primary',
                  px: 1,
                  py: 0.5,
                  borderRadius: 1,
                  fontFamily: '"Fira Code", "Consolas", monospace'
                }
              }}
            >
              <ReactMarkdown components={markdownComponents}>
                {cleanedContent}
              </ReactMarkdown>
              {renderOperationBlocks()}
            </Box>
          </>
        ) : (
          <Typography>{cleanedContent}</Typography>
        )}
      </Box>
    </Box>
  );
}
