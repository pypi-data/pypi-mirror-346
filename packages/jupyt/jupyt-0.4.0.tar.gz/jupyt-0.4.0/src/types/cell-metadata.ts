import { CellOperation } from './stream';

/**
 * Metadata stored in a cell when an operation is pending user approval.
 */
export interface JupytPendingOperation {
  /** Type of operation pending. */
  type: CellOperation['type'];
  /** The proposed code content. Required for 'create' and 'update'. */
  code?: string;
  /** The original code content before the update. Required for 'update'. */
  oldCode?: string;
  /** Original cell index (for updates/deletes). */
  originalIndex?: number;
  /** Whether the cell should be run after approval. */
  runNeeded?: boolean;
}

/**
 * Metadata stored in a cell after an operation has been approved, allowing for revert.
 */
export interface JupytApprovedOperation {
  /** Type of operation that was approved. */
  type: CellOperation['type'];
  /** The code content of the cell *before* the approved update. Only for 'update'. */
  previousCode?: string;
  /** The code content of the cell *before* the approved creation (empty). Only for 'create'. */
  previousCodeForCreate?: ''; // Mark explicitly for created cells
  /** Whether the cell was run after approval. */
  runAfterApproval?: boolean;
}

/**
 * Key used to store pending operation metadata in a cell.
 */
export const PENDING_OPERATION_METADATA_KEY = 'jupyt_pending_operation';

/**
 * Key used to store approved operation metadata in a cell.
 */
export const APPROVED_OPERATION_METADATA_KEY = 'jupyt_approved_operation';
