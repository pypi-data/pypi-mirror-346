import { useState } from 'react';

export function useAgenticState() {
  const [plan, setPlan] = useState<string | null>(null);
  const [planStage, setPlanStage] = useState<string | null>(null);
  const [cellOutput, setCellOutput] = useState<string | null>(null);

  return {
    plan,
    setPlan,
    planStage,
    setPlanStage,
    cellOutput,
    setCellOutput
  };
}
