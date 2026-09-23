import { Navigate, useNavigate } from "react-router";
import { KeyRound, LogOut } from "lucide-react";
import { ALSenseLogo } from "../shared/ALSenseLogo";
import { ChangePasswordForm } from "../shared/ChangePasswordForm";
import { useAuthStore } from "../../../lib/store/authStore";
import { homeForRole, toPath } from "../../../lib/navigation";

/**
 * Forced password change. Registered in App.tsx as a plain route - NOT wrapped
 * in ProtectedPage, whose AppLayout (sidebar/nav) would give a flagged user
 * somewhere else to go. While the flag is set, the router's gate keeps every
 * other path redirecting here; the only way out is changing the password or
 * signing out.
 *
 * There's no explicit "success" navigation: the form's re-sync clears
 * mustChangePassword, which makes the check below send the user home.
 */
export function ChangePasswordPage() {
  const user = useAuthStore((s) => s.user);
  const role = useAuthStore((s) => s.role);
  const mustChangePassword = useAuthStore((s) => s.mustChangePassword);
  const navigate = useNavigate();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Nothing to change - also what releases the user after a successful change.
  if (!mustChangePassword) {
    return <Navigate to={toPath(homeForRole(role))} replace />;
  }

  const signOut = () => {
    useAuthStore.getState().logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-[#F5F7FA] flex flex-col items-center justify-center p-6">
      <div className="mb-10">
        <ALSenseLogo size="md" showSub subText="Empowering Adult Learners" />
      </div>
      <div className="bg-white rounded-2xl border border-gray-100 shadow-lg p-10 max-w-md w-full">
        <div className="w-16 h-16 bg-orange-50 rounded-2xl flex items-center justify-center mx-auto mb-5">
          <KeyRound className="w-8 h-8 text-orange-500" />
        </div>
        <h2 className="text-gray-800 mb-2 text-center" style={{ fontSize: "1.3rem", fontWeight: 700 }}>
          Change your password
        </h2>
        <p className="text-gray-500 text-sm leading-relaxed mb-6 text-center">
          Your password was reset by an administrator. Choose a new password to continue — your current password is
          the one you just signed in with.
        </p>

        <div className="flex justify-center">
          <ChangePasswordForm />
        </div>

        <button
          type="button"
          onClick={signOut}
          className="w-full mt-6 flex items-center justify-center gap-2 py-2.5 text-gray-500 hover:text-gray-700 text-sm transition-colors"
        >
          <LogOut className="w-4 h-4" />
          Sign out
        </button>
      </div>
    </div>
  );
}
