import { useEffect, useState } from "react";
import { BookOpen, Calculator, CheckCircle2, ChevronLeft, ChevronRight, ClipboardList, FileText, LoaderCircle, LockKeyhole, Star } from "lucide-react";
import { AppLayout } from "../shared/AppLayout";
import { ImageWithFallback } from "../figma/ImageWithFallback";

const API_ROOT = import.meta.env.VITE_API_URL || "/api";
const INTAKE_STORAGE_KEY = "alsense_demo_participant_intake";
const DEMO_LRI_COMPLETE_KEY = "alsense_demo_lri_complete";
const LIKERT_OPTIONS = [
  { label: "Strongly Disagree", value: 1 },
  { label: "Disagree", value: 2 },
  { label: "Agree", value: 3 },
  { label: "Strongly Agree", value: 4 },
];
const demoLri = {
  test_id: "demo-lri",
  title: "Learner Readiness Inventory",
  image_url: "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1200&q=80",
  items: Array.from({ length: 10 }, (_, index) => ({ item_id: `lri-${index + 1}`, question_text: `I feel ready to participate actively in my ALS learning activities. (Statement ${index + 1})` })),
};
const demoTests = [
  { test_id: "demo-english", title: "English baseline diagnostic", image_url: "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80", strand_code: "LS1", strand_name: "English" },
  { test_id: "demo-filipino", title: "Filipino baseline diagnostic", image_url: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80", strand_code: "LS1", strand_name: "Filipino" },
  { test_id: "demo-mathematics", title: "Mathematics baseline diagnostic", image_url: "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80", strand_code: "LS3", strand_name: "Mathematics" },
];
const demoQuestions = [
  { item_id: "question-1", question_text: "This is a demo diagnostic question. Choose the response that best answers the question.", options: ["Option A", "Option B", "Option C", "Option D"].map((option_text, index) => ({ option_id: `option-${index + 1}`, option_text })) },
  { item_id: "question-2", question_text: "This is the second demo question for the selected learning strand.", options: ["Option A", "Option B", "Option C", "Option D"].map((option_text, index) => ({ option_id: `option-2-${index + 1}`, option_text })) },
];
const strandStyles = {
  English: { icon: BookOpen, tone: "blue" },
  Filipino: { icon: FileText, tone: "rose" },
  Mathematics: { icon: Calculator, tone: "violet" },
};
const toneClasses = {
  blue: "bg-blue-50 text-blue-600 border-blue-100", rose: "bg-rose-50 text-rose-600 border-rose-100", violet: "bg-violet-50 text-violet-600 border-violet-100",
};

async function api(path, options) {
  const accessToken = localStorage.getItem("alsense_access_token");
  const response = await fetch(`${API_ROOT}${path}`, { credentials: "include", headers: { "Content-Type": "application/json", ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}) }, ...options });
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new Error(data?.message || `Request failed (${response.status})`);
  }
  const contentLength = response.headers.get("content-length");
  return response.status === 204 || contentLength === "0" ? null : response.json();
}

function PretestLoadingIndicator() {
  return (
    <div className="py-12 flex justify-center">
      <LoaderCircle className="w-6 h-6 text-[#3535C5] animate-spin" />
    </div>
  );
}

