import { useEffect, useState } from "react";
import { AlertCircle, ArrowLeft, CheckCircle2, ClipboardCheck, LoaderCircle } from "lucide-react";
import { AppLayout } from "../shared/AppLayout";

const INTAKE_STORAGE_KEY = "alsense_demo_participant_intake";
const strandOptions = ["English (LS1)", "Filipino (LS1)", "Mathematics (LS3)"];
const inputClass = "w-full rounded-xl border border-gray-200 bg-white px-3 py-2.5 text-sm text-gray-800 outline-none transition focus:border-[#3535C5] focus:ring-2 focus:ring-[#3535C5]/15";
const initialForm = {
  age: "", sex: "", civil_status: "", highest_educational_attainment: "", als_learning_strands: [],
  als_enrollment_months: "", has_taken_ae_test: "", ae_test_attempt_count: "0",
};

export function ParticipantIntake({ navigate, user, onLogout }) {
  const [form, setForm] = useState(initialForm);
  const [existingIntake, setExistingIntake] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const loadIntake = async () => {
      try {
        const savedIntake = sessionStorage.getItem(INTAKE_STORAGE_KEY);
        if (savedIntake) {
          const intake = JSON.parse(savedIntake);
          setExistingIntake(true);
          setForm({
            ...intake,
            age: String(intake.age),
            als_enrollment_months: String(intake.als_enrollment_months),
            has_taken_ae_test: String(intake.has_taken_ae_test),
            ae_test_attempt_count: String(intake.ae_test_attempt_count),
          });
        }
      } catch { setError("The saved demo intake could not be read. Please complete the form again."); }
      finally { setLoading(false); }
    };
    loadIntake();
  }, []);

  const update = (field, value) => setForm((current) => ({ ...current, [field]: value }));
  const toggleStrand = (strand) => setForm((current) => ({
    ...current,
    als_learning_strands: current.als_learning_strands.includes(strand)
      ? current.als_learning_strands.filter((value) => value !== strand)
      : [...current.als_learning_strands, strand],
  }));
  const submit = async (event) => {
    event.preventDefault(); setSaving(true); setError(""); setMessage("");
    const payload = {
      ...form,
      age: Number(form.age),
      als_enrollment_months: Number(form.als_enrollment_months),
      has_taken_ae_test: form.has_taken_ae_test === "true",
      ae_test_attempt_count: Number(form.ae_test_attempt_count),
    };
    try {
      sessionStorage.setItem(INTAKE_STORAGE_KEY, JSON.stringify(payload));
      setExistingIntake(true);
      setMessage("Participant intake submitted for this demo session. You may now start Part II and Part III.");
    } catch { setError("Your intake could not be stored for this demo session. Please try again."); }
    finally { setSaving(false); }
  };

  return (
    <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage="participant-intake">
      <main className="p-6 max-w-3xl mx-auto w-full">
        <button onClick={() => navigate("diagnostic-test")} className="mb-5 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-[#3535C5]"><ArrowLeft className="w-4 h-4" /> Back to pre-test</button>
        <section className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm">
          <div className="bg-gradient-to-r from-[#182f68] to-[#3535C5] p-7 text-white">
            <div className="w-12 h-12 rounded-xl bg-white/15 flex items-center justify-center mb-4"><ClipboardCheck className="w-6 h-6" /></div>
            <p className="text-blue-200 text-xs font-semibold uppercase tracking-[0.16em] mb-2">Pre-test · Part I</p>
            <h2 className="text-2xl font-bold mb-2">Participant intake</h2>
            <p className="text-blue-100 text-sm leading-relaxed">Complete this background questionnaire once before beginning the Learner Readiness Inventory and diagnostic exams.</p>
          </div>

          {loading ? <div className="p-12 flex justify-center"><LoaderCircle className="w-6 h-6 text-[#3535C5] animate-spin" /></div> : <form onSubmit={submit} className="p-7 space-y-6">
            <div className="flex gap-3 p-4 rounded-xl border border-blue-100 bg-blue-50"><AlertCircle className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" /><p className="text-blue-900 text-sm">Demo mode: your responses stay only in this browser session and are not sent to the database. All fields are required.</p></div>
            {message && <div className="flex gap-2 p-4 rounded-xl bg-green-50 text-green-800 text-sm"><CheckCircle2 className="w-5 h-5 shrink-0" />{message}</div>}
            {error && <p className="p-4 rounded-xl bg-red-50 text-red-700 text-sm">{error}</p>}

            <div className="grid sm:grid-cols-3 gap-4">
              <Field label="Age"><input required min="15" max="120" type="number" value={form.age} onChange={(event) => update("age", event.target.value)} className={inputClass} /></Field>
              <Field label="Sex"><select required value={form.sex} onChange={(event) => update("sex", event.target.value)} className={inputClass}><option value="">Select</option><option value="male">Male</option><option value="female">Female</option><option value="other">Other</option></select></Field>
              <Field label="Civil status"><input required value={form.civil_status} onChange={(event) => update("civil_status", event.target.value)} className={inputClass} placeholder="e.g., Single" /></Field>
            </div>
            <Field label="Highest educational attainment prior to ALS"><input required value={form.highest_educational_attainment} onChange={(event) => update("highest_educational_attainment", event.target.value)} className={inputClass} placeholder="e.g., Grade 10" /></Field>
            <fieldset><legend className="text-sm font-medium text-gray-700 mb-2">ALS learning strand(s) currently enrolled in</legend><div className="grid sm:grid-cols-3 gap-3">{strandOptions.map((strand) => <label key={strand} className="flex items-center gap-2 p-3 rounded-xl border border-gray-200 text-sm text-gray-700 cursor-pointer"><input type="checkbox" checked={form.als_learning_strands.includes(strand)} onChange={() => toggleStrand(strand)} className="accent-[#3535C5]" />{strand}</label>)}</div></fieldset>
            <Field label="Length of time enrolled in ALS (months)"><input required min="0" max="1200" type="number" value={form.als_enrollment_months} onChange={(event) => update("als_enrollment_months", event.target.value)} className={inputClass} /></Field>
            <div className="grid sm:grid-cols-2 gap-4"><Field label="Have you taken the A&E test before?"><select required value={form.has_taken_ae_test} onChange={(event) => { update("has_taken_ae_test", event.target.value); if (event.target.value === "false") update("ae_test_attempt_count", "0"); }} className={inputClass}><option value="">Select</option><option value="true">Yes</option><option value="false">No</option></select></Field><Field label="Number of previous A&E attempts"><input required min={form.has_taken_ae_test === "true" ? "1" : "0"} max="100" disabled={form.has_taken_ae_test !== "true"} type="number" value={form.ae_test_attempt_count} onChange={(event) => update("ae_test_attempt_count", event.target.value)} className={`${inputClass} disabled:bg-gray-100`} /></Field></div>
            <div className="border-t border-gray-100 pt-5 flex justify-end"><button disabled={saving || form.als_learning_strands.length === 0} className="px-5 py-2.5 rounded-xl bg-[#3535C5] text-white hover:bg-[#2929a8] disabled:bg-gray-300 disabled:cursor-not-allowed text-sm font-medium">{saving ? "Saving…" : existingIntake ? "Update intake" : "Submit participant intake"}</button></div>
          </form>}
        </section>
      </main>
    </AppLayout>
  );
}

function Field({ label, children }) { return <label className="block text-sm font-medium text-gray-700">{label}<div className="mt-1.5">{children}</div></label>; }
