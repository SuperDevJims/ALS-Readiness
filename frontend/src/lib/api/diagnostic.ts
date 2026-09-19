import { apiClient } from "./client";
import type {
  AttemptSubmissionResponse,
  LriAttemptCreate,
  LriAttemptResult,
  LriTestListResponse,
  LriTestWithItems,
  ParticipantIntake,
  ParticipantIntakeUpsert,
  StrandAttemptCreate,
  StrandAttemptResult,
  StrandCode,
  StrandTestListResponse,
  StrandTestType,
  StrandTestWithItems,
} from "./types";

// M02 diagnostic API: strand pretest/posttest, LRI, participant intake.
// Built on the shared apiClient, so auth headers, silent refresh on 401 and the
// 403 redirect all come from client.ts - nothing auth-related belongs here.
//
// Failures reject with the axios error; read them with lib/api/errors.ts
// (getErrorCode / getErrorMessage / isAttemptAlreadySubmitted / isPretestRequired /
// isAttemptNotFound). Notably, GET .../attempts rejects with a 404 when the
// learner hasn't attempted the test - that's "no result yet", not a failure.

export const STRAND_CODES: readonly StrandCode[] = ["LS1-EN", "LS1-FIL", "LS3"];

/** Short display labels, keyed by strand_code (for UI copy only - not for matching). */
export const STRAND_SHORT_LABEL: Record<StrandCode, string> = {
  "LS1-EN": "English",
  "LS1-FIL": "Filipino",
  "LS3": "Mathematics",
};

export function isStrandCode(value: string): value is StrandCode {
  return (STRAND_CODES as readonly string[]).includes(value);
}

/**
 * Index items by their `strand_code`. Items with a code outside STRAND_CODES
 * are skipped, so a screen only ever renders in-scope strands.
 */
export function indexByStrandCode<T extends { strand_code: string }>(
  items: readonly T[],
): Partial<Record<StrandCode, T>> {
  const index: Partial<Record<StrandCode, T>> = {};
  for (const item of items) {
    if (isStrandCode(item.strand_code)) {
      index[item.strand_code] = item;
    }
  }
  return index;
}

// ── Strand tests ─────────────────────────────────────────────────────────────

/** GET /api/learner/strand-tests?test_type=... - one entry per strand, with the learner's attempt_status. */
export async function getStrandTests(testType: StrandTestType): Promise<StrandTestListResponse> {
  const res = await apiClient.get<StrandTestListResponse>("/api/learner/strand-tests", {
    params: { test_type: testType },
  });
  return res.data;
}

/** GET /api/learner/strand-tests/{test_id}?include_items=true - items with options; correct answers are never sent. */
export async function getStrandTestWithItems(testId: number): Promise<StrandTestWithItems> {
  const res = await apiClient.get<StrandTestWithItems>(`/api/learner/strand-tests/${testId}`, {
    params: { include_items: true },
  });
  return res.data;
}

/**
 * POST /api/learner/strand-tests/{test_id}/attempts - 201.
 * One attempt per test (409 STRAND_TEST_ATTEMPT_ALREADY_EXISTS on a repeat) and a
 * posttest needs the same strand's pretest first (400 PRETEST_REQUIRED).
 */
export async function submitStrandAttempt(
  testId: number,
  data: StrandAttemptCreate,
): Promise<AttemptSubmissionResponse> {
  const res = await apiClient.post<AttemptSubmissionResponse>(
    `/api/learner/strand-tests/${testId}/attempts`,
    data,
  );
  return res.data;
}

/** GET /api/learner/strand-tests/{test_id}/attempts - the caller's own result, with MPS. 404 if unattempted. */
export async function getStrandAttemptResult(testId: number): Promise<StrandAttemptResult> {
  const res = await apiClient.get<StrandAttemptResult>(`/api/learner/strand-tests/${testId}/attempts`);
  return res.data;
}

// ── LRI ──────────────────────────────────────────────────────────────────────

/** GET /api/learner/lri-tests - `{tests: [...]}` envelope, one entry per LRI test. */
export async function getLriTests(): Promise<LriTestListResponse> {
  const res = await apiClient.get<LriTestListResponse>("/api/learner/lri-tests");
  return res.data;
}

/**
 * GET /api/learner/lri-tests/{test_id} - always includes items. (The backend has
 * no include_items switch for LRI - a `?include_items=true` would be ignored - so
 * none is sent.)
 */
export async function getLriTestWithItems(testId: number): Promise<LriTestWithItems> {
  const res = await apiClient.get<LriTestWithItems>(`/api/learner/lri-tests/${testId}`);
  return res.data;
}

/** POST /api/learner/lri-tests/{test_id}/attempts - 201. One attempt per test (409 LRI_TEST_ATTEMPT_ALREADY_EXISTS). */
export async function submitLriAttempt(
  testId: number,
  data: LriAttemptCreate,
): Promise<AttemptSubmissionResponse> {
  const res = await apiClient.post<AttemptSubmissionResponse>(
    `/api/learner/lri-tests/${testId}/attempts`,
    data,
  );
  return res.data;
}

/** GET /api/learner/lri-tests/{test_id}/attempts - the caller's own result (lri_score). 404 if unattempted. */
export async function getLriAttemptResult(testId: number): Promise<LriAttemptResult> {
  const res = await apiClient.get<LriAttemptResult>(`/api/learner/lri-tests/${testId}/attempts`);
  return res.data;
}

// ── Participant intake ───────────────────────────────────────────────────────

const INTAKE_PATH = "/api/learner/participant-intake";

/** GET - null (not a 404) until the learner has submitted their intake. */
export async function getParticipantIntake(): Promise<ParticipantIntake | null> {
  const res = await apiClient.get<ParticipantIntake | null>(INTAKE_PATH);
  return res.data;
}

/** POST - creates the intake, or updates it if one exists (an upsert; 200 either way). */
export async function submitParticipantIntake(data: ParticipantIntakeUpsert): Promise<ParticipantIntake> {
  const res = await apiClient.post<ParticipantIntake>(INTAKE_PATH, data);
  return res.data;
}

/** PUT - same upsert as POST; `submitted_at` keeps the original submission time. */
export async function updateParticipantIntake(data: ParticipantIntakeUpsert): Promise<ParticipantIntake> {
  const res = await apiClient.put<ParticipantIntake>(INTAKE_PATH, data);
  return res.data;
}
