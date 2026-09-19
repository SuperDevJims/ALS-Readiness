import { useEffect, useState, type ReactNode } from "react";
import { CheckCircle2, ChevronLeft, ChevronRight, LoaderCircle } from "lucide-react";
import { ImageWithFallback } from "../figma/ImageWithFallback";
import {
  STRAND_SHORT_LABEL,
  getLriAttemptResult,
  getLriTestWithItems,
  getStrandAttemptResult,
  getStrandTestWithItems,
  submitLriAttempt,
  submitStrandAttempt,
} from "../../../lib/api/diagnostic";
import { getErrorMessage, isAttemptAlreadySubmitted } from "../../../lib/api/errors";
import type { LriAnswerValue, LriTestListItem, StrandTestListItem } from "../../../lib/api/types";
import {
  LIKERT_OPTIONS,
  formatWhen,
  isComplete,
  toLriAttemptCreate,
  toStrandAttemptCreate,
} from "./pretestLogic";

// The screens a learner sees while taking a pretest (strand + LRI) and viewing a
// saved result. Everything here is loaded from the real API; a failure is shown
// as a failure (with a retry), never replaced by placeholder content.

const ALREADY_SUBMITTED_NOTICE =
  "You've already submitted this test (perhaps on another tab or device), so here is your saved result.";

// ── Shared pieces ────────────────────────────────────────────────────────────

type LoadState<T> = { status: "loading" } | { status: "error"; message: string } | { status: "ready"; data: T };

/** Runs `load` on mount and again whenever the returned retry function is called. */
function useLoad<T>(load: () => Promise<T>, errorFallback: string): [LoadState<T>, () => void] {
  const [state, setState] = useState<LoadState<T>>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    load()
      .then((data) => { if (!cancelled) setState({ status: "ready", data }); })
      .catch((err) => { if (!cancelled) setState({ status: "error", message: getErrorMessage(err, errorFallback) }); });
    return () => { cancelled = true; };
    // `load` is stable for a given screen; only a retry should re-run it.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [attempt]);

  return [state, () => setAttempt((n) => n + 1)];
}

