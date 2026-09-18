// Shared helpers for reading the confirmed ApiErrorResponse shape
// ({success, code, message, details}) off a failed axios call. Centralized
// here so every form (this phase's profile/password, Phase 4's admin forms)
// handles errors the same way instead of re-deriving this per component.

interface PydanticDetail {
  msg?: string;
  loc?: unknown[];
}

function getResponseData(err: unknown): { code?: string; message?: string; details?: unknown } | undefined {
  return (err as { response?: { data?: unknown } })?.response?.data as
    | { code?: string; message?: string; details?: unknown }
    | undefined;
}

/** The error `code` field (e.g. "INCORRECT_CURRENT_PASSWORD", "PASSWORD_REUSE"), if present. */
export function getErrorCode(err: unknown): string | undefined {
  return getResponseData(err)?.code;
}

/**
 * A human-readable message for the failure - prefers the first pydantic
 * validation detail (422s) over the generic top-level `message`, since
 * "Request validation failed." on its own tells the user nothing.
 */
export function getErrorMessage(err: unknown, fallback = "Something went wrong. Please try again."): string {
  const data = getResponseData(err);
  if (!data) return fallback;

  if (Array.isArray(data.details) && data.details.length > 0) {
    const first = data.details[0] as PydanticDetail;
    if (first?.msg) return first.msg;
  }

  return data.message || fallback;
}
