import { Cell } from '@jupyterlab/cells';

export interface ICellAIButtonProps {
  cell: Cell;
  onCellSelect: (cell: Cell) => void;
}
