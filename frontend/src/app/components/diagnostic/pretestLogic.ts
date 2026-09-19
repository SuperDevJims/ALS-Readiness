import type {
  LriAnswerValue,
  LriAttemptCreate,
  LriTestItem,
  StrandAttemptCreate,
  StrandTestItem,
} from "../../../lib/api/types";

// Pure logic for the pretest screens (answer payloads, date display), kept free
// of React so it can be exercised on its own.

/** Four-point agreement scale used by the LRI. */
export const LIKERT_OPTIONS: readonly { label: string; value: LriAnswerValue }[] = [
  { label: "Strongly Disagree", value: 1 },
  { label: "Disagree", value: 2 },
  { label: "Agree", value: 3 },
  { label: "Strongly Agree", value: 4 },
];

/** True once every item has an answer. */
export function isComplete(items: readonly { item_id: number }[], answers: Record<number, unknown>): boolean {
  return items.length > 0 && items.every((item) => answers[item.item_id] !== undefined);
}

/**
 * Strand submission body: one `{item_id, option_id}` per item, in item order.
 * Throws rather than send a partial submission (the server rejects those anyway).
 */
export function toStrandAttemptCreate(
  items: readonly StrandTestItem[],
  answers: Record<number, number>,
): StrandAttemptCreate {
  return {
    answers: items.map((item) => {
      const option_id = answers[item.item_id];
      if (option_id === undefined) throw new Error(`Question ${item.item_id} is unanswered`);
      return { item_id: item.item_id, option_id };
    }),
  };
}

/** LRI submission body: one `{item_id, answer_value}` per statement, in item order. */
export function toLriAttemptCreate(
  items: readonly LriTestItem[],
  answers: Record<number, LriAnswerValue>,
): LriAttemptCreate {
  return {
    answers: items.map((item) => {
      const answer_value = answers[item.item_id];
      if (answer_value === undefined) throw new Error(`Statement ${item.item_id} is unanswered`);
      return { item_id: item.item_id, answer_value };
    }),
  };
}

/**
 * Display a backend timestamp. The API sends UTC datetimes without a zone suffix
 * (e.g. "2026-09-19T00:45:12.255363"), which `new Date()` would read as local
 * time - so a "Z" is added when no zone is present.
 */
export function formatWhen(iso: string | null): string {
  if (!iso) return "";
  const hasZone = /(Z|[+-]\d{2}:?\d{2})$/i.test(iso);
  const date = new Date(hasZone ? iso : `${iso}Z`);
  return Number.isNaN(date.getTime()) ? "" : date.toLocaleString();
}
