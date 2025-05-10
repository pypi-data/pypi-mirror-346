import { NotebookPanel } from '@jupyterlab/notebook';
import { CellOperation } from './stream';
import { CodeCell } from '@jupyterlab/cells';

export interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  onCopyCode?: (code: string) => void;
  onExecuteCode?: (code: string) => void;
  onModifyCell?: (code: string, position: number) => void;
  onAddCell?: (code: string, position: number, runNeeded: boolean) => void;
  onDeleteCell?: (position: number) => void;
  referencedCells?: Set<number>;
  operations?: CellOperation[];
  showNotification?: (message: string, type: 'success' | 'error') => void;
  onRevertOperation?: (
    operation: CellOperation,
    cell: CodeCell
  ) => Promise<void>;
  canRevertOperation?: (operation: CellOperation) => Promise<boolean>;
  notebookPanel?: NotebookPanel;
}