export function DiagnosticTest({ navigate, user, onLogout }) {
  const [lri, setLri] = useState(null);
  const [tests, setTests] = useState([]);
  const [intakeComplete, setIntakeComplete] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [view, setView] = useState("hub");
  const [activeTest, setActiveTest] = useState(null);
  const [demoMode, setDemoMode] = useState(false);

  const loadHub = async () => {
    setLoading(true); setError("");
    try {
      const [lriData, strandData] = await Promise.all([api("/learner/lri-tests"), api("/learner/strand-tests?test_type=pretest")]);
      setLri(lriData); setTests((strandData?.tests || []).filter((test) => ["English", "Filipino", "Mathematics"].includes(test.strand_name))); setIntakeComplete(Boolean(sessionStorage.getItem(INTAKE_STORAGE_KEY)));
    } catch {
      setDemoMode(true);
      setLri({ ...demoLri, attempt_status: sessionStorage.getItem(DEMO_LRI_COMPLETE_KEY) ? "completed" : "pending" });
      setTests(demoTests.map((test) => ({ ...test, attempt_status: sessionStorage.getItem(`alsense_${test.test_id}_complete`) ? "completed" : "pending" })));
      setIntakeComplete(Boolean(sessionStorage.getItem(INTAKE_STORAGE_KEY)));
    }
    finally { setLoading(false); }
  };
  useEffect(() => { loadHub(); }, []);

  const completed = tests.filter((test) => test.attempt_status === "completed");
  const allComplete = tests.length === 3 && completed.length === 3 && lri?.attempt_status === "completed";
  const openLri = async () => {
    if (demoMode) { setActiveTest(demoLri); setView("lri"); return; }
    try { setLoading(true); const data = await api(`/learner/lri-tests/${lri.test_id}`); setActiveTest(data); setView("lri"); }
    catch { setError("The Learner Readiness Inventory could not be opened."); }
    finally { setLoading(false); }
  };
  const openStrand = async (test) => {
    if (demoMode) { setActiveTest({ ...test, items: demoQuestions }); setView("strand"); return; }
    try { setLoading(true); const data = await api(`/learner/strand-tests/${test.test_id}?include_items=true`); setActiveTest({ ...data, strand_name: test.strand_name, strand_code: test.strand_code }); setView("strand"); }
    catch { setError("This diagnostic test could not be opened."); }
    finally { setLoading(false); }
  };

  if (view === "lri") return <LriAttempt test={activeTest} demoMode={demoMode} onClose={() => { setView("hub"); loadHub(); }} />;
  if (view === "strand") return <StrandAttempt test={activeTest} demoMode={demoMode} onClose={() => { setView("hub"); loadHub(); }} />;

  return <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage="diagnostic-test">
    <main className="p-6 max-w-6xl mx-auto w-full">
      <section className="bg-gradient-to-r from-[#182f68] to-[#3535C5] rounded-2xl p-7 text-white mb-6">
        <p className="text-blue-200 text-xs font-semibold uppercase tracking-[0.16em] mb-2">Baseline assessment · No EEG device</p>
        <h2 className="text-2xl font-bold mb-2">Pre-test</h2>
        <p className="text-blue-100 text-sm max-w-2xl leading-relaxed">Complete the participant intake, Learner Readiness Inventory, and three diagnostic exams to establish your baseline.</p>
      </section>

      <div className="grid gap-4 md:grid-cols-3 mb-6">
        <Stat icon={ClipboardList} label="Diagnostic tests" value={`${completed.length}/3`} />
        <Stat icon={CheckCircle2} label="LRI status" value={lri?.attempt_status === "completed" ? "Complete" : "Pending"} />
        <Stat icon={Star} label="Pre-test status" value={allComplete ? "Complete" : "In progress"} />
      </div>

      {error && <div className="mb-5 flex items-center justify-between gap-4 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl text-sm"><span>{error}</span><button onClick={loadHub} className="font-semibold underline">Try again</button></div>}
      {demoMode && <div className="mb-5 bg-blue-50 border border-blue-200 text-blue-800 p-4 rounded-xl text-sm">Demo mode is active. Pre-test responses are stored only for this browser session and are not sent to the database.</div>}
      {loading ? <PretestLoadingIndicator /> : <div className="space-y-5">
        <PartCard number="Part I" title="Participant intake" description="Background questionnaire required before all assessment activities." status={intakeComplete ? "Completed" : "Required"} action={intakeComplete ? "Review intake" : "Complete intake"} onClick={() => navigate("participant-intake")} />
        <PartCard number="Part II" title="Learner Readiness Inventory" imageUrl={lri?.image_url} description="10 required statements using a four-point agreement scale." status={lri?.attempt_status === "completed" ? "Completed" : intakeComplete ? "Ready to attempt" : "Locked until Part I"} disabled={!intakeComplete || lri?.attempt_status === "completed"} action={lri?.attempt_status === "completed" ? "Completed" : "Attempt LRI"} onClick={openLri} />
        <section className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between mb-5">
            <div><p className="text-xs font-bold text-[#3535C5] uppercase tracking-wider mb-1">Part III</p><h3 className="text-gray-800 font-bold text-lg">Diagnostic / Equivalency Exams</h3><p className="text-gray-500 text-sm mt-1">One baseline exam for each enrolled learning strand. Completed pre-tests cannot be retaken.</p></div>
            <span className={`inline-flex items-center gap-1.5 self-start px-3 py-1.5 rounded-full text-xs font-medium ${intakeComplete ? "bg-green-50 text-green-700" : "bg-gray-100 text-gray-500"}`}><LockKeyhole className="w-3.5 h-3.5" /> {intakeComplete ? "Part I complete" : "Complete Part I first"}</span>
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            {tests.map((test) => <StrandCard key={test.test_id} test={test} intakeComplete={intakeComplete} onClick={() => openStrand(test)} />)}
            {!tests.length && <p className="text-sm text-gray-500">No pre-test strands are currently available.</p>}
          </div>
        </section>
      </div>}
    </main>
  </AppLayout>;
}

