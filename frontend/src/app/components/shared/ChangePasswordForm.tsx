import { useState } from "react";
import { Lock } from "lucide-react";
import { Banner } from "./Banner";
import * as authApi from "../../../lib/api/auth";
import { getErrorCode, getErrorMessage } from "../../../lib/api/errors";
import { useAuthStore } from "../../../lib/store/authStore";

const DEFAULT_SUCCESS_TEXT =
  "Password changed. You're still signed in on this device — every other session has been signed out.";

/**
 * Current / new / confirm password form, shared by the profile page and the
 * forced-change page. On success it re-syncs the auth store, which is what
 * clears `mustChangePassword` (see below).
 */
export function ChangePasswordForm({ successText = DEFAULT_SUCCESS_TEXT }: { successText?: string }) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [pwSaving, setPwSaving] = useState(false);
  const [pwResult, setPwResult] = useState(null);

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setPwResult(null);

    if (!currentPassword || !newPassword || !confirmPassword) {
      setPwResult({ type: "error", text: "Please fill in all three password fields." });
      return;
    }
    if (newPassword !== confirmPassword) {
      setPwResult({ type: "error", text: "New password and confirmation don't match." });
      return;
    }

    setPwSaving(true);
    try {
      const changed = await authApi.changeMyPassword({ current_password: currentPassword, new_password: newPassword });

      // PATCH /me/password returns a bare User (no `profile`), which refreshUser
      // can't take - so re-fetch /me and feed that. This is what flips the
      // store's mustChangePassword to false; get it wrong and the router's gate
      // bounces the user straight back to the change-password page.
      try {
        useAuthStore.getState().refreshUser(await authApi.getMe());
      } catch {
        // The change itself succeeded (200) and the server has cleared the flag,
        // so don't strand the user behind a stale local copy of it.
        useAuthStore.getState().setMustChangePassword(changed.must_change_password);
      }

      setPwResult({ type: "success", text: successText });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      const code = getErrorCode(err);
      if (code === "INCORRECT_CURRENT_PASSWORD") {
        setPwResult({ type: "error", text: "Current password is incorrect." });
      } else if (code === "PASSWORD_REUSE") {
        setPwResult({ type: "error", text: "New password must be different from your current password." });
      } else {
        setPwResult({ type: "error", text: getErrorMessage(err, "Couldn't change your password.") });
      }
    } finally {
      setPwSaving(false);
    }
  };

  return (
    <form onSubmit={handleChangePassword} className="max-w-sm space-y-4">
      <Banner result={pwResult} />

      <div>
        <label className="text-gray-600 text-sm font-medium mb-1.5 block">Current Password</label>
        <input
          type="password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
        />
      </div>
      <div>
        <label className="text-gray-600 text-sm font-medium mb-1.5 block">New Password</label>
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
        />
      </div>
      <div>
        <label className="text-gray-600 text-sm font-medium mb-1.5 block">Confirm New Password</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
        />
      </div>

      <button
        type="submit"
        disabled={pwSaving}
        className="flex items-center gap-2 px-5 py-2.5 bg-[#1a3a6c] hover:bg-[#152e56] text-white rounded-xl text-sm font-medium transition-colors disabled:opacity-50"
      >
        <Lock className="w-4 h-4" />
        {pwSaving ? "Changing…" : "Change Password"}
      </button>
    </form>
  );
}
