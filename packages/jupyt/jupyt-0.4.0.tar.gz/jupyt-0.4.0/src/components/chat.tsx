import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Box, Button } from '@mui/material';
import {
  DEFAULT_MODEL_CONFIG,
  getModelConfig,
  saveModelConfig
} from '../config';
import { StreamChunk, QueryType, CellOperation } from '../types/stream';
import { ChatMessage } from './chat-message';
import { ChatInput } from './chat-input';
import { ChatHeader } from './chat-header';
import { CellService } from '../services/cell-service';
import { IMessage, IModelConfig } from '../types/api';
import { IChatProps } from '../types/chat';
import {
  extractCellReferences,
  removeCellOperationTags
} from '../utils/chatUtils';
import { useNotebookOperations } from '../hooks/use-notebook-operations';
import { showNotification } from '../hooks/use-show-notification';
import { useAgenticLoopManager } from '../hooks/use-agentic-loop-manager';
import {
  streamAgenticAssistant,
  IAgenticAssistantPayload
} from '../services/api-service';
import { extractNotebookState } from '../utils/notebook-state-extractor';
import { useAgenticState } from '../hooks/use-agentic-state';
import { extractTextOutputFromCell } from '../utils/cellOutputExtractor';
import {
  JupytPendingOperation,
  PENDING_OPERATION_METADATA_KEY
} from '../types/cell-metadata';
import {
  JupytApprovedOperation,
  APPROVED_OPERATION_METADATA_KEY
} from '../types/cell-metadata';
import { CodeCell, CodeCellModel } from '@jupyterlab/cells';
import {
  injectOrUpdateCellUI,
  handleApprove,
  handleReject
} from '../plugins/cell-toolbar';
import DoneAllIcon from '@mui/icons-material/DoneAll';
import ClearAllIcon from '@mui/icons-material/ClearAll';

