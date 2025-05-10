import { INotebookCell, INotebookState } from '../types/api';
import { NotebookPanel } from '@jupyterlab/notebook';

/**
 * Extracts the full notebook state in the format required by the agentic loop API.
 * @param notebookPanel The JupyterLab NotebookPanel instance
 * @returns INotebookState object containing all cells and notebook metadata
 */
export function extractNotebookState(
  notebookPanel: NotebookPanel | undefined
): INotebookState {
  if (!notebookPanel || !notebookPanel.model) {
    return { cells: [], metadata: {} };
  }
  const notebook = notebookPanel.content;
  const model = notebookPanel.model;
  const cells: INotebookCell[] = notebook.widgets.map((cellWidget, idx) => {
    const cellModel = cellWidget.model;
    return {
      cell_id: cellModel.id,
      cell_type: cellModel.type,
      source: cellModel.sharedModel.getSource(),
      outputs:
        cellModel.type === 'code' && 'outputs' in cellModel
          ? (cellModel as any).outputs?.toJSON?.() || []
          : [],
      cell_index: idx
    };
  });
  const metadata = model.sharedModel.getMetadata();
  return { cells, metadata };
}
