import { useState, useCallback } from 'react';
import { CellOperation } from '../types/stream';

interface IUseOperationApprovalArgs {
  executeCellOperation: (op: CellOperation) => Promise<string | undefined>;
  getCellContent: (index: number) => string | undefined;
}

interface IPendingOperation {
  operation: CellOperation;
  oldCode?: string;
}

/**
 * Hook to manage approval workflow for cell operations.
 * Handles queuing, approving, and rejecting operations with theme-aware UI components.
 */
export function useOperationApproval({
  executeCellOperation,
  getCellContent
}: IUseOperationApprovalArgs) {
  const [pendingOperations, setPendingOperations] = useState<
    IPendingOperation[]
  >([]);
  const [isApprovalMode, setIsApprovalMode] = useState(false);

  const queueOperations = useCallback(
    (operations: CellOperation[]) => {
      const pending = operations.map(operation => {
        let oldCode: string | undefined;
        if (
          operation.type === 'update_cell' &&
          typeof operation.cell_index === 'number'
        ) {
          oldCode = getCellContent(operation.cell_index);
        }
        return { operation, oldCode };
      });
      setPendingOperations(pending);
      setIsApprovalMode(true);
    },
    [getCellContent]
  );

  const approveOperation = useCallback(
    async (index: number) => {
      const operation = pendingOperations[index];
      if (!operation) {
        return;
      }

      await executeCellOperation(operation.operation);
      setPendingOperations(prev => prev.filter((_, i) => i !== index));

      if (pendingOperations.length === 1) {
        setIsApprovalMode(false);
      }
    },
    [pendingOperations, executeCellOperation]
  );

  const rejectOperation = useCallback(
    (index: number) => {
      setPendingOperations(prev => prev.filter((_, i) => i !== index));
      if (pendingOperations.length === 1) {
        setIsApprovalMode(false);
      }
    },
    [pendingOperations]
  );

  const executeAllOperations = useCallback(async () => {
    for (const { operation } of pendingOperations) {
      await executeCellOperation(operation);
    }
    setPendingOperations([]);
    setIsApprovalMode(false);
  }, [pendingOperations, executeCellOperation]);

  return {
    pendingOperations,
    isApprovalMode,
    queueOperations,
    approveOperation,
    rejectOperation,
    executeAllOperations
  };
}
