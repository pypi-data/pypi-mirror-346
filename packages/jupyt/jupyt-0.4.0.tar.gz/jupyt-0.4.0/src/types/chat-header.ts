import { QueryType } from './stream';
import { IModelConfig } from './api';

export interface ChatHeaderProps {
  isStreaming: boolean;
  currentType: QueryType | null;
  onNewChat?: () => void;
  onModelConfigChange?: (config: IModelConfig) => void;
}
