import { useEffect, useState } from "react";
import { BookOpen, Calculator, CheckCircle2, ClipboardList, FileText, LoaderCircle, LockKeyhole, Star } from "lucide-react";
import { AppLayout } from "../shared/AppLayout";
import { ImageWithFallback } from "../figma/ImageWithFallback";
import {
  STRAND_CODES,
  STRAND_SHORT_LABEL,
  getLriTests,
  getParticipantIntake,
  getStrandTests,
  indexByStrandCode,
} from "../../../lib/api/diagnostic";
import { getErrorMessage } from "../../../lib/api/errors";
import type { LriTestListItem, StrandCode, StrandTestListItem } from "../../../lib/api/types";
import { LriAttempt, LriResult, StrandAttempt, StrandResult } from "./PretestAttempts";

// Pre-test hub: Part I participant intake, Part II Learner Readiness Inventory,
// Part III one diagnostic exam per strand. All of it comes from the real API; if
// something fails to load, the hub says so (with a retry) rather than showing
// stand-in content.

const strandStyles: Record<StrandCode, { icon: typeof BookOpen; tone: string }> = {
  "LS1-EN": { icon: BookOpen, tone: "blue" },
  "LS1-FIL": { icon: FileText, tone: "rose" },
  "LS3": { icon: Calculator, tone: "violet" },
};
const toneClasses: Record<string, string> = {
  blue: "bg-blue-50 text-blue-600 border-blue-100", rose: "bg-rose-50 text-rose-600 border-rose-100", violet: "bg-violet-50 text-violet-600 border-violet-100",
};

type View =
  | { name: "hub" }
  | { name: "strand-attempt"; test: StrandTestListItem }
  | { name: "strand-result"; test: StrandTestListItem }
  | { name: "lri-attempt"; test: LriTestListItem }
  | { name: "lri-result"; test: LriTestListItem };

function PretestLoadingIndicator() {
  return (
    <div className="py-12 flex justify-center">
      <LoaderCircle className="w-6 h-6 text-[#3535C5] animate-spin" />
    </div>
  );
}

