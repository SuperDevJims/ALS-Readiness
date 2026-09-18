import { apiClient } from "./client";
import type { PasswordChangeRequest, TokenResponse, User, UserMe, UserProfileUpdate } from "./types";

/** POST /api/auth/login - form-encoded (OAuth2PasswordRequestForm: username/password) */
export async function login(idNo: string, password: string): Promise<TokenResponse> {
  const form = new URLSearchParams();
  form.set("username", idNo);
  form.set("password", password);

  const res = await apiClient.post<TokenResponse>("/api/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
}

/** POST /api/auth/refresh - no body; refresh token is read from the httpOnly cookie */
export async function refresh(): Promise<TokenResponse> {
  const res = await apiClient.post<TokenResponse>("/api/auth/refresh");
  return res.data;
}

/** POST /api/auth/logout - 204 No Content */
export async function logout(): Promise<void> {
  await apiClient.post("/api/auth/logout");
}

/** GET /api/users/me */
export async function getMe(): Promise<UserMe> {
  const res = await apiClient.get<UserMe>("/api/users/me");
  return res.data;
}

/** PATCH /api/users/me - accepts only UserProfileUpdate's fields; id_no/role are read-only */
export async function updateMe(data: UserProfileUpdate): Promise<UserMe> {
  const res = await apiClient.patch<UserMe>("/api/users/me", data);
  return res.data;
}

/** PATCH /api/users/me/password - response has no `profile`, unlike GET/PATCH /me */
export async function changeMyPassword(data: PasswordChangeRequest): Promise<User> {
  const res = await apiClient.patch<User>("/api/users/me/password", data);
  return res.data;
}
