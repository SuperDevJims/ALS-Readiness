import { useEffect, useState } from "react";
import { CheckCircle2, LoaderCircle, LockKeyhole } from "lucide-react";
import { AppLayout } from "../shared/AppLayout";
import { STRAND_CODES, getStrandTests, indexByStrandCode } from "../../../lib/api/diagnostic";
import { getErrorMessage } from "../../../lib/api/errors";
import type { StrandTestListItem } from "../../../lib/api/types";
import { StrandAttempt } from "../diagnostic/PretestAttempts";
import { StrandTestCard } from "../diagnostic/StrandTestCard";

// Post-test hub: one real diagnostic exam per in-scope strand (LS1-EN, LS1-FIL,
// LS3 - no Science/AP, those were never in scope). Reuses Phase 2's overview
// modal, countdown and shuffle utilities via StrandAttempt directly, rather
// than reimplementing any of them - a posttest attempt is just a strand-test
// attempt against `test_type=posttest` tests, same as pretest is for
// `test_type=pretest`. No score is fetched or shown here, and a strand whose
// pretest isn't done yet isn't offered - the backend rejects that
// (PRETEST_REQUIRED) but the UI shouldn't let a learner walk into it.

type View = { name: "hub" } | { name: "strand-attempt"; test: StrandTestListItem };

function PostTestLoadingIndicator() {
  return (
    <div className="py-12 flex justify-center">
      <LoaderCircle className="w-6 h-6 text-[#3535C5] animate-spin" />
    </div>
  );
}

export function PostTest({ navigate, user, onLogout }) {
  const learnerId: string | number = user?.raw?.id ?? user?.id_no ?? "anonymous";
  const [postTests, setPostTests] = useState<StrandTestListItem[]>([]);
  const [pretestDoneByCode, setPretestDoneByCode] = useState<Partial<Record<string, boolean>>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [view, setView] = useState<View>({ name: "hub" });

  const loadHub = async () => {
    setLoading(true); setError("");
    try {
      const [postData, preData] = await Promise.all([getStrandTests("posttest"), getStrandTests("pretest")]);
      setPostTests(postData.tests);
      const preDone: Partial<Record<string, boolean>> = {};
      for (const test of preData.tests) preDone[test.strand_code] = test.attempt_status === "completed";
      setPretestDoneByCode(preDone);
    } catch (err) {
      setError(getErrorMessage(err, "The post-test could not be loaded. Please try again."));
    } finally { setLoading(false); }
  };
  useEffect(() => { loadHub(); }, []);

  const backToHub = () => { setView({ name: "hub" }); loadHub(); };

  if (view.name === "strand-attempt") return <StrandAttempt test={view.test} learnerId={learnerId} onClose={backToHub} backLabel="Back to post-test" />;

  // Strands are identified by strand_code, never by name; unknown codes are skipped.
  const byCode = indexByStrandCode(postTests);
  const strands = STRAND_CODES.map((code) => byCode[code]).filter((test): test is StrandTestListItem => Boolean(test));
  const completedStrands = strands.filter((test) => test.attempt_status === "completed");
  const allComplete = strands.length > 0 && completedStrands.length === strands.length;

  return <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage="post-test">
    <main className="p-6 max-w-6xl mx-auto w-full">
      <section className="bg-gradient-to-r from-orange-600 to-amber-600 rounded-2xl p-7 text-white mb-6">
        <p className="text-orange-100 text-xs font-semibold uppercase tracking-[0.16em] mb-2">After stimulus content</p>
        <h2 className="text-2xl font-bold mb-2">Post-test</h2>
        <p className="text-orange-100 text-sm max-w-2xl leading-relaxed">Complete one post-test for each learning strand you've studied. Each strand needs its pre-test done first.</p>
      </section>

      {loading ? <PostTestLoadingIndicator /> : error ? (
        <div role="alert" className="flex items-center justify-between gap-4 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl text-sm">
          <span>{error}</span><button onClick={loadHub} className="font-semibold underline shrink-0">Try again</button>
        </div>
      ) : <>
        <section className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between mb-5">
            <div>
              <h3 className="text-gray-800 font-bold text-lg">Diagnostic / Equivalency Exams</h3>
              <p className="text-gray-500 text-sm mt-1">One post-test for each enrolled learning strand. Completed post-tests cannot be retaken.</p>
            </div>
            {allComplete && strands.length > 0 && (
              <span className="inline-flex items-center gap-1.5 self-start px-3 py-1.5 rounded-full text-xs font-medium bg-green-50 text-green-700"><LockKeyhole className="w-3.5 h-3.5" /> All post-tests complete</span>
            )}
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            {strands.map((test) => (
              <StrandTestCard
                key={test.test_id}
                test={test}
                canAttempt={Boolean(pretestDoneByCode[test.strand_code])}
                disabledReason="Complete the pretest for this strand first"
                attemptLabel="Start post-test"
                onAttempt={() => setView({ name: "strand-attempt", test })}
              />
            ))}
            {!strands.length && <p className="text-sm text-gray-500">No post-test strands are currently available.</p>}
          </div>
        </section>

        {allComplete && strands.length > 0 && (
          <div className="mt-6 bg-green-50 border border-green-200 rounded-2xl p-5 flex items-center gap-4">
            <CheckCircle2 className="w-8 h-8 text-green-500 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-green-800 font-bold">All post-tests complete!</h3>
              <p className="text-green-700 text-sm">You've completed the full diagnostic-to-delivery pipeline.</p>
            </div>
            <button onClick={() => navigate("my-progress")} className="px-5 py-2.5 bg-green-600 hover:bg-green-700 text-white rounded-xl text-sm font-medium transition-colors">View Progress</button>
          </div>
        )}
      </>}
    </main>
  </AppLayout>;
}
