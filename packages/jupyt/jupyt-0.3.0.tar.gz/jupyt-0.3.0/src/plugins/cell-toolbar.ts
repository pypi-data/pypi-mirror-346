import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import {
  INotebookTracker,
  NotebookPanel,
  NotebookActions
} from '@jupyterlab/notebook';
import { Cell, CodeCell, CodeCellModel } from '@jupyterlab/cells';
import { CellService } from '../services/cell-service';
import React from 'react';
import ReactDOM from 'react-dom';
import { CellApprovalControls } from '../components/cell-approval-controls';
import {
  JupytPendingOperation,
  JupytApprovedOperation,
  PENDING_OPERATION_METADATA_KEY,
  APPROVED_OPERATION_METADATA_KEY
} from '../types/cell-metadata';
import { showNotification } from '../hooks/use-show-notification';

const JUPYT_UI_CONTAINER_CLASS = 'jupyt-cell-ui-container';

/**
 * Injects or updates the Jupyt UI (Approval controls) in a cell based on metadata.
 */
export const injectOrUpdateCellUI = (cell: CodeCell, panel: NotebookPanel) => {
  if (
    !cell.model ||
    !(cell instanceof CodeCell) ||
    !cell.inputArea /* Check needed for typing */
  ) {
    return;
  }

  const model = cell.model as CodeCellModel;
  const pendingMetadata = model.sharedModel.getMetadata(
    PENDING_OPERATION_METADATA_KEY
  ) as JupytPendingOperation | undefined;

  // Find container within the main cell node
  let container = cell.node.querySelector(
    `:scope > .${JUPYT_UI_CONTAINER_CLASS}`
  ) as HTMLElement;

  // Clean up existing UI if no relevant metadata is found
  if (!pendingMetadata) {
    if (container) {
      ReactDOM.unmountComponentAtNode(container);
      container.remove();
    }
    return;
  }

  // Create container if it doesn't exist
  if (!container) {
    container = document.createElement('div');
    container.className = JUPYT_UI_CONTAINER_CLASS;
    // Add margin below the container
    container.style.marginTop = '10px';
    // Add left margin to align with cell content
    container.style.marginLeft = '70px'; // Estimated prompt width
    // Append to the main cell node (instead of prepending)
    cell.node.appendChild(container);
  }

  // Render the approval component if pending metadata exists
  ReactDOM.render(
    React.createElement(CellApprovalControls, {
      pendingOperation: pendingMetadata,
      onApprove: () => handleApprove(cell, panel, pendingMetadata),
      onReject: () => handleReject(cell, panel, pendingMetadata)
    }),
    container
  );
};

/**
 * Handles the approval of a pending operation.
 */