function Stat({ icon: Icon, label, value }) { return <div className="bg-white rounded-2xl border border-gray-100 p-4 flex items-center gap-3"><div className="w-10 h-10 bg-indigo-50 text-[#3535C5] rounded-xl flex items-center justify-center"><Icon className="w-5 h-5" /></div><div><p className="text-lg font-bold text-gray-800">{value}</p><p className="text-xs text-gray-500">{label}</p></div></div>; }
function PartCard({ number, title, imageUrl, description, status, action, onClick, disabled }) { return <section className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row gap-5 sm:items-center sm:justify-between">{imageUrl && <ImageWithFallback src={imageUrl} alt="" className="h-24 w-full sm:w-36 object-cover rounded-xl" />}<div className="flex-1"><p className="text-xs font-bold text-[#3535C5] uppercase tracking-wider mb-1">{number}</p><h3 className="text-gray-800 font-bold text-lg">{title}</h3><p className="text-gray-500 text-sm mt-1">{description}</p></div><div className="flex flex-col sm:items-end gap-2 shrink-0"><span className={`text-xs font-medium px-2.5 py-1 rounded-full ${disabled ? "bg-amber-50 text-amber-700" : "bg-blue-50 text-blue-700"}`}>{status}</span><button onClick={onClick} disabled={disabled} className="px-4 py-2.5 rounded-xl text-sm font-medium bg-[#3535C5] text-white hover:bg-[#2929a8] disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed">{action}</button></div></section>; }
function StrandCard({ test, intakeComplete, onClick }) { const setting = strandStyles[test.strand_name] || strandStyles.English; const Icon = setting.icon; const done = test.attempt_status === "completed"; return <article className="overflow-hidden rounded-xl border border-gray-100"><ImageWithFallback src={test.image_url} alt={`${test.strand_name} test`} className="h-28 w-full object-cover" /><div className="p-4"><div className="flex justify-between mb-4"><div className={`w-10 h-10 rounded-xl border flex items-center justify-center ${toneClasses[setting.tone]}`}><Icon className="w-5 h-5" /></div><span className="text-xs text-gray-400 font-mono">{test.strand_code}</span></div><h4 className="text-gray-800 font-semibold">{test.strand_name}</h4><p className="text-xs text-gray-500 mt-1 mb-4">{test.title}</p>{done ? <div className="flex items-center gap-2 text-sm text-green-700 bg-green-50 py-2 px-3 rounded-lg"><CheckCircle2 className="w-4 h-4" /> Completed</div> : <button onClick={onClick} disabled={!intakeComplete} className="w-full py-2 rounded-lg text-sm bg-[#3535C5] text-white hover:bg-[#2929a8] disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed">{intakeComplete ? "Attempt test" : "Locked until Part I"}</button>}</div></article>; }

function LriAttempt({ test, demoMode, onClose }) {
  const [answers, setAnswers] = useState({});
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const complete = test.items?.length && Object.keys(answers).length === test.items.length;

  const submit = async () => {
    setSaving(true);
    try {
      if (demoMode) {
        sessionStorage.setItem(DEMO_LRI_COMPLETE_KEY, "true");
      } else {
        await api(`/learner/lri-tests/${test.test_id}/attempts`, {
          method: "POST",
          body: JSON.stringify({
            answers: test.items.map((item) => ({
              item_id: item.item_id,
              answer_value: answers[item.item_id],
            })),
          }),
        });
      }
      onClose();
    } catch {
      setMessage("Your LRI responses could not be submitted. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return <AttemptShell title={test.title} subtitle="Select one response for every statement." onClose={onClose}>
    {test.image_url && <ImageWithFallback src={test.image_url} alt="Learner Readiness Inventory" className="w-full h-40 object-cover rounded-xl mb-6" />}
    <div className="overflow-x-auto border border-slate-800 rounded-sm">
      <table className="w-full min-w-[700px] table-fixed border-collapse text-sm">
        <thead className="bg-[#244477] text-white">
          <tr>
            <th className="w-1/2 border border-slate-800 p-3 text-center font-semibold">Statement</th>
            {LIKERT_OPTIONS.map(({ label }) => <th key={label} className="w-[12.5%] border border-slate-800 p-2 text-center font-semibold leading-tight">{label}</th>)}
          </tr>
        </thead>
        <tbody>
          {test.items?.map((item, index) => <tr key={item.item_id} className="odd:bg-white even:bg-slate-50">
            <td className="border border-slate-800 p-3 text-gray-800 align-top"><span className="font-semibold mr-1">{index + 1}.</span>{item.question_text}</td>
            {LIKERT_OPTIONS.map(({ label, value }) => <td key={value} className="border border-slate-800 p-3 text-center">
              <input aria-label={`${item.question_text}: ${label}`} type="radio" name={`item-${item.item_id}`} value={value} checked={answers[item.item_id] === value} onChange={() => setAnswers((current) => ({ ...current, [item.item_id]: value }))} className="h-4 w-4 accent-[#244477]" />
            </td>)}
          </tr>)}
        </tbody>
      </table>
    </div>
    {message && <p className="text-red-600 text-sm mt-4">{message}</p>}
    <AttemptActions disabled={!complete || saving} saving={saving} onSubmit={submit} />
  </AttemptShell>;
}
function StrandAttempt({ test, demoMode, onClose }) { const [current, setCurrent] = useState(0); const [answers, setAnswers] = useState({}); const [saving, setSaving] = useState(false); const [message, setMessage] = useState(""); const item = test.items[current]; const complete = test.items?.length && Object.keys(answers).length === test.items.length; const submit = async () => { setSaving(true); try { if (demoMode) sessionStorage.setItem(`alsense_${test.test_id}_complete`, "true"); else await api(`/learner/strand-tests/${test.test_id}/attempts`, { method: "POST", body: JSON.stringify({ answers: test.items.map((question) => ({ item_id: question.item_id, option_id: answers[question.item_id] })) }) }); onClose(); } catch { setMessage("Your answers could not be submitted. Please try again."); } finally { setSaving(false); } }; return <AttemptShell title={`${test.strand_name} diagnostic exam`} subtitle={`Question ${current + 1} of ${test.items?.length || 0}`} onClose={onClose}>{item && <><div className="h-2 bg-gray-100 rounded-full mb-6"><div className="h-full bg-[#3535C5] rounded-full" style={{ width: `${((current + 1) / test.items.length) * 100}%` }} /></div><section className="border border-gray-100 rounded-2xl p-6"><p className="text-gray-800 text-lg font-medium leading-relaxed mb-6">{item.question_text}</p><div className="space-y-3">{item.options.map((option, index) => <button key={option.option_id} onClick={() => setAnswers((old) => ({ ...old, [item.item_id]: option.option_id }))} className={`w-full flex text-left gap-3 p-4 border rounded-xl transition-colors ${answers[item.item_id] === option.option_id ? "border-[#3535C5] bg-indigo-50 text-indigo-900" : "border-gray-200 hover:border-indigo-300 text-gray-700"}`}><span className="w-6 h-6 shrink-0 rounded-full border flex justify-center items-center text-xs font-semibold">{String.fromCharCode(65 + index)}</span>{option.option_text}</button>)}</div></section><div className="flex justify-between mt-5"><button onClick={() => setCurrent((number) => number - 1)} disabled={current === 0} className="inline-flex gap-1 items-center px-4 py-2 text-sm text-gray-600 disabled:text-gray-300"><ChevronLeft className="w-4 h-4" /> Previous</button>{current < test.items.length - 1 ? <button onClick={() => setCurrent((number) => number + 1)} className="inline-flex gap-1 items-center px-4 py-2 rounded-xl text-sm text-white bg-[#3535C5]">Next <ChevronRight className="w-4 h-4" /></button> : <span />}</div></>}{message && <p className="text-red-600 text-sm mt-4">{message}</p>}<AttemptActions disabled={!complete || saving} saving={saving} onSubmit={submit} /></AttemptShell>; }
function AttemptShell({ title, subtitle, onClose, children }) { return <div className="min-h-screen bg-[#F0F4F8] p-4 sm:p-8"><main className="max-w-4xl mx-auto"><button onClick={onClose} className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-[#3535C5] mb-5"><ChevronLeft className="w-4 h-4" /> Back to pre-test</button><div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm"><h1 className="text-xl font-bold text-gray-800">{title}</h1><p className="text-sm text-gray-500 mt-1 mb-6">{subtitle}</p>{children}</div></main></div>; }
function AttemptActions({ disabled, saving, onSubmit }) { return <div className="border-t border-gray-100 pt-5 mt-6 flex justify-end"><button onClick={onSubmit} disabled={disabled} className="px-5 py-2.5 bg-[#3535C5] hover:bg-[#2929a8] text-white rounded-xl text-sm font-medium disabled:bg-gray-200 disabled:text-gray-400">{saving ? "Submitting…" : "Submit baseline responses"}</button></div>; }
