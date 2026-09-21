import { useEffect, useState } from "react";
import { ArrowDown, ArrowUp, LoaderCircle } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "../ui/dialog";
import { getStrandAttemptResult } from "../../../lib/api/diagnostic";
import { getErrorMessage } from "../../../lib/api/errors";
import type { StrandAttemptResult } from "../../../lib/api/types";

// Shared "Show Score" reveal, used by both the pretest hub and the posttest
// hub's StrandTestCard. Only ever mounted once both halves are already known
// complete - a separate, deliberate, learner-initiated action, not the
// submission-time flow (which stays score-free per that locked decision).

type LoadState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; pre: StrandAttemptResult; post: StrandAttemptResult };

export function ScoreCompareModal({
  strandLabel,
  pretestTestId,
  posttestTestId,
  onClose,
}: {
  strandLabel: string;
  pretestTestId: number;
  posttestTestId: number;
  onClose: () => void;
}) {
  const [state, setState] = useState<LoadState>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    Promise.all([getStrandAttemptResult(pretestTestId), getStrandAttemptResult(posttestTestId)])
      .then(([pre, post]) => { if (!cancelled) setState({ status: "ready", pre, post }); })
      .catch((err) => { if (!cancelled) setState({ status: "error", message: getErrorMessage(err, "Your scores could not be loaded.") }); });
    return () => { cancelled = true; };
  }, [pretestTestId, posttestTestId]);

  const improved = state.status === "ready" && state.post.mps >= state.pre.mps;

  return (
    <Dialog open onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{strandLabel} score</DialogTitle>
          <DialogDescription>Pre-test vs. post-test Mean Percentage Score.</DialogDescription>
        </DialogHeader>

        {state.status === "loading" && <div className="py-10 flex justify-center"><LoaderCircle className="w-6 h-6 text-[#3535C5] animate-spin" /></div>}
        {state.status === "error" && <p role="alert" className="text-sm text-red-700 bg-red-50 p-3 rounded-xl">{state.message}</p>}
        {state.status === "ready" && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="text-center p-4 bg-gray-50 rounded-xl">
                <p className="text-xs text-gray-500 mb-1">Pre-test</p>
                <p className="text-2xl font-bold text-gray-800">{state.pre.mps}%</p>
                <p className="text-xs text-gray-400 mt-1">{state.pre.total_score}/{state.pre.item_count} correct</p>
              </div>
              <div className={`text-center p-4 rounded-xl ${improved ? "bg-green-50" : "bg-orange-50"}`}>
                <p className="text-xs text-gray-500 mb-1">Post-test</p>
                <p className={`text-2xl font-bold ${improved ? "text-green-700" : "text-orange-700"}`}>{state.post.mps}%</p>
                <p className="text-xs text-gray-400 mt-1">{state.post.total_score}/{state.post.item_count} correct</p>
              </div>
            </div>
            <div className={`flex items-center justify-center gap-1.5 text-sm font-medium ${improved ? "text-green-700" : "text-orange-700"}`}>
              {improved ? <ArrowUp className="w-4 h-4" /> : <ArrowDown className="w-4 h-4" />}
              {Math.abs(Math.round((state.post.mps - state.pre.mps) * 100) / 100)} point {improved ? "improvement" : "decrease"}
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
