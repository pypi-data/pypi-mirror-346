import { NotebookPanel } from '@jupyterlab/notebook';

import { ISessionContext } from '@jupyterlab/apputils';

export interface IChatProps {
  notebookPanel?: NotebookPanel;
  sessionContext?: ISessionContext;
}

export interface ICellOutput {
  output_type: string;
  data: Record<string, any>;
}

export interface ICellPayload {
  cell_id: string;
  cell_type: string;
  source: string;
  outputs: ICellOutput[];
  position: number;
}