export const handleApprove = async (
  cell: CodeCell,
  panel: NotebookPanel,
  metadata: JupytPendingOperation
) => {
  if (!cell.model) {
    return;
  }
  const model = cell.model as CodeCellModel;

  // --- IMMEDIATE UI REMOVAL ---
  // Clear pending metadata *first* to trigger UI removal immediately
  try {
    model.sharedModel.deleteMetadata(PENDING_OPERATION_METADATA_KEY);
    injectOrUpdateCellUI(cell, panel);
  } catch (e) {
    console.error('Failed to clear pending metadata for UI removal:', e);
    // Continue with approval attempt anyway
  }
  // --- END IMMEDIATE UI REMOVAL ---

  const notebook = panel.content;
  const notebookModel = panel.model;

  if (!notebookModel) {
    showNotification('Notebook model not found. Cannot approve.', 'error');
    // Attempt to clear approved metadata if it was somehow set before failure
    try {
      model.sharedModel.deleteMetadata(APPROVED_OPERATION_METADATA_KEY);
    } catch {
      return;
    }
  }
  try {
    let approvedMetadata: JupytApprovedOperation | null = null;
    let cellIndexToRun: number | null = null;
    const runAfterDelete = false;

    switch (metadata.type) {
      case 'create_cell':
        if (metadata.code !== undefined) {
          model.sharedModel.setSource(metadata.code);
          approvedMetadata = {
            type: 'create_cell',
            previousCodeForCreate: '',
            runAfterApproval: metadata.runNeeded
          };
          const index = notebook.widgets.findIndex(w => w === cell);
          if (index !== -1 && metadata.runNeeded) {
            cellIndexToRun = index;
          }
          showNotification('Cell created successfully.', 'success');
        } else {
          throw new Error('Missing code for create operation.');
        }
        break;
      case 'update_cell':
        if (metadata.code !== undefined && metadata.oldCode !== undefined) {
          model.sharedModel.setSource(metadata.code);
          approvedMetadata = {
            type: 'update_cell',
            previousCode: metadata.oldCode,
            runAfterApproval: metadata.runNeeded
          };
          const index = notebook.widgets.findIndex(w => w === cell);
          if (index !== -1 && metadata.runNeeded) {
            cellIndexToRun = index;
          }
          showNotification('Cell updated successfully.', 'success');
        } else {
          throw new Error('Missing code or oldCode for update operation.');
        }
        break;
      case 'delete_cell':
        // eslint-disable-next-line no-case-declarations
        const indexToDelete = notebook.widgets.findIndex(w => w === cell);
        if (indexToDelete !== -1) {
          // Store the next cell index before deletion if we need to run it
          let nextCellIndex = null;
          if (
            metadata.runNeeded &&
            indexToDelete + 1 < notebook.widgets.length
          ) {
            nextCellIndex = indexToDelete + 1;
          }

          // Delete the cell
          if (notebookModel) {
            notebookModel.sharedModel.deleteCell(indexToDelete);
            showNotification('Cell deleted successfully.', 'success');

            // If we need to run the next cell after deletion
            if (
              nextCellIndex !== null &&
              panel.sessionContext.session?.kernel
            ) {
              notebook.activeCellIndex = nextCellIndex;
              await NotebookActions.run(notebook, panel.sessionContext);
            }
          } else {
            throw new Error('Could not find cell index to delete.');
          }
        }
        break;
      default:
        console.warn('Unsupported operation type for approval:', metadata.type);
        showNotification(`Unsupported operation: ${metadata.type}`, 'error');
        return;
    }

    // Set approved metadata *after* operation succeeds (if applicable)
    if (approvedMetadata) {
      // We already deleted pending, just set approved
      model.sharedModel.setMetadata(
        APPROVED_OPERATION_METADATA_KEY,
        approvedMetadata as any
      );
    }
    // For delete, the metadata is gone with the cell.

    // Run Cell if Needed
    if (cellIndexToRun !== null && panel.sessionContext.session?.kernel) {
      notebook.activeCellIndex = cellIndexToRun;
      await NotebookActions.run(notebook, panel.sessionContext);
    } else if (runAfterDelete) {
      console.log(
        'Run needed after delete - current implementation does not run.'
      );
    }
  } catch (error) {
    console.error('Error approving operation:', error);
    showNotification(
      `Failed to approve operation: ${error instanceof Error ? error.message : 'Unknown error'}`,
      'error'
    );
    // Pending metadata was already cleared. Ensure approved isn't set if it failed.
    try {
      model.sharedModel.deleteMetadata(APPROVED_OPERATION_METADATA_KEY);
    } catch {
      return;
    }
  }
};

/**
 * Handles the rejection of a pending operation.
 */
