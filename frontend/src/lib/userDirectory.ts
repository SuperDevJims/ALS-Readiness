import { listUsers } from "./api/admin";
import type { AdminUserListItem, Role } from "./api/types";

// GET /api/admin/users has no search parameter and returns at most 100 users
// a page, so finding a person by name or ID number means reading every page
// for the role and searching the result in the browser.

/** The largest page the API serves. */
const PAGE_SIZE = 100;
/** A ceiling on how much is read, so a very large user list cannot run away: 3,000 users. */
const MAX_PAGES = 30;

export interface UserDirectory {
  users: AdminUserListItem[];
  /** How many users of the role the API says exist. */
  total: number;
  /** False when the ceiling was reached before every user was read; a search then covers only `users`. */
  complete: boolean;
}

/** Every user of a role, read page by page through the admin users list. */
export async function loadUserDirectory(role: Role): Promise<UserDirectory> {
  const users: AdminUserListItem[] = [];
  let total = 0;
  for (let page = 1; page <= MAX_PAGES; page++) {
    const response = await listUsers({ page, page_size: PAGE_SIZE, role });
    total = response.total;
    users.push(...response.items);
    if (response.items.length === 0 || users.length >= total) break;
  }
  return { users, total, complete: users.length >= total };
}

/** ID numbers by user id, for rows that carry a user id but no ID number. */
export function idNumbersByUserId(users: readonly Pick<AdminUserListItem, "id" | "id_no">[]): Map<number, string | null> {
  return new Map(users.map((user) => [user.id, user.id_no]));
}
