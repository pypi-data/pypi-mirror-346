import { API_CONFIG } from '../config';
import { INotebookState, IModelConfig } from '../types/api';
import { StreamChunk } from '../types/stream';

export interface IAgenticAssistantPayload {
  query: string;
  session_id: string;
  notebook_state: INotebookState;
  llm_config: IModelConfig;
  search?: boolean;
  plan?: string;
  plan_stage?: string;
  cell_output?: string;
}

/**
 * Calls the /assistant endpoint and yields StreamChunk objects as they arrive.
 */
export async function* streamAgenticAssistant(
  payload: IAgenticAssistantPayload
): AsyncGenerator<StreamChunk, void, unknown> {
  // Use the API key that was set during authentication
  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': API_CONFIG.apiKey,
    Accept: 'text/event-stream'
  };

  // Validate API key exists
  if (!API_CONFIG.apiKey) {
    throw new Error('API key is missing. Please log in first.');
  } else {
    // Log that we have a valid API key - this helps confirm it's loaded correctly after refresh
    console.log(
      'Using API key from config (length):',
      API_CONFIG.apiKey.length
    );
  }
  // Log the model being used for debugging
  console.log('Sending request with model:', payload);

  // Ensure the model is being sent in the correct format
  // The API expects the model to be passed as is, e.g. 'claude-3-7-sonnet'
  // No modifications are made to the model name selected by the user

  const response = await fetch(`${API_CONFIG.baseUrl}/assistant`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('Response body reader could not be created');
  }
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }
    const chunkStr = decoder.decode(value, { stream: true });
    buffer += chunkStr;
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      if (!line.startsWith('data:')) {
        continue;
      }
      const data = line.slice(5).trim();
      if (!data) {
        continue;
      }
      try {
        const chunk: StreamChunk = JSON.parse(data);
        yield chunk;
      } catch (err) {
        // Ignore parse errors for incomplete lines
      }
    }
  }
}