export const handleReject = (
  cell: CodeCell,
  panel: NotebookPanel,
  metadata: JupytPendingOperation
) => {
  if (!cell.model) {
    return;
  }
  const model = cell.model as CodeCellModel;

  // --- IMMEDIATE UI REMOVAL ---
  // Clear pending metadata *first* to trigger UI removal immediately
  try {
    model.sharedModel.deleteMetadata(PENDING_OPERATION_METADATA_KEY);
    injectOrUpdateCellUI(cell, panel);
  } catch (e) {
    console.error('Failed to clear pending metadata for UI removal:', e);
    // Continue with rejection attempt anyway
  }
  // --- END IMMEDIATE UI REMOVAL ---

  const notebook = panel.content;
  const notebookModel = panel.model;

  if (!notebookModel) {
    showNotification('Notebook model not found. Cannot reject.', 'error');
    return;
  }
  try {
    switch (metadata.type) {
      case 'create_cell':
        // eslint-disable-next-line no-case-declarations
        const indexToDelete = notebook.widgets.findIndex(w => w === cell);
        if (indexToDelete !== -1) {
          notebookModel.sharedModel.deleteCell(indexToDelete);
          showNotification(
            'Cell creation rejected and placeholder removed.',
            'success'
          );
        } else {
          throw new Error(
            'Could not find index for rejected placeholder cell.'
          );
        }
        return; // Exit after deletion
      case 'update_cell':
        showNotification('Cell update rejected.', 'success');
        break; // Metadata already cleared
      case 'delete_cell':
        showNotification('Cell deletion rejected.', 'success');
        break; // Metadata already cleared
      default:
        console.warn(
          'Unsupported operation type for rejection:',
          metadata.type
        );
        showNotification(
          `Cannot reject unsupported operation: ${metadata.type}`,
          'error'
        );
        return;
    }
    // Metadata was cleared at the start
  } catch (error) {
    console.error('Error rejecting operation:', error);
    showNotification(
      `Failed to reject operation: ${error instanceof Error ? error.message : 'Unknown error'}`,
      'error'
    );
    // Metadata was already attempted to be cleared
  }
};

