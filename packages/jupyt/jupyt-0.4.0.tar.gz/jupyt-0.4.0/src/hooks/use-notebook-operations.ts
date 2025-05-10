import { NotebookActions, NotebookPanel } from '@jupyterlab/notebook';
import { CodeCell, CodeCellModel } from '@jupyterlab/cells';
import { IChatProps } from '../types/chat';
import { stripCodeBlockMarkers } from '../utils/chatUtils';
import { JupytApprovedOperation } from '../types/cell-metadata';

export function useNotebookOperations({
  notebookPanel,
  sessionContext,
  showNotification
}: {
  notebookPanel?: NotebookPanel;
  sessionContext?: IChatProps['sessionContext'];
  showNotification: (message: string, type: 'success' | 'error') => void;
}) {
  // Copy code to a new cell and optionally execute
  const copyToNotebook = async (
    code: string,
    shouldExecute = false
  ): Promise<void> => {
    if (!notebookPanel?.model || !sessionContext) {
      showNotification(
        'No notebook is open. Please open a notebook first.',
        'error'
      );
      return;
    }
    try {
      const notebook = notebookPanel.content;
      const model = notebookPanel.model;
      if (!model || !notebook || !notebook.model) {
        showNotification('Error: Could not access notebook content.', 'error');
        return;
      }
      const activeCellIndex = notebook.activeCellIndex;
      const newCellIndex = activeCellIndex + 1;
      model.sharedModel.insertCell(newCellIndex, {
        cell_type: 'code',
        source: stripCodeBlockMarkers(code),
        metadata: {},
        outputs: []
      });
      notebook.activeCellIndex = newCellIndex;
      if (shouldExecute) {
        await sessionContext.ready;
        await NotebookActions.run(notebook, sessionContext);
      }
      const activeCell = notebook.activeCell;
      if (activeCell) {
        notebook.scrollToCell(activeCell);
      }
      showNotification(
        shouldExecute
          ? 'Code executed in notebook.'
          : 'Code copied to notebook.',
        'success'
      );
    } catch (error) {
      showNotification(
        `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'error'
      );
    }
  };

  // Modify an existing cell
  const modifyCell = async (
    code: string,
    cell_index: number,
    run_needed?: boolean
  ): Promise<void> => {
    if (!notebookPanel?.model) {
      showNotification(
        'No notebook is open. Please open a notebook first.',
        'error'
      );
      return;
    }
    try {
      const notebook = notebookPanel.content;
      if (cell_index < 0 || cell_index >= notebook.widgets.length) {
        showNotification(`Invalid cell index ${cell_index + 1}`, 'error');
        return;
      }
      const cell = notebook.widgets[cell_index];
      const cleanCode = stripCodeBlockMarkers(code);
      cell.model.sharedModel.setSource(cleanCode);
      if (run_needed) {
        await sessionContext?.ready;
        notebook.activeCellIndex = cell_index;
        await NotebookActions.run(notebook, sessionContext!);
      }
      showNotification(
        `Cell ${cell_index + 1} updated successfully${run_needed ? ' and executed' : ''}`,
        'success'
      );
    } catch (error) {
      showNotification(
        `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'error'
      );
    }
  };

  // Add a new cell at a given position
  const handleAddCell = async (
    code: string,
    cell_index: number,
    run_needed: boolean
  ): Promise<void> => {
    if (!notebookPanel?.model) {
      showNotification(
        'No notebook is open. Please open a notebook first.',
        'error'
      );
      return;
    }
    try {
      const notebook = notebookPanel.content;
      const model = notebookPanel.model;
      if (!model || !notebook || !notebook.model) {
        showNotification('Error: Could not access notebook content.', 'error');
        return;
      }
      if (cell_index < 0 || cell_index > notebook.widgets.length) {
        showNotification(`Invalid cell index ${cell_index + 1}`, 'error');
        return;
      }
      const cleanCode = stripCodeBlockMarkers(code);
      model.sharedModel.insertCell(cell_index, {
        cell_type: 'code',
        source: cleanCode,
        metadata: {},
        outputs: []
      });
      notebook.activeCellIndex = cell_index;
      if (run_needed) {
        await sessionContext?.ready;
        await NotebookActions.run(notebook, sessionContext!);
      }
      const activeCell = notebook.activeCell;
      if (activeCell) {
        notebook.scrollToCell(activeCell);
      }
      showNotification(
        run_needed
          ? `Code executed at cell index ${cell_index + 1}.`
          : `Code added at cell index ${cell_index + 1}.`,
        'success'
      );
    } catch (error) {
      showNotification(
        `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'error'
      );
    }
  };

  // Delete a cell at a given position
  const handleDeleteCell = async (cell_index: number): Promise<void> => {
    if (!notebookPanel?.model) {
      showNotification(
        'No notebook is open. Please open a notebook first.',
        'error'
      );
      return;
    }
    try {
      const notebook = notebookPanel.content;
      if (cell_index < 0 || cell_index >= notebook.widgets.length) {
        showNotification(`Invalid cell index ${cell_index + 1}`, 'error');
        return;
      }
      notebookPanel.model.sharedModel.deleteCell(cell_index);
      showNotification(
        `Cell at index ${cell_index + 1} deleted successfully`,
        'success'
      );
    } catch (error) {
      showNotification(
        `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'error'
      );
    }
  };

  const handleRevertOperation = async (
    cell: CodeCell,
    metadata: JupytApprovedOperation
  ): Promise<boolean> => {
    if (!notebookPanel?.model || !cell.model) {
      showNotification(
        'Notebook or cell model not available for revert.',
        'error'
      );
      return false;
    }
    const notebook = notebookPanel.content;
    const notebookModel = notebookPanel.model;
    const cellModel = cell.model as CodeCellModel;

    console.log('Attempting revert:', metadata.type, 'for cell:', cellModel.id);

    try {
      switch (metadata.type) {
        case 'create_cell':
          // eslint-disable-next-line no-case-declarations
          const indexToDelete = notebook.widgets.findIndex(w => w === cell);
          if (indexToDelete !== -1) {
            notebookModel.sharedModel.deleteCell(indexToDelete);
            showNotification(
              'Cell creation reverted (cell deleted).',
              'success'
            );
            return true; // Revert successful
          } else {
            throw new Error(
              'Could not find index for created cell to revert-delete.'
            );
          }
        // No return needed here due to throw/return above

        case 'update_cell':
          if (metadata.previousCode !== undefined) {
            cellModel.sharedModel.setSource(metadata.previousCode);
            // TODO: Decide if running the cell after revert is desired/needed
            showNotification('Cell update reverted.', 'success');
            return true; // Revert successful
          } else {
            throw new Error(
              'Cannot revert update: Previous code not found in metadata.'
            );
          }
        // No return needed here due to throw/return above

        case 'delete_cell':
          showNotification(
            'Cannot revert a delete operation this way.',
            'error'
          );
          console.warn(
            'Attempted to revert a delete operation via handleRevertOperation'
          );
          return false; // Revert not possible/applicable

        default:
          showNotification(
            `Cannot revert unsupported operation type: ${metadata.type}`,
            'error'
          );
          return false; // Revert failed
      }
    } catch (error) {
      console.error('Error reverting operation:', error);
      showNotification(
        `Failed to revert operation: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'error'
      );
      return false; // Revert failed
    }
  };

  return {
    copyToNotebook,
    modifyCell,
    handleAddCell,
    handleDeleteCell,
    handleRevertOperation
  };
}