export function AttemptShell({ title, subtitle, onClose, children }: { title: string; subtitle?: string; onClose: () => void; children: ReactNode }) {
  return (
    <div className="min-h-screen bg-[#F0F4F8] p-4 sm:p-8">
      <main className="max-w-4xl mx-auto">
        <button onClick={onClose} className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-[#3535C5] mb-5"><ChevronLeft className="w-4 h-4" /> Back to pre-test</button>
        <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
          <h1 className="text-xl font-bold text-gray-800">{title}</h1>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
          <div className="mt-6">{children}</div>
        </div>
      </main>
    </div>
  );
}

function Loading() {
  return <div className="py-12 flex justify-center"><LoaderCircle className="w-6 h-6 text-[#3535C5] animate-spin" /></div>;
}

function LoadError({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div role="alert" className="flex items-center justify-between gap-4 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl text-sm">
      <span>{message}</span>
      <button onClick={onRetry} className="font-semibold underline shrink-0">Try again</button>
    </div>
  );
}

function SubmitBar({ disabled, saving, error, onSubmit }: { disabled: boolean; saving: boolean; error: string; onSubmit: () => void }) {
  return (
    <div className="border-t border-gray-100 pt-5 mt-6">
      {error && <p role="alert" className="mb-4 p-3 rounded-xl bg-red-50 text-red-700 text-sm">{error}</p>}
      <div className="flex justify-end">
        <button onClick={onSubmit} disabled={disabled || saving} className="px-5 py-2.5 bg-[#3535C5] hover:bg-[#2929a8] text-white rounded-xl text-sm font-medium disabled:bg-gray-200 disabled:text-gray-400">{saving ? "Submitting…" : "Submit baseline responses"}</button>
      </div>
    </div>
  );
}

function ResultCard({ notice, headline, label, detail, footnote, onClose }: { notice?: string; headline: string; label: string; detail: string; footnote?: string; onClose: () => void }) {
  return (
    <div className="text-center">
      {notice && <p role="status" className="mb-5 p-3 rounded-xl bg-blue-50 text-blue-800 text-sm text-left">{notice}</p>}
      <div className="w-16 h-16 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4"><CheckCircle2 className="w-8 h-8" /></div>
      <p className="text-sm text-gray-500">{label}</p>
      <p data-testid="result-headline" className="text-5xl font-bold text-gray-800 my-2">{headline}</p>
      <p className="text-sm text-gray-600">{detail}</p>
      {footnote && <p className="text-xs text-gray-400 mt-3">{footnote}</p>}
      <button onClick={onClose} className="mt-8 px-5 py-2.5 rounded-xl bg-[#3535C5] text-white hover:bg-[#2929a8] text-sm font-medium">Back to pre-test</button>
    </div>
  );
}

const strandTitle = (test: StrandTestListItem) => `${STRAND_SHORT_LABEL[test.strand_code] ?? test.strand_name} diagnostic exam`;

// ── Strand: result ───────────────────────────────────────────────────────────

/** A saved strand result. Also shown right after submitting, and on a 409 (`notice`). */
export function StrandResult({ test, notice, onClose }: { test: StrandTestListItem; notice?: string; onClose: () => void }) {
  const [state, retry] = useLoad(() => getStrandAttemptResult(test.test_id), "Your result could not be loaded.");

  return (
    <AttemptShell title={strandTitle(test)} subtitle={test.title} onClose={onClose}>
      {state.status === "loading" && <Loading />}
      {state.status === "error" && <LoadError message={state.message} onRetry={retry} />}
      {state.status === "ready" && (
        <ResultCard
          notice={notice}
          label="Mean Percentage Score"
          headline={`${state.data.mps}%`}
          detail={`${state.data.total_score} of ${state.data.item_count} correct`}
          footnote={state.data.taken_at ? `Submitted ${formatWhen(state.data.taken_at)}` : undefined}
          onClose={onClose}
        />
      )}
    </AttemptShell>
  );
}

// ── Strand: take the test ────────────────────────────────────────────────────

export function StrandAttempt({ test, onClose }: { test: StrandTestListItem; onClose: () => void }) {
  const [detail, retry] = useLoad(() => getStrandTestWithItems(test.test_id), "This test could not be opened.");
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [saving, setSaving] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [finished, setFinished] = useState<{ notice?: string } | null>(null);

  if (finished) return <StrandResult test={test} notice={finished.notice} onClose={onClose} />;

  const items = detail.status === "ready" ? detail.data.items : [];
  const item = items[current];

  const submit = async () => {
    setSaving(true); setSubmitError("");
    try {
      await submitStrandAttempt(test.test_id, toStrandAttemptCreate(items, answers));
      setFinished({});
    } catch (err) {
      // A 409 means another tab/device already submitted: that's a result to show, not a dead end.
      if (isAttemptAlreadySubmitted(err)) setFinished({ notice: ALREADY_SUBMITTED_NOTICE });
      else setSubmitError(getErrorMessage(err, "Your answers could not be submitted. Please try again."));
    } finally { setSaving(false); }
  };

  return (
    <AttemptShell title={strandTitle(test)} subtitle={detail.status === "ready" ? `Question ${current + 1} of ${items.length}` : test.title} onClose={onClose}>
      {detail.status === "loading" && <Loading />}
      {detail.status === "error" && <LoadError message={detail.message} onRetry={retry} />}
      {detail.status === "ready" && items.length === 0 && <p className="text-sm text-gray-500">This test has no questions yet.</p>}
      {detail.status === "ready" && item && (
        <>
          <div className="h-2 bg-gray-100 rounded-full mb-6"><div className="h-full bg-[#3535C5] rounded-full" style={{ width: `${((current + 1) / items.length) * 100}%` }} /></div>
          <section className="border border-gray-100 rounded-2xl p-6">
            {/* Not every question has an image (asset_url is null when there's none, or storage isn't configured). */}
            {item.asset_url && <ImageWithFallback src={item.asset_url} alt="Illustration for this question" className="max-h-72 w-auto max-w-full object-contain rounded-xl mb-5" />}
            <p className="text-gray-800 text-lg font-medium leading-relaxed mb-6 whitespace-pre-line">{item.question_text}</p>
            <div className="space-y-3">
              {item.options.map((option, index) => (
                <button key={option.option_id} aria-pressed={answers[item.item_id] === option.option_id} onClick={() => setAnswers((old) => ({ ...old, [item.item_id]: option.option_id }))} className={`w-full flex text-left gap-3 p-4 border rounded-xl transition-colors ${answers[item.item_id] === option.option_id ? "border-[#3535C5] bg-indigo-50 text-indigo-900" : "border-gray-200 hover:border-indigo-300 text-gray-700"}`}>
                  <span className="w-6 h-6 shrink-0 rounded-full border flex justify-center items-center text-xs font-semibold">{String.fromCharCode(65 + index)}</span>{option.option_text}
                </button>
              ))}
            </div>
          </section>
          <div className="flex justify-between mt-5">
            <button onClick={() => setCurrent((n) => n - 1)} disabled={current === 0} className="inline-flex gap-1 items-center px-4 py-2 text-sm text-gray-600 disabled:text-gray-300"><ChevronLeft className="w-4 h-4" /> Previous</button>
            {current < items.length - 1 ? <button onClick={() => setCurrent((n) => n + 1)} className="inline-flex gap-1 items-center px-4 py-2 rounded-xl text-sm text-white bg-[#3535C5]">Next <ChevronRight className="w-4 h-4" /></button> : <span />}
          </div>
          <SubmitBar disabled={!isComplete(items, answers)} saving={saving} error={submitError} onSubmit={submit} />
        </>
      )}
    </AttemptShell>
  );
}

// ── LRI: result ──────────────────────────────────────────────────────────────

export function LriResult({ test, notice, onClose }: { test: LriTestListItem; notice?: string; onClose: () => void }) {
  const [state, retry] = useLoad(() => getLriAttemptResult(test.test_id), "Your result could not be loaded.");

  return (
    <AttemptShell title={test.title} onClose={onClose}>
      {state.status === "loading" && <Loading />}
      {state.status === "error" && <LoadError message={state.message} onRetry={retry} />}
      {state.status === "ready" && (
        <ResultCard
          notice={notice}
          label="Learner Readiness Inventory score"
          headline={state.data.lri_score.toFixed(2)}
          detail="Average of your responses on the 1–4 agreement scale"
          footnote={state.data.submitted_at ? `Submitted ${formatWhen(state.data.submitted_at)}` : undefined}
          onClose={onClose}
        />
      )}
    </AttemptShell>
  );
}

// ── LRI: take the inventory ──────────────────────────────────────────────────

export function LriAttempt({ test, onClose }: { test: LriTestListItem; onClose: () => void }) {
  // The LRI detail always includes its statements - there's no include_items switch.
  const [detail, retry] = useLoad(() => getLriTestWithItems(test.test_id), "The Learner Readiness Inventory could not be opened.");
  const [answers, setAnswers] = useState<Record<number, LriAnswerValue>>({});
  const [saving, setSaving] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [finished, setFinished] = useState<{ notice?: string } | null>(null);

  if (finished) return <LriResult test={test} notice={finished.notice} onClose={onClose} />;

  const items = detail.status === "ready" ? detail.data.items : [];

  const submit = async () => {
    setSaving(true); setSubmitError("");
    try {
      await submitLriAttempt(test.test_id, toLriAttemptCreate(items, answers));
      setFinished({});
    } catch (err) {
      if (isAttemptAlreadySubmitted(err)) setFinished({ notice: ALREADY_SUBMITTED_NOTICE });
      else setSubmitError(getErrorMessage(err, "Your LRI responses could not be submitted. Please try again."));
    } finally { setSaving(false); }
  };

  return (
    <AttemptShell title={test.title} subtitle="Select one response for every statement." onClose={onClose}>
      {detail.status === "loading" && <Loading />}
      {detail.status === "error" && <LoadError message={detail.message} onRetry={retry} />}
      {detail.status === "ready" && items.length === 0 && <p className="text-sm text-gray-500">This inventory has no statements yet.</p>}
      {detail.status === "ready" && items.length > 0 && (
        <>
          <div className="overflow-x-auto border border-slate-800 rounded-sm">
            <table className="w-full min-w-[700px] table-fixed border-collapse text-sm">
              <thead className="bg-[#244477] text-white">
                <tr>
                  <th className="w-1/2 border border-slate-800 p-3 text-center font-semibold">Statement</th>
                  {LIKERT_OPTIONS.map(({ label }) => <th key={label} className="w-[12.5%] border border-slate-800 p-2 text-center font-semibold leading-tight">{label}</th>)}
                </tr>
              </thead>
              <tbody>
                {items.map((item, index) => (
                  <tr key={item.item_id} className="odd:bg-white even:bg-slate-50">
                    <td className="border border-slate-800 p-3 text-gray-800 align-top"><span className="font-semibold mr-1">{index + 1}.</span>{item.question_text}</td>
                    {LIKERT_OPTIONS.map(({ label, value }) => (
                      <td key={value} className="border border-slate-800 p-3 text-center">
                        <input aria-label={`${item.question_text}: ${label}`} type="radio" name={`item-${item.item_id}`} value={value} checked={answers[item.item_id] === value} onChange={() => setAnswers((current) => ({ ...current, [item.item_id]: value }))} className="h-4 w-4 accent-[#244477]" />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <SubmitBar disabled={!isComplete(items, answers)} saving={saving} error={submitError} onSubmit={submit} />
        </>
      )}
    </AttemptShell>
  );
}