// --- Plugin Definition ---

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyt:cell-toolbar',
  autoStart: true,
  requires: [INotebookTracker],
  activate: (app: JupyterFrontEnd, notebooks: INotebookTracker) => {
    const cellService = CellService.getInstance();

    notebooks.widgetAdded.connect((sender, panel: NotebookPanel) => {
      const addAIButton = (cell: Cell) => {
        // Find the JupyterLab toolbar
        const jupyterToolbar = cell.node.querySelector('.jp-Toolbar');
        if (!jupyterToolbar) {
          return;
        }

        // Remove any existing AI buttons to prevent duplicates
        const existingButtons =
          jupyterToolbar.querySelectorAll('.jupyt-ai-button');
        existingButtons.forEach(button => button.remove());

        // Add cell number label
        let cellNumberLabel =
          jupyterToolbar.querySelector('.jupyt-cell-number');
        if (!cellNumberLabel) {
          cellNumberLabel = document.createElement('div');
          cellNumberLabel.className = 'jupyt-cell-number';
          (cellNumberLabel as HTMLElement).style.marginLeft = 'auto'; // Push to the right
          (cellNumberLabel as HTMLElement).style.marginRight = '8px';
          (cellNumberLabel as HTMLElement).style.fontSize = '12px';
          (cellNumberLabel as HTMLElement).style.color =
            'var(--jp-ui-font-color2)';
          (cellNumberLabel as HTMLElement).style.fontFamily =
            'var(--jp-ui-font-family)';
          jupyterToolbar.appendChild(cellNumberLabel);
        }

        // Get cell index and update the label
        const notebook = panel.content;
        const cellIndex = notebook.widgets.findIndex(c => c === cell);
        if (cellNumberLabel) {
          cellNumberLabel.textContent = `Cell [${cellIndex + 1}]`;
        }

        const button = document.createElement('button');
        button.className = 'jp-Button jp-ToolbarButton jupyt-ai-button';
        button.title = 'Use Jupyt Assistant for this cell';
        button.innerHTML = `
          <span class="jp-ToolbarButton-icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 0C3.6 0 0 3.6 0 8C0 12.4 3.6 16 8 16C12.4 16 16 12.4 16 8C16 3.6 12.4 0 8 0ZM8 14C4.7 14 2 11.3 2 8C2 4.7 4.7 2 8 2C11.3 2 14 4.7 14 8C14 11.3 11.3 14 8 14Z" fill="currentColor"/>
              <path d="M8 4C6.3 4 5 5.3 5 7C5 8.7 6.3 10 8 10C9.7 10 11 8.7 11 7C11 5.3 9.7 4 8 4ZM8 8C7.4 8 7 7.6 7 7C7 6.4 7.4 6 8 6C8.6 6 9 6.4 9 7C9 7.6 8.6 8 8 8Z" fill="currentColor"/>
            </svg>
          </span>
          <span class="jp-ToolbarButton-label">AI</span>
        `;

        button.onclick = () => {
          cellService.selectCell(cell);
        };

        // Find the move up button (which is typically the first button)
        const moveUpButton = jupyterToolbar.querySelector(
          '.jp-Button[data-command="notebook:move-cell-up"]'
        );

        if (moveUpButton) {
          // Insert after the move up button
          moveUpButton.insertAdjacentElement('afterend', button);
        } else {
          // Fallback: insert at the beginning of the toolbar
          const firstButton = jupyterToolbar.querySelector('.jp-Button');
          if (firstButton) {
            firstButton.insertAdjacentElement('beforebegin', button);
          } else {
            jupyterToolbar.insertBefore(button, jupyterToolbar.firstChild);
          }
        }
      };

      // Function to update all cell numbers
      const updateAllCellNumbers = () => {
        panel.content.widgets.forEach((cell, index) => {
          const toolbar = cell.node.querySelector('.jp-Toolbar');
          if (toolbar) {
            let numberLabel = toolbar.querySelector('.jupyt-cell-number');
            if (!numberLabel) {
              numberLabel = document.createElement('div');
              numberLabel.className = 'jupyt-cell-number';
              (numberLabel as HTMLElement).style.marginLeft = 'auto';
              (numberLabel as HTMLElement).style.marginRight = '8px';
              (numberLabel as HTMLElement).style.fontSize = '12px';
              (numberLabel as HTMLElement).style.color =
                'var(--jp-ui-font-color2)';
              (numberLabel as HTMLElement).style.fontFamily =
                'var(--jp-ui-font-family)';
              toolbar.appendChild(numberLabel);
            }
            numberLabel.textContent = `Cell [${index + 1}]`;
          }
        });
      };

      // --- NEW: Inject UI based on metadata for all cells ---
      const setupCellUIs = () => {
        panel.content.widgets.forEach(cell => {
          if (cell instanceof CodeCell) {
            injectOrUpdateCellUI(cell, panel);
          }
        });
      };

      // Listen for metadata changes on ANY cell in the model
      panel.model?.sharedModel.changed.connect((sharedModel, changes) => {
        if (changes.metadataChange) {
          // Add a minimal delay to allow DOM updates before checking/injecting UI
          setTimeout(() => {
            setupCellUIs();
          }, 50); // 50ms delay, adjust if needed
        }
      });

      // Listen for cell list changes (add/remove)
      panel.model?.cells.changed.connect(() => {
        // No timeout - run immediately (might cause flicker if DOM isn't ready, but let's try)
        updateAllCellNumbers();
        setupCellUIs();
        // Potential TODO: Check if a slight delay is needed here if UI doesn't appear reliably
      });

      // Initial setup for existing cells
      panel.revealed.then(() => {
        // Keep this delay - needed to ensure initial DOM is ready
        setTimeout(() => {
          panel.content.widgets.forEach(addAIButton);
          updateAllCellNumbers();
          setupCellUIs();
        }, 1000);
      });

      // Update AI button and UI on active cell change
      panel.content.activeCellChanged.connect((_, cell) => {
        if (cell) {
          // No timeout - run immediately
          addAIButton(cell);
          if (cell instanceof CodeCell) {
            injectOrUpdateCellUI(cell, panel);
          }
        }
      });
    });
  }
};

export default plugin;
