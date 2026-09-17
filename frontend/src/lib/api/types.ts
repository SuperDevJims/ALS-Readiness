// Auth domain types. Confirmed against backend source (2026-09-17), not assumed:
//   - app/api/routes/auth.py, app/schemas/auth.py, app/schemas/user.py
//   - app/api/routes/users.py, app/schemas/user_profile.py
//   - app/main.py (exception -> status code mapping)
//
// Phase 3 additions, confirmed live against the running backend (2026-09-17):
//   - PATCH /api/users/me accepts exactly UserProfileUpdate's fields below (all
//     optional) - confirmed by sending id_no/role in the same request and
//     observing they're silently ignored (not persisted, not errored).
//   - PATCH /api/users/me/password: wrong current password -> 400 (not 401),
//     code INCORRECT_CURRENT_PASSWORD; password reuse -> 400, code
//     PASSWORD_REUSE; new_password too short -> 422 REQUEST_VALIDATION with a
//     pydantic-style details array. Success -> 200 with UserResponse (NOT
//     nested under `profile` - this endpoint's response has no profile field).

export type Role = "learner" | "facilitator" | "admin";

/** POST /api/auth/login is submitted as x-www-form-urlencoded (OAuth2PasswordRequestForm) */
export interface LoginRequest {
  id_no: string;
  password: string;
}

/** Shared response shape for both POST /api/auth/login and POST /api/auth/refresh */
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export type LoginResponse = TokenResponse;

/** POST /api/auth/refresh returns only a new access token (TokenResponse) -
 *  the rotated refresh token is set as an httpOnly cookie, never in the body. */
export type RefreshResponse = TokenResponse;

export interface UserProfile {
  first_name: string;
  last_name: string;
  middle_name: string | null;
  birthdate: string | null;
  gender: string | null;
  address: string | null;
  contact_number: string | null;
  contact_email: string | null;
}

export interface User {
  id: number;
  id_no: string;
  role: Role;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

/** GET /api/users/me response shape */
export interface UserMe extends User {
  profile: UserProfile;
}

export type Gender = "male" | "female" | "other";

/** PATCH /api/users/me body - every field optional, only these are accepted. */
export interface UserProfileUpdate {
  first_name?: string | null;
  last_name?: string | null;
  middle_name?: string | null;
  birthdate?: string | null;
  gender?: Gender | null;
  address?: string | null;
  contact_number?: string | null;
  contact_email?: string | null;
}

/** PATCH /api/users/me/password body */
export interface PasswordChangeRequest {
  current_password: string;
  new_password: string;
}


export interface AdminUserListItem {
  id: number;
  id_no: string | null;
  role: Role;
  is_active: boolean;
  first_name: string | null;
  last_name: string | null;
  created_at: string;
}

export interface AdminUserListResponse {
  items: AdminUserListItem[];
  total: number;
  page: number;
  page_size: number;
}

/** Identical body shape for POST /api/admin/{learners,facilitators,admins} */
export interface AdminUserCreate {
  first_name: string;
  last_name: string;
  middle_name?: string | null;
  birthdate?: string | null;
  gender?: Gender | null;
  address?: string | null;
  contact_number?: string | null;
  contact_email?: string | null;
}

export interface AdminUserCreateResponse {
  user_id: number;
  id_no: string;
  password: string;
  role: Role;
  is_active: boolean;
  profile: UserProfile;
  created_at: string;
  updated_at: string;
}

/** PATCH /api/admin/users/{id}/password body - just the new password, admin-set */
export interface AdminPasswordResetRequest {
  password: string;
}

/** Shape of app/schemas/error.py's ErrorResponse, returned by every handled exception */
export interface ApiErrorResponse {
  success: false;
  code: string;
  message: string;
  details?: unknown;
}

/**
 * Confirmed status codes from app/main.py's exception handlers - not assumed:
 *   NotFoundError            -> 404
 *   UnauthenticatedError     -> 401
 *   UnauthorizedError        -> 403
 *   AlreadyExistsError       -> 409  (matches design intent)
 *   DomainValidationError    -> 400  (matches design intent)
 *   RequestValidationError / PydanticValidationError -> 422
 */
export const API_STATUS = {
  UNAUTHENTICATED: 401,
  UNAUTHORIZED: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  VALIDATION: 400,
  UNPROCESSABLE: 422,
} as const;
