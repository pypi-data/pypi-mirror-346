export function extractCellReferences(text: string): {
  cleanQuery: string;
  cellNumbers: Set<number>;
} {
  const cellRefs = text.match(/@cell(\d+)/g) || [];
  const cellNumbers = new Set(
    cellRefs.map(ref => parseInt(ref.replace('@cell', ''), 10))
  );
  const cleanQuery = text.replace(/@cell\d+\s*/g, '').trim();
  return { cleanQuery, cellNumbers };
}

// Utility to strip markdown code block markers from code
export function stripCodeBlockMarkers(code: string): string {
  // Remove triple backticks and optional language
  return code.replace(/^```[a-zA-Z]*\n?|```$/gm, '').trim();
}

// Helper to extract JSON object from a string containing text + JSON
export function extractJsonFromContent(content: string): {
  json: any | null;
  rest: string;
} {
  const firstBrace = content.indexOf('{');
  const lastBrace = content.lastIndexOf('}');
  if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
    const jsonStr = content.slice(firstBrace, lastBrace + 1);
    try {
      const json = JSON.parse(jsonStr);
      const rest = (
        content.slice(0, firstBrace) + content.slice(lastBrace + 1)
      ).trim();
      return { json, rest };
    } catch (e) {
      // fallback: treat as plain text
    }
  }
  return { json: null, rest: content };
}

/**
 * Removes all <cell_operation>...</cell_operation> blocks from a string.
 */
export function removeCellOperationTags(input: string): string {
  return input
    .replace(/<cell_operation>[\s\S]*?<\/cell_operation>/g, '')
    .trim();
}
