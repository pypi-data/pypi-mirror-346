import { z } from 'zod';

export type ChunkType = 'start' | 'content' | 'end';
export type QueryType = 'simple_query' | 'agent';

export interface CellOperation {
  type: 'create_cell' | 'update_cell' | 'delete_cell';
  cell_id?: string;
  cell_index?: number;
  code?: string;
  run_needed?: boolean;
}

export interface StreamChunk {
  chunk_type: ChunkType;
  type?: QueryType | null;
  progress?: number | null;
  content?: string | null;
  plan?: string | null;
  plan_stage?: string | null;
  cell_output?: string | null;
  next_action?: CellOperation[] | null;
  request_id?: string | null;
  user_id?: string | null;
  session_id?: string | null;
  metadata?: Record<string, unknown> | null;
  completion_status?: string | null;
}

// Create Zod enums from our TypeScript types
const chunkTypeEnum = z.enum([
  'start',
  'content',
  'end'
] as const) satisfies z.ZodType<ChunkType>;
const queryTypeEnum = z.enum([
  'simple_query',
  'agent'
] as const) satisfies z.ZodType<QueryType>;
const cellOpTypeEnum = z.enum([
  'create_cell',
  'update_cell',
  'delete_cell'
] as const);

// Zod schema for runtime validation
export const CellOperationSchema = z.object({
  type: cellOpTypeEnum,
  cell_id: z.string().optional(),
  cell_index: z.number().optional(),
  code: z.string().optional(),
  run_needed: z.boolean().optional()
});

export const StreamChunkSchema = z.object({
  chunk_type: chunkTypeEnum,
  type: queryTypeEnum.nullish(),
  progress: z.number().min(0).max(1).nullish(),
  content: z.string().nullish(),
  plan: z.string().nullish(),
  plan_stage: z.string().nullish(),
  cell_output: z.string().nullish(),
  next_action: z.array(CellOperationSchema).nullish(),
  request_id: z.string().nullish(),
  user_id: z.string().nullish(),
  session_id: z.string().nullish(),
  metadata: z.record(z.unknown()).nullish(),
  completion_status: z.string().nullish()
});