export function Chat({
  notebookPanel,
  sessionContext
}: IChatProps): JSX.Element {
  // Chat state
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentType] = useState<QueryType | null>(null);
  const [sessionId, setSessionId] = useState(() => generateSessionId());
  const [hasPendingOperations, setHasPendingOperations] = useState(false);

  // Model configuration state
  const [modelConfig, setModelConfig] =
    useState<IModelConfig>(getModelConfig());

  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const cellServiceRef = useRef<CellService>(CellService.getInstance());

  // Helper function to generate a random session ID
  function generateSessionId(): string {
    return `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  const scrollToBottom = useCallback(() => {
    if (messagesEndRef.current) {
      const container = messagesEndRef.current.parentElement;
      if (container) {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: 'smooth'
        });
      }
    }
  }, []);

  // Handle model configuration change
  const handleModelConfigChange = useCallback(
    (config: IModelConfig) => {
      setModelConfig(config);
      saveModelConfig(config);
      showNotification(
        `Model updated to ${config.provider} - ${config.model}`,
        'success'
      );
    },
    [showNotification]
  );

  useEffect(() => {
    if (notebookPanel) {
      cellServiceRef.current.setNotebookPanel(notebookPanel);
    }
  }, [notebookPanel]);

  const {
    copyToNotebook,
    modifyCell,
    handleAddCell,
    handleDeleteCell,
    handleRevertOperation
  } = useNotebookOperations({
    notebookPanel,
    sessionContext,
    showNotification
  });

  // Cell operation executor for agentic loop
  const executeCellOperation = async (
    op: CellOperation
  ): Promise<string | undefined> => {
    try {
      if (
        op.type === 'create_cell' &&
        op.code !== undefined &&
        op.cell_index !== undefined
      ) {
        await handleAddCell(op.code, op.cell_index, !!op.run_needed);
        return undefined;
      } else if (
        op.type === 'update_cell' &&
        op.code !== undefined &&
        op.cell_index !== undefined
      ) {
        await modifyCell(op.code, op.cell_index, !!op.run_needed);
        return undefined;
      } else if (op.type === 'delete_cell' && op.cell_index !== undefined) {
        await handleDeleteCell(op.cell_index);
        return undefined;
      }
    } catch (err) {
      showNotification(
        `Cell operation failed: ${err instanceof Error ? err.message : 'Unknown error'}`,
        'error'
      );
      return `Error: ${err instanceof Error ? err.message : 'Unknown error'}`;
    }
    return undefined;
  };

  // Agentic state
  const { plan, setPlan, planStage, setPlanStage, cellOutput, setCellOutput } =
    useAgenticState();

  // Agentic loop manager
  const { startAgenticLoop, cancelAgenticLoop, isLooping, revertAllChanges } =
    useAgenticLoopManager({
      plan,
      setPlan,
      planStage,
      setPlanStage,
      cellOutput,
      setCellOutput,
      notebookPanel,
      sessionId,
      setMessages,
      onStreamingStateChange: setIsStreaming,
      executeCellOperation,
      extractTextOutputFromCell
    });

  // Conditional rendering for Revert All Changes button
  const shouldShowRevertButton = isLooping || !!plan;

  // Function to handle starting a new chat with a fresh session ID
  const handleNewChat = useCallback(() => {
    if (isStreaming || isLooping) {
      return; // Prevent starting new chat while streaming
    }

    // Reset states
    setMessages([]);
    setInput('');
    setSessionId(generateSessionId());

    // Reset agentic state if needed
    setPlan('');
    setPlanStage('');
    setCellOutput('');

    // Show notification
    showNotification('Started new chat session', 'success');

    // Scroll to bottom
    setTimeout(() => scrollToBottom(), 100);
  }, [
    isStreaming,
    isLooping,
    setPlan,
    setPlanStage,
    setCellOutput,
    showNotification,
    scrollToBottom
  ]);

  // Helper function to clean message content
  const cleanMessageContent = (content: string): string => {
    // Correct the regex: Use single backslashes for bracket escaping in a regex literal
    const cleanedOfStatus = content
      .replace(/\n?\[COMPLETION_STATUS:[^\]]*\]/gi, '')
      .trim();
    // Remove cell operation tags separately
    return removeCellOperationTags(cleanedOfStatus);
  };

  useEffect(() => {
    if (notebookPanel) {
      cellServiceRef.current.setNotebookPanel(notebookPanel);
    }
  }, [notebookPanel]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming || !notebookPanel) {
      return;
    }
    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [
      ...prev,
      {
        role: 'user',
        content: userMessage,
        timestamp: Date.now()
      }
    ]);
    setIsStreaming(true);

    const notebookState = extractNotebookState(notebookPanel);
    const includeSearch = userMessage.includes('@search');
    const payload: IAgenticAssistantPayload = {
      query: userMessage,
      session_id: sessionId,
      notebook_state: notebookState,
      llm_config: modelConfig
    };

    if (includeSearch) {
      payload.search = true;
    }

    let assistantMsgIndex = -1;
    setMessages(prev => {
      assistantMsgIndex = prev.length;
      return [
        ...prev,
        {
          role: 'assistant',
          content: '',
          timestamp: Date.now()
        }
      ];
    });
    scrollToBottom();

    let lastChunk: StreamChunk | undefined = undefined;
    let fullContent = '';
    let initialCellOutput: string | null = null;
    try {
      for await (const chunk of streamAgenticAssistant(payload)) {
        lastChunk = chunk;
        if (chunk.chunk_type !== 'end' && chunk.content) {
          if (chunk.content.length > 0) {
            fullContent += chunk.content;
            setMessages(prev => {
              // Update only the last assistant message
              const updated = [...prev];
              if (updated.length > 0 && updated[assistantMsgIndex]) {
                updated[assistantMsgIndex] = {
                  ...updated[assistantMsgIndex],
                  // Clean the content as it streams
                  content: cleanMessageContent(fullContent)
                };
              }
              return updated;
            });
          }
        }
      }
    } catch (err) {
      setMessages(prev => {
        const updated = [...prev];
        if (updated.length > 0 && updated[assistantMsgIndex]) {
          updated[assistantMsgIndex] = {
            ...updated[assistantMsgIndex],
            content: `Error: ${err instanceof Error ? err.message : 'Unknown error'}`
          };
        } else {
          // Add new error message if placeholder wasn't added correctly
          updated.push({
            role: 'assistant',
            content: `Error: ${err instanceof Error ? err.message : 'Unknown error'}`,
            timestamp: Date.now()
          });
        }
        return updated;
      });
      setIsStreaming(false);
      return;
    }
    setIsStreaming(false);

    // Clean the final message content *before* potentially adding operations
    setMessages(prev => {
      const updated = [...prev];
      const lastMessageIndex = assistantMsgIndex; // Use the saved index

      if (lastMessageIndex >= 0 && updated[lastMessageIndex]) {
        updated[lastMessageIndex] = {
          ...updated[lastMessageIndex],
          content: cleanMessageContent(fullContent) // Clean the content here
        };
      }
      return updated;
    });

    // If agentic, execute all next_actions before entering the agentic loop
    let lastExecutedOperationIndex = -1;
    if (
      lastChunk &&
      lastChunk.next_action &&
      lastChunk.next_action.length > 0 &&
      lastChunk.completion_status === 'continue'
    ) {
      for (let i = 0; i < lastChunk.next_action.length; i++) {
        const op = lastChunk.next_action[i];
        await executeCellOperation(op);
        if (op.run_needed && typeof op.cell_index === 'number') {
          lastExecutedOperationIndex = i; // Keep track of the last op that needs output checking
        }
      }

      // If the last executed operation needed running, wait for its output
      if (lastExecutedOperationIndex !== -1) {
        const op = lastChunk.next_action[lastExecutedOperationIndex];
        await new Promise(resolve => setTimeout(resolve, 100)); // Small delay
        await (async function waitForCellOutput() {
          const pos = typeof op.cell_index === 'number' ? op.cell_index : 0;
          const cell = notebookPanel?.content?.widgets?.[pos];
          if (!cell) {
            return;
          }
          const hasOutputs = (model: any): boolean => {
            return (
              model &&
              typeof model === 'object' &&
              'outputs' in model &&
              model.outputs
            );
          };
          if (hasOutputs(cell.model)) {
            let resolved = false;
            const checkOutput = () => {
              if (hasOutputs(cell.model)) {
                const output = extractTextOutputFromCell(cell.model as any);
                if (output && output.length > 0) {
                  resolved = true;
                  initialCellOutput = output;
                }
              }
            };
            const outputChanged = () => {
              if (!resolved) {
                checkOutput();
              }
            };
            (cell.model as any).outputs.changed.connect(outputChanged);
            checkOutput();
            setTimeout(() => {
              if (!resolved) {
                resolved = true;
                (cell.model as any).outputs.changed.disconnect(outputChanged);
                initialCellOutput = extractTextOutputFromCell(
                  cell.model as any
                );
              }
            }, 10000); // 10-second timeout
          }
        })();
      }
    }

    // If agentic, enter the agentic loop
    if (lastChunk && lastChunk.completion_status === 'continue') {
      setCellOutput(initialCellOutput); // Set the initial cell output for the agentic loop
      await startAgenticLoop({
        query: userMessage,
        llmConfig: DEFAULT_MODEL_CONFIG
      });
    } else if (lastChunk && lastChunk.chunk_type === 'end') {
      const operations = lastChunk.next_action;
      if (operations && operations.length > 0) {
        const notebook = notebookPanel.content;
        const model = notebookPanel.model;

        if (!model) {
          showNotification('Error: Notebook model not available.', 'error');
          return;
        }

        for (const op of operations) {
          const pendingMetadata: JupytPendingOperation = {
            type: op.type,
            code: op.code,
            runNeeded: op.run_needed
          };

          try {
            if (
              op.type === 'create_cell' &&
              op.cell_index !== undefined &&
              op.code !== undefined
            ) {
              // Insert a placeholder cell FIRST
              model.sharedModel.insertCell(op.cell_index, {
                cell_type: 'code',
                source: ''
              }); // Insert empty initially
              const cellWidget = notebook.widgets[op.cell_index];
              if (cellWidget) {
                // Now set the metadata on the newly created cell
                pendingMetadata.originalIndex = op.cell_index;
                cellWidget.model.sharedModel.setMetadata(
                  PENDING_OPERATION_METADATA_KEY,
                  pendingMetadata as any
                ); // Cast to any

                // Delay UI injection and selection slightly to allow DOM rendering
                setTimeout(() => {
                  // Add checks for safety and type narrowing
                  if (
                    cellWidget.isAttached &&
                    cellWidget.node &&
                    op.cell_index !== undefined
                  ) {
                    injectOrUpdateCellUI(cellWidget as CodeCell, notebookPanel);
                    // Select the newly created cell to ensure UI updates
                    notebook.activeCellIndex = op.cell_index; // Now type-safe
                    notebook.scrollToCell(cellWidget);
                  } else {
                    console.warn(
                      `Cell widget at index ${op.cell_index ?? 'unknown'} not ready after delay for UI injection.`
                    );
                  }
                }, 0);
              } else {
                console.error(
                  `Failed to get cell widget after creation at index ${op.cell_index}`
                );
                showNotification(
                  `Error preparing cell creation at index ${op.cell_index + 1}.`,
                  'error'
                );
              }
            } else if (
              op.type === 'update_cell' &&
              op.cell_index !== undefined &&
              op.code !== undefined
            ) {
              const cellWidget = notebook.widgets[op.cell_index];
              if (cellWidget) {
                const oldCode = cellWidget.model.sharedModel.source;
                pendingMetadata.oldCode = oldCode; // Store old code for diff
                pendingMetadata.originalIndex = op.cell_index;
                cellWidget.model.sharedModel.setMetadata(
                  PENDING_OPERATION_METADATA_KEY,
                  pendingMetadata as any
                ); // Cast to any
                injectOrUpdateCellUI(cellWidget as CodeCell, notebookPanel);
              } else {
                showNotification(
                  `Error: Could not find cell ${op.cell_index + 1} to update.`,
                  'error'
                );
              }
            } else if (
              op.type === 'delete_cell' &&
              op.cell_index !== undefined
            ) {
              const cellWidget = notebook.widgets[op.cell_index];
              if (cellWidget) {
                pendingMetadata.originalIndex = op.cell_index;
                // For delete, just mark the cell for deletion via metadata
                cellWidget.model.sharedModel.setMetadata(
                  PENDING_OPERATION_METADATA_KEY,
                  pendingMetadata as any
                ); // Cast to any
                injectOrUpdateCellUI(cellWidget as CodeCell, notebookPanel);
              } else {
                showNotification(
                  `Error: Could not find cell ${op.cell_index + 1} to delete.`,
                  'error'
                );
              }
            }
          } catch (metaError) {
            console.error('Error setting metadata:', metaError);
            showNotification(
              `Failed to set metadata for operation on cell ${op.cell_index !== undefined ? op.cell_index + 1 : 'N/A'}.`,
              'error'
            );
          }
        }
        // Optionally, update the assistant message to indicate actions are pending cell approval
        setMessages(prev => {
          const updated = [...prev];
          // Ensure assistantMsgIndex is valid and the message exists
          if (
            assistantMsgIndex >= 0 &&
            assistantMsgIndex < updated.length &&
            updated[assistantMsgIndex]
          ) {
            const currentContent = updated[assistantMsgIndex].content;
            updated[assistantMsgIndex] = {
              ...updated[assistantMsgIndex],
              content:
                currentContent +
                '\n\n*Code modifications suggested. Please approve or reject them in the notebook cells.*',
              operations: operations // <-- Add the operations array here
            };
          } else {
            console.warn(
              'Could not find assistant message to attach operations to. Index:',
              assistantMsgIndex
            );
            // Optionally handle this case, maybe add a new message?
          }
          return updated;
        });
      }
    }
  };

  // --- NEW: Function to check if a specific operation can be reverted ---
  const checkCanRevert = useCallback(
    async (operation: CellOperation): Promise<boolean> => {
      if (!notebookPanel || typeof operation.cell_index !== 'number') {
        return false;
      }
      const notebook = notebookPanel.content;
      // For creates/updates, check the cell at the original index
      const cellWidget = notebook.widgets[operation.cell_index];
      if (cellWidget instanceof CodeCell && cellWidget.model) {
        const approvedMetadata = cellWidget.model.sharedModel.getMetadata(
          APPROVED_OPERATION_METADATA_KEY
        ) as JupytApprovedOperation | undefined;
        // Can revert if approved metadata exists for this operation type
        return !!approvedMetadata && approvedMetadata.type === operation.type;
      }
      return false;
    },
    [notebookPanel]
  );

  // --- NEW: Handler passed to ChatMessage to trigger revert ---
  const handleRevertRequest = useCallback(
    async (operation: CellOperation, cell: CodeCell) => {
      if (!cell.model) {
        return;
      }
      const model = cell.model as CodeCellModel;
      const approvedMetadata = model.sharedModel.getMetadata(
        APPROVED_OPERATION_METADATA_KEY
      ) as JupytApprovedOperation | undefined;

      if (approvedMetadata && approvedMetadata.type === operation.type) {
        const success = await handleRevertOperation(cell, approvedMetadata);
        if (success) {
          // Clear the metadata AFTER successful revert
          model.sharedModel.deleteMetadata(APPROVED_OPERATION_METADATA_KEY);
          // Maybe add a confirmation message?
        } else {
          // handleRevertOperation already shows notification on failure
        }
      } else {
        showNotification(
          'Revert impossible: Cell state changed or metadata missing.',
          'error'
        );
      }
    },
    [handleRevertOperation, showNotification]
  );

  // Add function to check for pending operations
  const checkPendingOperations = useCallback(() => {
    if (!notebookPanel?.content) {
      return false;
    }
    const notebook = notebookPanel.content;
    for (const cell of notebook.widgets) {
      if (cell instanceof CodeCell && cell.model) {
        const pendingMetadata = cell.model.sharedModel.getMetadata(
          PENDING_OPERATION_METADATA_KEY
        );
        if (pendingMetadata) {
          return true;
        }
      }
    }
    return false;
  }, [notebookPanel]);

  // Update hasPendingOperations when notebook changes
  useEffect(() => {
    if (!notebookPanel) {
      return;
    }

    const updatePendingStatus = () => {
      setHasPendingOperations(checkPendingOperations());
    };

    // Initial check
    updatePendingStatus();

    // Use MutationObserver to watch for metadata changes
    const observer = new MutationObserver(() => {
      updatePendingStatus();
    });

    // Observe the notebook for changes
    observer.observe(notebookPanel.node, {
      attributes: true,
      childList: true,
      subtree: true
    });

    return () => {
      observer.disconnect();
    };
  }, [notebookPanel, checkPendingOperations]);

  // Function to handle approve all
  const handleApproveAll = useCallback(async () => {
    if (!notebookPanel?.content) {
      return;
    }
    const notebook = notebookPanel.content;

    // First, collect all cells with pending operations
    const pendingCells = notebook.widgets
      .map((cell, index) => ({ cell, index }))
      .filter(
        ({ cell }) =>
          cell instanceof CodeCell &&
          cell.model?.sharedModel.getMetadata(PENDING_OPERATION_METADATA_KEY)
      );

    // Sort delete operations to the end to handle them last
    pendingCells.sort((a, b) => {
      const aMetadata = (a.cell as CodeCell).model?.sharedModel.getMetadata(
        PENDING_OPERATION_METADATA_KEY
      ) as unknown as JupytPendingOperation;
      const bMetadata = (b.cell as CodeCell).model?.sharedModel.getMetadata(
        PENDING_OPERATION_METADATA_KEY
      ) as unknown as JupytPendingOperation;
      // Put delete operations at the end
      if (
        aMetadata.type === 'delete_cell' &&
        bMetadata.type !== 'delete_cell'
      ) {
        return 1;
      }
      if (
        bMetadata.type === 'delete_cell' &&
        aMetadata.type !== 'delete_cell'
      ) {
        return -1;
      }
      return 0;
    });

    // Process operations in order
    for (const { cell } of pendingCells) {
      if (cell instanceof CodeCell && cell.model) {
        const pendingMetadata = cell.model.sharedModel.getMetadata(
          PENDING_OPERATION_METADATA_KEY
        ) as JupytPendingOperation | undefined;
        if (pendingMetadata) {
          await handleApprove(cell as CodeCell, notebookPanel, pendingMetadata);
          // Add a small delay to allow the notebook to stabilize
          await new Promise(resolve => setTimeout(resolve, 100));
        }
      }
    }
    showNotification('All operations approved successfully', 'success');
  }, [notebookPanel, showNotification]);

  // Function to handle reject all
  const handleRejectAll = useCallback(async () => {
    if (!notebookPanel?.content) {
      return;
    }
    const notebook = notebookPanel.content;

    for (const cell of notebook.widgets) {
      if (cell instanceof CodeCell && cell.model) {
        const pendingMetadata = cell.model.sharedModel.getMetadata(
          PENDING_OPERATION_METADATA_KEY
        ) as JupytPendingOperation | undefined;
        if (pendingMetadata) {
          await handleReject(cell as CodeCell, notebookPanel, pendingMetadata);
        }
      }
    }
    showNotification('All operations rejected', 'success');
  }, [notebookPanel, showNotification]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  useEffect(() => {
    if (isStreaming) {
      scrollToBottom();
    }
  }, [isStreaming, scrollToBottom]);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        bgcolor: 'background.default',
        zIndex: 1000
      }}
    >
      <Box
        sx={{
          position: 'sticky',
          top: 0,
          zIndex: 1001,
          bgcolor: 'background.default',
          borderBottom: '1px solid',
          borderColor: 'divider',
          p: 2
        }}
      >
        <ChatHeader
          isStreaming={isStreaming}
          currentType={currentType}
          onNewChat={handleNewChat}
          onModelConfigChange={handleModelConfigChange}
        />
      </Box>

      <Box
        sx={{
          flex: 1,
          overflow: 'auto',
          px: 3,
          py: 2
        }}
      >
        {messages.map((message, index) => {
          const { cellNumbers } = extractCellReferences(
            message.role === 'user'
              ? message.content
              : messages[index - 1]?.content || ''
          );

          return (
            <ChatMessage
              key={index}
              role={message.role}
              content={message.content}
              onCopyCode={copyToNotebook}
              onExecuteCode={code => copyToNotebook(code, true)}
              onModifyCell={modifyCell}
              onAddCell={handleAddCell}
              onDeleteCell={handleDeleteCell}
              referencedCells={cellNumbers}
              operations={message.operations}
              showNotification={showNotification}
              onRevertOperation={handleRevertRequest}
              canRevertOperation={checkCanRevert}
              notebookPanel={notebookPanel}
            />
          );
        })}
        <div ref={messagesEndRef} />
      </Box>
      {shouldShowRevertButton && (
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
          <Button
            variant="outlined"
            color="warning"
            onClick={async () => {
              await revertAllChanges();
            }}
          >
            Revert All Changes
          </Button>
        </Box>
      )}
      {hasPendingOperations && (
        <Box
          sx={{
            position: 'fixed',
            bottom: 16,
            right: 16,
            display: 'flex',
            gap: 1,
            zIndex: 1002,
            bgcolor: 'background.paper',
            borderRadius: 1,
            boxShadow: 2,
            p: 1
          }}
        >
          <Button
            size="small"
            variant="contained"
            color="primary"
            onClick={handleApproveAll}
            startIcon={<DoneAllIcon />}
          >
            Approve All
          </Button>
          <Button
            size="small"
            variant="outlined"
            color="error"
            onClick={handleRejectAll}
            startIcon={<ClearAllIcon />}
          >
            Reject All
          </Button>
        </Box>
      )}
      <Box
        sx={{
          p: 3,
          borderTop: '1px solid',
          borderColor: 'divider',
          bgcolor: 'background.default'
        }}
      >
        <ChatInput
          value={input}
          isStreaming={isStreaming || isLooping}
          onChange={setInput}
          onSubmit={handleSubmit}
          isAgenticLooping={isLooping}
          onStopAgenticLoop={cancelAgenticLoop}
        />
      </Box>
    </Box>
  );
}
