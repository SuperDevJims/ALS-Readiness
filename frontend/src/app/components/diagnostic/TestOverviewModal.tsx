import { Clock, ListChecks } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "../ui/dialog";
import { formatCountdown } from "./testTiming";

// Instructions/overview modal shown before any test (strand pretest, LRI, and
// - reused as-is - posttest in Phase 3). The actual test only starts once
// "Start" is clicked; closing/cancelling never begins an attempt.

export function TestOverviewModal({
  title,
  description,
  timeLimitSeconds,
  itemCount,
  onStart,
  onCancel,
}: {
  title: string;
  description: string;
  /** Null means untimed - no "time limit" line is shown. */
  timeLimitSeconds: number | null;
  /** Omit while still loading; shown once known. */
  itemCount?: number;
  onStart: () => void;
  onCancel: () => void;
}) {
  return (
    <Dialog open onOpenChange={(open) => { if (!open) onCancel(); }}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription className="whitespace-pre-line text-left">{description}</DialogDescription>
        </DialogHeader>

        <div className="space-y-2 text-sm text-gray-600">
          {typeof itemCount === "number" && (
            <div className="flex items-center gap-2"><ListChecks className="w-4 h-4 text-[#3535C5]" /> {itemCount} question{itemCount === 1 ? "" : "s"}</div>
          )}
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-[#3535C5]" />
            {timeLimitSeconds === null ? "No time limit" : `Time limit: ${formatCountdown(timeLimitSeconds)}`}
          </div>
          <p>Once you submit, this attempt cannot be retaken.</p>
        </div>

        <DialogFooter>
          <button onClick={onCancel} className="px-4 py-2.5 rounded-xl text-sm font-medium text-gray-600 hover:bg-gray-50">Not now</button>
          <button onClick={onStart} className="px-5 py-2.5 rounded-xl text-sm font-medium bg-[#3535C5] text-white hover:bg-[#2929a8]">Start</button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
