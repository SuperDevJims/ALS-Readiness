import { BarChart3, BookOpen, Calculator, CheckCircle2, FileText } from "lucide-react";
import { ImageWithFallback } from "../figma/ImageWithFallback";
import { STRAND_SHORT_LABEL } from "../../../lib/api/diagnostic";
import type { StrandCode, StrandTestListItem } from "../../../lib/api/types";

// Shared strand branding + attempt card, used by both the pretest hub and the
// posttest hub - same three strands, same visual identity, only the "why is
// this locked" reason differs between the two callers.

const strandStyles: Record<StrandCode, { icon: typeof BookOpen; tone: string }> = {
  "LS1-EN": { icon: BookOpen, tone: "blue" },
  "LS1-FIL": { icon: FileText, tone: "rose" },
  "LS3": { icon: Calculator, tone: "violet" },
};
const toneClasses: Record<string, string> = {
  blue: "bg-blue-50 text-blue-600 border-blue-100", rose: "bg-rose-50 text-rose-600 border-rose-100", violet: "bg-violet-50 text-violet-600 border-violet-100",
};

export function StrandTestCard({
  test,
  canAttempt,
  disabledReason,
  attemptLabel = "Attempt test",
  onAttempt,
  canShowScore = false,
  onShowScore,
}: {
  test: StrandTestListItem;
  /** Whether the precondition for starting an attempt is met (e.g. intake done, or pretest done). */
  canAttempt: boolean;
  /** Shown on the button in place of `attemptLabel` when `canAttempt` is false. */
  disabledReason: string;
  attemptLabel?: string;
  onAttempt: () => void;
  /** True once both this strand's pretest AND posttest are completed - a deliberate, learner-initiated reveal, not shown on submission. */
  canShowScore?: boolean;
  onShowScore?: () => void;
}) {
  const setting = strandStyles[test.strand_code];
  const Icon = setting.icon;
  const done = test.attempt_status === "completed";
  return (
    <article className="overflow-hidden rounded-xl border border-gray-100">
      {/* image_url is optional - most tests don't have one. */}
      {test.image_url && <ImageWithFallback src={test.image_url} alt={`${STRAND_SHORT_LABEL[test.strand_code]} test`} className="h-28 w-full object-cover" />}
      <div className="p-4">
        <div className="flex justify-between mb-4"><div className={`w-10 h-10 rounded-xl border flex items-center justify-center ${toneClasses[setting.tone]}`}><Icon className="w-5 h-5" /></div><span className="text-xs text-gray-400 font-mono">{test.strand_code}</span></div>
        <h4 className="text-gray-800 font-semibold">{STRAND_SHORT_LABEL[test.strand_code]}</h4>
        <p className="text-xs text-gray-500 mt-1 mb-4">{test.title}</p>
        {/* Completed, no score shown by default - only a deliberate "Show Score" click reveals it, and only once both halves exist. */}
        {done ? (
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm text-green-700 bg-green-50 py-2 px-3 rounded-lg"><CheckCircle2 className="w-4 h-4" /> Completed</div>
            {canShowScore && onShowScore && (
              <button onClick={onShowScore} className="w-full flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm border border-[#3535C5] text-[#3535C5] hover:bg-indigo-50">
                <BarChart3 className="w-3.5 h-3.5" /> Show Score
              </button>
            )}
          </div>
        ) : (
          <button onClick={onAttempt} disabled={!canAttempt} className="w-full py-2 rounded-lg text-sm bg-[#3535C5] text-white hover:bg-[#2929a8] disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed">
            {canAttempt ? attemptLabel : disabledReason}
          </button>
        )}
      </div>
    </article>
  );
}
