import { INotebookCell } from '../types/api';

/**
 * Extracts plain text output from a notebook cell, ignoring images/plots.
 * @param cell The notebook cell object
 * @returns Concatenated plain text output
 */
export function extractTextOutputFromCell(cell: INotebookCell): string {
  if (!cell.outputs || !Array.isArray(cell.outputs)) {
    return '';
  }
  return cell.outputs
    .filter(
      output =>
        output.output_type === 'stream' ||
        output.output_type === 'error' ||
        (output.output_type === 'execute_result' &&
          output.data &&
          typeof output.data['text/plain'] === 'string')
    )
    .map(output => {
      if (output.output_type === 'stream') {
        return (output as any).text || '';
      }
      if (output.output_type === 'error') {
        return (
          ((output as any).ename || '') + ': ' + ((output as any).evalue || '')
        );
      }
      if (
        output.output_type === 'execute_result' &&
        output.data &&
        output.data['text/plain']
      ) {
        return output.data['text/plain'];
      }
      return '';
    })
    .join('\n')
    .trim();
}