export function DiagnosticTest({ navigate, user, onLogout }) {
  const [strandTests, setStrandTests] = useState<StrandTestListItem[]>([]);
  const [lriTests, setLriTests] = useState<LriTestListItem[]>([]);
  const [intakeComplete, setIntakeComplete] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [view, setView] = useState<View>({ name: "hub" });

  // Gate for Parts II/III is the learner's real intake record, not a browser-local flag.
  const loadHub = async () => {
    setLoading(true); setError("");
    try {
      const [strandData, lriData, intake] = await Promise.all([getStrandTests("pretest"), getLriTests(), getParticipantIntake()]);
      setStrandTests(strandData.tests);
      setLriTests(lriData.tests);
      setIntakeComplete(intake !== null);
    } catch (err) {
      setError(getErrorMessage(err, "The pre-test could not be loaded. Please try again."));
    } finally { setLoading(false); }
  };
  useEffect(() => { loadHub(); }, []);

  const backToHub = () => { setView({ name: "hub" }); loadHub(); };

  if (view.name === "strand-attempt") return <StrandAttempt test={view.test} onClose={backToHub} />;
  if (view.name === "strand-result") return <StrandResult test={view.test} onClose={backToHub} />;
  if (view.name === "lri-attempt") return <LriAttempt test={view.test} onClose={backToHub} />;
  if (view.name === "lri-result") return <LriResult test={view.test} onClose={backToHub} />;

  // Strands are identified by strand_code, never by name; unknown codes are skipped.
  const byCode = indexByStrandCode(strandTests);
  const strands = STRAND_CODES.map((code) => byCode[code]).filter((test): test is StrandTestListItem => Boolean(test));
  const completedStrands = strands.filter((test) => test.attempt_status === "completed");
  const lriComplete = lriTests.length > 0 && lriTests.every((test) => test.attempt_status === "completed");
  const allComplete = strands.length > 0 && completedStrands.length === strands.length && lriComplete;

  return <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage="diagnostic-test">
    <main className="p-6 max-w-6xl mx-auto w-full">
      <section className="bg-gradient-to-r from-[#182f68] to-[#3535C5] rounded-2xl p-7 text-white mb-6">
        <p className="text-blue-200 text-xs font-semibold uppercase tracking-[0.16em] mb-2">Baseline assessment · No EEG device</p>
        <h2 className="text-2xl font-bold mb-2">Pre-test</h2>
        <p className="text-blue-100 text-sm max-w-2xl leading-relaxed">Complete the participant intake, Learner Readiness Inventory, and three diagnostic exams to establish your baseline.</p>
      </section>

      {loading ? <PretestLoadingIndicator /> : error ? (
        <div role="alert" className="flex items-center justify-between gap-4 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl text-sm">
          <span>{error}</span><button onClick={loadHub} className="font-semibold underline shrink-0">Try again</button>
        </div>
      ) : <>
        <div className="grid gap-4 md:grid-cols-3 mb-6">
          <Stat icon={ClipboardList} label="Diagnostic tests" value={`${completedStrands.length}/${strands.length}`} />
          <Stat icon={CheckCircle2} label="LRI status" value={lriComplete ? "Complete" : "Pending"} />
          <Stat icon={Star} label="Pre-test status" value={allComplete ? "Complete" : "In progress"} />
        </div>

        <div className="space-y-5">
          <PartCard number="Part I" title="Participant intake" description="Background questionnaire required before all assessment activities." status={intakeComplete ? "Completed" : "Required"} action={intakeComplete ? "Review intake" : "Complete intake"} onClick={() => navigate("participant-intake")} />

          {lriTests.length === 0 && <section className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm"><p className="text-xs font-bold text-[#3535C5] uppercase tracking-wider mb-1">Part II</p><h3 className="text-gray-800 font-bold text-lg">Learner Readiness Inventory</h3><p className="text-sm text-gray-500 mt-1">No readiness inventory is currently available.</p></section>}
          {lriTests.map((test) => {
            const done = test.attempt_status === "completed";
            return <PartCard key={test.test_id} number="Part II" title={test.title} description={test.description} status={done ? "Completed" : intakeComplete ? "Ready to attempt" : "Locked until Part I"} disabled={!done && !intakeComplete} action={done ? "View result" : "Attempt LRI"} onClick={() => setView(done ? { name: "lri-result", test } : { name: "lri-attempt", test })} />;
          })}

          <section className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between mb-5">
              <div><p className="text-xs font-bold text-[#3535C5] uppercase tracking-wider mb-1">Part III</p><h3 className="text-gray-800 font-bold text-lg">Diagnostic / Equivalency Exams</h3><p className="text-gray-500 text-sm mt-1">One baseline exam for each enrolled learning strand. Completed pre-tests cannot be retaken.</p></div>
              <span className={`inline-flex items-center gap-1.5 self-start px-3 py-1.5 rounded-full text-xs font-medium ${intakeComplete ? "bg-green-50 text-green-700" : "bg-gray-100 text-gray-500"}`}><LockKeyhole className="w-3.5 h-3.5" /> {intakeComplete ? "Part I complete" : "Complete Part I first"}</span>
            </div>
            <div className="grid md:grid-cols-3 gap-4">
              {strands.map((test) => <StrandCard key={test.test_id} test={test} intakeComplete={intakeComplete} onAttempt={() => setView({ name: "strand-attempt", test })} onViewResult={() => setView({ name: "strand-result", test })} />)}
              {!strands.length && <p className="text-sm text-gray-500">No pre-test strands are currently available.</p>}
            </div>
          </section>
        </div>
      </>}
    </main>
  </AppLayout>;
}

function Stat({ icon: Icon, label, value }) { return <div className="bg-white rounded-2xl border border-gray-100 p-4 flex items-center gap-3"><div className="w-10 h-10 bg-indigo-50 text-[#3535C5] rounded-xl flex items-center justify-center"><Icon className="w-5 h-5" /></div><div><p className="text-lg font-bold text-gray-800">{value}</p><p className="text-xs text-gray-500">{label}</p></div></div>; }

function PartCard({ number, title, imageUrl, description, status, action, onClick, disabled }: { number: string; title: string; imageUrl?: string | null; description: string; status: string; action: string; onClick: () => void; disabled?: boolean }) { return <section className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row gap-5 sm:items-center sm:justify-between">{imageUrl && <ImageWithFallback src={imageUrl} alt="" className="h-24 w-full sm:w-36 object-cover rounded-xl" />}<div className="flex-1"><p className="text-xs font-bold text-[#3535C5] uppercase tracking-wider mb-1">{number}</p><h3 className="text-gray-800 font-bold text-lg">{title}</h3><p className="text-gray-500 text-sm mt-1">{description}</p></div><div className="flex flex-col sm:items-end gap-2 shrink-0"><span className={`text-xs font-medium px-2.5 py-1 rounded-full ${disabled ? "bg-amber-50 text-amber-700" : "bg-blue-50 text-blue-700"}`}>{status}</span><button onClick={onClick} disabled={disabled} className="px-4 py-2.5 rounded-xl text-sm font-medium bg-[#3535C5] text-white hover:bg-[#2929a8] disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed">{action}</button></div></section>; }

function StrandCard({ test, intakeComplete, onAttempt, onViewResult }: { test: StrandTestListItem; intakeComplete: boolean; onAttempt: () => void; onViewResult: () => void }) {
  const setting = strandStyles[test.strand_code];
  const Icon = setting.icon;
  const done = test.attempt_status === "completed";
  return <article className="overflow-hidden rounded-xl border border-gray-100">
    {/* image_url is optional - most tests don't have one. */}
    {test.image_url && <ImageWithFallback src={test.image_url} alt={`${STRAND_SHORT_LABEL[test.strand_code]} test`} className="h-28 w-full object-cover" />}
    <div className="p-4">
      <div className="flex justify-between mb-4"><div className={`w-10 h-10 rounded-xl border flex items-center justify-center ${toneClasses[setting.tone]}`}><Icon className="w-5 h-5" /></div><span className="text-xs text-gray-400 font-mono">{test.strand_code}</span></div>
      <h4 className="text-gray-800 font-semibold">{STRAND_SHORT_LABEL[test.strand_code]}</h4>
      <p className="text-xs text-gray-500 mt-1 mb-4">{test.title}</p>
      {done ? <div className="space-y-2">
        <div className="flex items-center gap-2 text-sm text-green-700 bg-green-50 py-2 px-3 rounded-lg"><CheckCircle2 className="w-4 h-4" /> Completed</div>
        <button onClick={onViewResult} className="w-full py-2 rounded-lg text-sm border border-[#3535C5] text-[#3535C5] hover:bg-indigo-50">View result</button>
      </div> : <button onClick={onAttempt} disabled={!intakeComplete} className="w-full py-2 rounded-lg text-sm bg-[#3535C5] text-white hover:bg-[#2929a8] disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed">{intakeComplete ? "Attempt test" : "Locked until Part I"}</button>}
    </div>
  </article>;
}
