import { Cell } from '@jupyterlab/cells';
import { NotebookPanel } from '@jupyterlab/notebook';

export interface ICellInfo {
  id: string;
  type: string;
  content: string;
  metadata: any;
  cellNumber: number;
}

export class CellService {
  private static instance: CellService;
  private selectedCell: Cell | null = null;
  private notebookPanel: NotebookPanel | null = null;

  private constructor() {}

  static getInstance(): CellService {
    if (!CellService.instance) {
      CellService.instance = new CellService();
    }
    return CellService.instance;
  }

  setNotebookPanel(panel: NotebookPanel) {
    this.notebookPanel = panel;
  }

  selectCell(cell: Cell) {
    this.selectedCell = cell;
    this.notifyCellSelected();
  }

  getCellNumber(cell: Cell): number {
    if (!this.notebookPanel) {
      return -1;
    }
    return this.notebookPanel.content.widgets.indexOf(cell) + 1;
  }

  getCellByNumber(cellNumber: number): Cell | null {
    if (!this.notebookPanel) {
      return null;
    }
    const index = cellNumber - 1;
    if (index >= 0 && index < this.notebookPanel.content.widgets.length) {
      return this.notebookPanel.content.widgets[index];
    }
    return null;
  }

  getCellById(cellId: string): Cell | null {
    if (!this.notebookPanel) {
      return null;
    }
    const cells = this.notebookPanel.content.widgets;
    return cells.find(cell => cell.model.id === cellId) || null;
  }

  getCellInfo(cell: Cell): ICellInfo {
    return {
      id: cell.model.id,
      type: cell.model.type,
      content: cell.model.sharedModel.source,
      metadata: cell.model.metadata,
      cellNumber: this.getCellNumber(cell)
    };
  }

  updateCell(cellId: string, content: string) {
    if (!this.notebookPanel) {
      return;
    }

    const cells = this.notebookPanel.content.widgets;
    const cell = cells.find(c => c.model.id === cellId);

    if (cell) {
      cell.model.sharedModel.source = content;
    }
  }

  deleteCell(cellId: string) {
    if (!this.notebookPanel) {
      return;
    }

    const cells = this.notebookPanel.content.widgets;
    const cellIndex = cells.findIndex(c => c.model.id === cellId);

    if (cellIndex !== -1) {
      // this.notebookPanel.content.model?.cells.delete(cellIndex);
    }
  }

  private notifyCellSelected() {
    if (this.selectedCell) {
      const cellInfo = this.getCellInfo(this.selectedCell);
      // Dispatch custom event for sidebar to listen
      const event = new CustomEvent('jupyt:cell-selected', {
        detail: cellInfo
      });
      document.dispatchEvent(event);
    }
  }
}
