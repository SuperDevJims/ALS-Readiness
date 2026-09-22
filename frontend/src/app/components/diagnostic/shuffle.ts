// Deterministic per-(learner, test) shuffle, shared by pretest (this phase) and
// posttest (Phase 3). Posttest reuses a pretest's item set, so a fixed order
// would let a learner answer from positional memory - this makes the order
// stable for a given learner+test (safe to reload mid-attempt) but different
// across learners and across different test_ids for the same learner.

/** Small string hash (djb2 variant) - good enough for seeding a PRNG, not for anything cryptographic. */
function hashString(input: string): number {
  let hash = 5381;
  for (let i = 0; i < input.length; i++) {
    hash = ((hash << 5) + hash + input.charCodeAt(i)) | 0;
  }
  return hash >>> 0;
}

/** mulberry32: a small, fast, deterministic PRNG from a 32-bit seed. */
function mulberry32(seed: number): () => number {
  let t = seed >>> 0;
  return () => {
    t = (t + 0x6d2b79f5) | 0;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Fisher-Yates shuffle of `items`, seeded from `(learnerId, testId)`. Same
 * learner + same test always produces the same order; a different learner or
 * a different test_id naturally produces a different one.
 */
export function shuffleForLearner<T>(items: readonly T[], learnerId: string | number, testId: number): T[] {
  const rng = mulberry32(hashString(`${learnerId}:${testId}`));
  const result = items.slice();
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}
