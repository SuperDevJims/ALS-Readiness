import { Clock, LogIn } from "lucide-react";
import { useNavigate } from "react-router";
import { ALSenseLogo } from "./ALSenseLogo";

/** Reached only via the response interceptor's failed-silent-refresh path (Task 5). */
export function SessionExpired() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#F5F7FA] flex flex-col items-center justify-center p-6">
      <div className="mb-10">
        <ALSenseLogo size="md" showSub subText="Empowering Adult Learners" />
      </div>
      <div className="bg-white rounded-2xl border border-gray-100 shadow-lg p-10 max-w-md w-full text-center">
        <div className="w-16 h-16 bg-orange-50 rounded-2xl flex items-center justify-center mx-auto mb-5">
          <Clock className="w-8 h-8 text-orange-500" />
        </div>
        <h2 className="text-gray-800 mb-2" style={{ fontSize: "1.3rem", fontWeight: 700 }}>
          Session expired
        </h2>
        <p className="text-gray-500 text-sm leading-relaxed mb-6">
          Your session has ended. Sign in again to continue.
        </p>
        <button
          onClick={() => navigate("/login")}
          className="w-full flex items-center justify-center gap-2 py-3 bg-[#0B1F3A] hover:bg-[#152e56] text-white rounded-xl font-medium transition-colors"
        >
          <LogIn className="w-4 h-4" />
          Back to Sign In
        </button>
      </div>
    </div>
  );
}
