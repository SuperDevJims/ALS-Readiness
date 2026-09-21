import { useEffect, useRef, useState } from "react";

// Frontend-only time limits, shared by pretest (this phase) and posttest
// (Phase 3). Nullable by design: a null limit means the test is untimed.
// There's no backend enforcement - the schema has no "attempt started at"
// timestamp to enforce against (only submission time is captured), which is
// a meaningfully larger backend addition than this phase's scope. This is a
// UI countdown only; it never blocks or auto-submits an attempt.

/** Strand diagnostic exams: 20 multiple-choice items. */
export const STRAND_TEST_TIME_LIMIT_SECONDS: number | null = 30 * 60;

/** Learner Readiness Inventory: 10 Likert statements. */
export const LRI_TEST_TIME_LIMIT_SECONDS: number | null = 15 * 60;

/** "12:34"; caps at 59:59 display-wise only if given a value under an hour (these limits are). */
export function formatCountdown(totalSeconds: number): string {
  const clamped = Math.max(0, totalSeconds);
  const minutes = Math.floor(clamped / 60);
  const seconds = clamped % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

/**
 * Ticks down from `limitSeconds` once per second, starting the moment this
 * hook is first mounted with a non-null limit (i.e. when the caller mounts
 * the in-progress test screen, after the overview modal's "Start").
 * `limitSeconds === null` means untimed - `secondsLeft` stays null and
 * `expired` stays false.
 */
export function useCountdown(limitSeconds: number | null): { secondsLeft: number | null; expired: boolean } {
  const [secondsLeft, setSecondsLeft] = useState<number | null>(limitSeconds);
  const startedAtRef = useRef(Date.now());

  useEffect(() => {
    if (limitSeconds === null) {
      setSecondsLeft(null);
      return;
    }
    startedAtRef.current = Date.now();
    setSecondsLeft(limitSeconds);

    const id = window.setInterval(() => {
      const elapsed = Math.floor((Date.now() - startedAtRef.current) / 1000);
      setSecondsLeft(Math.max(0, limitSeconds - elapsed));
    }, 1000);
    return () => window.clearInterval(id);
  }, [limitSeconds]);

  return { secondsLeft, expired: secondsLeft === 0 };
}
