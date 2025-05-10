import { CellOperation } from './stream';

export interface IApiConfig {
  baseUrl: string;
  apiKey: string;
}

export interface INotebookCell {
  cell_id: string;
  cell_type: string;
  source: string;
  outputs: Array<{
    output_type: string;
    data: Record<string, any>;
  }>;
  cell_index: number;
}

export interface INotebookState {
  cells: INotebookCell[];
  metadata: Record<string, any>;
}

export interface IModelConfig {
  provider: string;
  model: string;
  temperature: number;
  max_tokens?: number;
  stream: boolean;
}

export interface IMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: number;
  codeBlocks?: ICodeBlock[];
  operations?: CellOperation[];
}

export interface ICodeBlock {
  language: string;
  code: string;
}

export interface IAPIConfig {
  endpoint: string;
  model: string;
  temperature: number;
  maxTokens: number;
  stream: boolean;
  apiKey?: string;
}
