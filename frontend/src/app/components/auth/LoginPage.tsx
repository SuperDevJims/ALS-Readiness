import { useState } from "react";
import { Eye, EyeOff, User, Lock, ChevronLeft } from "lucide-react";
import { ALSenseLogo } from "../shared/ALSenseLogo";
import { useAuthStore } from "../../../lib/store/authStore";
import { homeForRole } from "../../../lib/navigation";

export function LoginPage({ navigate }) {
  const [idNo, setIdNo] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!idNo || !password) {
      setError("Please fill in all fields.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      await useAuthStore.getState().login(idNo, password);
      const role = useAuthStore.getState().role;
      navigate(homeForRole(role));
    } catch (err) {
      setError(err?.response?.data?.message || "Unable to sign in. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-[#0B1F3A] via-[#1a3a5c] to-[#0B1F3A]">
      {/* Left Panel */}
      <div className="hidden lg:flex w-1/2 flex-col justify-between p-12">
        <ALSenseLogo size="md" light showSub subText="Empowering Adult Learners" />
        <div>
          <h2 className="text-white mb-4" style={{ fontSize: "2.5rem", fontWeight: 700, lineHeight: 1.2 }}>
            Welcome back to your learning journey
          </h2>
          <p className="text-blue-200/70 text-lg mb-8">
            Access your personalized ALS learning experience powered by AI and adaptive content delivery.
          </p>
          <div className="space-y-3">
            {["AI-powered readiness profiling", "Personalized stimulus content delivery", "Real-time progress tracking", "Multi-role access management"].map(feat => (
              <div key={feat} className="flex items-center gap-3 text-blue-200">
                <div className="w-5 h-5 rounded-full bg-green-500/20 border border-green-400 flex items-center justify-center flex-shrink-0">
                  <div className="w-2 h-2 bg-green-400 rounded-full" />
                </div>
                {feat}
              </div>
            ))}
          </div>
        </div>
        <div className="text-blue-400 text-sm">ALSense &copy; 2026</div>
      </div>

      {/* Right Panel */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <button onClick={() => navigate("landing")} className="flex items-center gap-2 text-blue-300 hover:text-white mb-8 transition-colors">
            <ChevronLeft className="w-4 h-4" /> Back to Home
          </button>

          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8">
            <h2 className="text-white mb-1" style={{ fontSize: "1.75rem", fontWeight: 700 }}>Sign In</h2>
            <p className="text-blue-300 mb-6">Module 1 — User Authentication</p>

            {error && <div className="mb-4 p-3 bg-red-500/10 border border-red-400/30 rounded-xl text-red-300 text-sm">{error}</div>}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="text-blue-200 text-sm mb-2 block">ID Number</label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-blue-400" />
                  <input type="text" value={idNo} onChange={e => setIdNo(e.target.value)} placeholder="2026-00001"
                    className="w-full bg-white/5 border border-white/15 text-white placeholder-blue-400/50 rounded-xl py-3 pl-11 pr-4 focus:outline-none focus:border-blue-400 transition-colors" />
                </div>
              </div>
              <div>
                <label className="text-blue-200 text-sm mb-2 block">Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-blue-400" />
                  <input type={showPassword ? "text" : "password"} value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••"
                    className="w-full bg-white/5 border border-white/15 text-white placeholder-blue-400/50 rounded-xl py-3 pl-11 pr-12 focus:outline-none focus:border-blue-400 transition-colors" />
                  <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-4 top-1/2 -translate-y-1/2 text-blue-400 hover:text-white transition-colors">
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>
              <button type="submit" disabled={isLoading}
                className="w-full py-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-400 hover:to-cyan-400 text-white rounded-xl font-medium transition-all duration-200 disabled:opacity-50 flex items-center justify-center gap-2">
                {isLoading ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : "Sign In"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
