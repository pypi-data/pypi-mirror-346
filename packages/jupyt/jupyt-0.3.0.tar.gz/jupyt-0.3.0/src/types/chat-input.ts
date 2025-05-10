export interface ChatInputProps {
  value: string;
  isStreaming: boolean;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  isAgenticLooping?: boolean;
  onStopAgenticLoop?: () => void;
}
