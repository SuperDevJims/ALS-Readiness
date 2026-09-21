import { useEffect, useState } from "react";
import {
  Plus, Eye, X, ShieldCheck, BookOpen, Shield,
  AlertCircle, CheckCircle2, Ban, RotateCcw, KeyRound, ChevronLeft, ChevronRight,
} from "lucide-react";
import { AppLayout } from "../shared/AppLayout";
import * as adminApi from "../../../lib/api/admin";
import { getErrorCode, getErrorMessage } from "../../../lib/api/errors";

const PAGE_SIZE = 10;

const roleIcon = { learner: BookOpen, facilitator: ShieldCheck, admin: Shield };
const roleColor = { learner: "text-green-600 bg-green-50", facilitator: "text-orange-600 bg-orange-50", admin: "text-purple-600 bg-purple-50" };
const roleLabel = { learner: "Learner", facilitator: "Facilitator", admin: "Admin" };

function displayName(u) {
  const name = [u.first_name, u.last_name].filter(Boolean).join(" ");
  return name || u.id_no || `User #${u.id}`;
}

function Banner({ result }) {
  if (!result) return null;
  const isSuccess = result.type === "success";
  return (
    <div className={`flex items-start gap-2 p-3 rounded-xl border text-xs mb-3 ${isSuccess ? "bg-green-50 border-green-200 text-green-700" : "bg-red-50 border-red-200 text-red-700"}`}>
      {isSuccess ? <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" /> : <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />}
      <span>{result.text}</span>
    </div>
  );
}

function UserModal({ u, onClose, onChanged }) {
  const [current, setCurrent] = useState(u);
  const [statusSaving, setStatusSaving] = useState(false);
  const [statusResult, setStatusResult] = useState(null);

  const [showResetForm, setShowResetForm] = useState(false);
  const [newPassword, setNewPassword] = useState("");
  const [resetSaving, setResetSaving] = useState(false);
  const [resetResult, setResetResult] = useState(null);

  if (!current) return null;
  const Icon = roleIcon[current.role];
  // Learners and facilitators are reset to a fixed default server-side; only admin targets take a typed password.
  const isAutoReset = current.role !== "admin";

  const toggleStatus = async () => {
    setStatusSaving(true);
    setStatusResult(null);
    try {
      const updated = current.is_active
        ? await adminApi.deactivateUser(current.id)
        : await adminApi.activateUser(current.id);
      setCurrent((c) => ({ ...c, is_active: updated.is_active }));
      setStatusResult({ type: "success", text: updated.is_active ? "Account reactivated." : "Account deactivated." });
      onChanged();
    } catch (err) {
      setStatusResult({ type: "error", text: getErrorMessage(err, "Couldn't change this account's status.") });
    } finally {
      setStatusSaving(false);
    }
  };

  const submitReset = async (e) => {
    e.preventDefault();
    setResetResult(null);

    if (isAutoReset) {
      setResetSaving(true);
      try {
        await adminApi.resetPasswordToDefault(current.id);
        setResetResult({
          type: "success",
          text: `Password has been reset to the default value. ${displayName(current)} will be asked to change it at next sign-in — every active session was signed out.`,
        });
        setShowResetForm(false);
      } catch (err) {
        setResetResult({ type: "error", text: getErrorMessage(err, "Couldn't reset this account's password.") });
      } finally {
        setResetSaving(false);
      }
      return;
    }

    if (newPassword.length < 8) {
      setResetResult({ type: "error", text: "New password must be at least 8 characters." });
      return;
    }

    setResetSaving(true);
    try {
      await adminApi.resetPassword(current.id, { password: newPassword });
      setResetResult({
        type: "success",
        text: `Password reset. ${displayName(current)} will need to log in again with the new password — every active session was signed out.`,
      });
      setNewPassword("");
    } catch (err) {
      const code = getErrorCode(err);
      setResetResult({
        type: "error",
        text: code === "VALIDATION" ? getErrorMessage(err) : getErrorMessage(err, "Couldn't reset this account's password."),
      });
    } finally {
      setResetSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between p-5 border-b border-gray-100">
          <h3 className="text-gray-800 font-bold">User Account</h3>
          <button onClick={onClose} className="p-1.5 hover:bg-gray-100 rounded-lg"><X className="w-4 h-4 text-gray-500" /></button>
        </div>
        <div className="p-5">
          <div className="flex items-center gap-4 mb-5">
            <div className="w-14 h-14 bg-gradient-to-br from-purple-400 to-indigo-500 rounded-2xl flex items-center justify-center text-white text-xl font-bold">
              {displayName(current)[0]?.toUpperCase()}
            </div>
            <div>
              <h4 className="text-gray-800 font-bold text-lg">{displayName(current)}</h4>
              <div className="text-gray-500 text-sm">{current.id_no}</div>
              <span className={`text-xs px-2 py-0.5 rounded-full mt-1 inline-flex items-center gap-1 ${roleColor[current.role]}`}>
                <Icon className="w-3 h-3" />{roleLabel[current.role]}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 mb-5">
            <div className="p-3 bg-gray-50 rounded-xl">
              <div className="text-gray-400 text-xs">Status</div>
              <div className={`font-medium text-sm ${current.is_active ? "text-green-600" : "text-gray-500"}`}>
                {current.is_active ? "Active" : "Inactive"}
              </div>
            </div>
            <div className="p-3 bg-gray-50 rounded-xl">
              <div className="text-gray-400 text-xs">Joined</div>
              <div className="text-gray-800 font-medium text-sm">{new Date(current.created_at).toLocaleDateString()}</div>
            </div>
          </div>

          {/* Deactivate / Reactivate */}
          <div className="border border-gray-100 rounded-xl p-4 mb-3">
            <Banner result={statusResult} />
            <p className="text-gray-500 text-xs mb-3">
              {current.is_active
                ? "Deactivating prevents this account from logging in until it's reactivated."
                : "This account is deactivated and cannot log in. Reactivating restores access immediately."}
            </p>
            <button
              onClick={toggleStatus}
              disabled={statusSaving}
              className={`w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium transition-colors disabled:opacity-50 ${
                current.is_active ? "bg-red-50 text-red-600 hover:bg-red-100" : "bg-green-50 text-green-700 hover:bg-green-100"
              }`}
            >
              {current.is_active ? <Ban className="w-4 h-4" /> : <RotateCcw className="w-4 h-4" />}
              {statusSaving ? "Working…" : current.is_active ? "Deactivate Account" : "Reactivate Account"}
            </button>
          </div>

          {/* Reset password */}
          <div className="border border-gray-100 rounded-xl p-4">
            <Banner result={resetResult} />
            {!showResetForm ? (
              <button
                onClick={() => setShowResetForm(true)}
                className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium bg-purple-50 text-purple-700 hover:bg-purple-100 transition-colors"
              >
                <KeyRound className="w-4 h-4" /> Reset Password
              </button>
            ) : (
              <form onSubmit={submitReset}>
                {isAutoReset ? (
                  <p className="text-gray-600 text-xs mb-2">
                    Reset this account's password to the default value? {displayName(current)} will be asked to change it the next time they sign in.
                  </p>
                ) : (
                  <>
                    <label className="text-gray-600 text-xs font-medium mb-1.5 block">New password for this account</label>
                    <input
                      type="text"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      placeholder="At least 8 characters"
                      className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-purple-400 mb-2"
                    />
                  </>
                )}
                <p className="text-gray-400 text-xs mb-3">Every active session for this account will be signed out immediately.</p>
                <div className={isAutoReset ? "flex gap-2" : ""}>
                  {isAutoReset && (
                    <button
                      type="button"
                      onClick={() => setShowResetForm(false)}
                      className="flex-1 py-2.5 bg-gray-100 text-gray-600 rounded-xl text-sm hover:bg-gray-200 transition-colors"
                    >
                      Cancel
                    </button>
                  )}
                  <button
                    type="submit"
                    disabled={resetSaving}
                    className={`${isAutoReset ? "flex-1" : "w-full"} py-2.5 bg-purple-500 hover:bg-purple-600 text-white rounded-xl text-sm font-medium transition-colors disabled:opacity-50`}
                  >
                    {resetSaving ? "Resetting…" : "Confirm Reset"}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function CreateUserModal({ onClose, onCreated }) {
  const [role, setRole] = useState("learner");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    if (!firstName.trim() || !lastName.trim()) {
      setError("First and last name are required.");
      return;
    }

    setSaving(true);
    try {
      const created = await adminApi.createUser(role, { first_name: firstName.trim(), last_name: lastName.trim() });
      setResult(created);
      onCreated();
    } catch (err) {
      const code = getErrorCode(err);
      if (code === "ALREADY_EXISTS") {
        setError(getErrorMessage(err, "That account already exists."));
      } else {
        setError(getErrorMessage(err, "Couldn't create the account."));
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between p-5 border-b border-gray-100">
          <h3 className="text-gray-800 font-bold">{result ? "Account Created" : "Add User Account"}</h3>
          <button onClick={onClose} className="p-1.5 hover:bg-gray-100 rounded-lg"><X className="w-4 h-4 text-gray-500" /></button>
        </div>

        {result ? (
          <div className="p-5">
            <div className="flex items-center gap-2 text-green-700 bg-green-50 border border-green-200 rounded-xl p-3 mb-4 text-sm">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>{roleLabel[result.role]} account created. Share these credentials securely — this password won't be shown again.</span>
            </div>
            <div className="grid grid-cols-1 gap-3 mb-4">
              <div className="p-3 bg-gray-50 rounded-xl">
                <div className="text-gray-400 text-xs mb-0.5">ID Number</div>
                <div className="text-gray-800 font-mono font-bold text-lg">{result.id_no}</div>
              </div>
              <div className="p-3 bg-gray-50 rounded-xl">
                <div className="text-gray-400 text-xs mb-0.5">Temporary Password</div>
                <div className="text-gray-800 font-mono font-bold text-lg">{result.password}</div>
              </div>
            </div>
            <button onClick={onClose} className="w-full py-2.5 bg-[#0B1F3A] hover:bg-[#152e56] text-white rounded-xl text-sm font-medium transition-colors">
              Done
            </button>
          </div>
        ) : (
          <form onSubmit={submit}>
            <div className="p-5 space-y-4">
              <div>
                <label className="text-gray-600 text-sm font-medium mb-1.5 block">Role</label>
                <div className="grid grid-cols-3 gap-2">
                  {["learner", "facilitator", "admin"].map((r) => {
                    const Icon = roleIcon[r];
                    return (
                      <button
                        key={r}
                        type="button"
                        onClick={() => setRole(r)}
                        className={`flex flex-col items-center gap-1 py-2.5 rounded-xl border text-xs font-medium transition-colors ${
                          role === r ? "border-purple-400 bg-purple-50 text-purple-700" : "border-gray-200 text-gray-500 hover:border-gray-300"
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                        {roleLabel[r]}
                      </button>
                    );
                  })}
                </div>
              </div>

              {error && (
                <div className="flex items-start gap-2 p-3 rounded-xl border border-red-200 bg-red-50 text-red-700 text-xs">
                  <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              <div>
                <label className="text-gray-600 text-sm font-medium mb-1.5 block">First Name</label>
                <input
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  placeholder="Juan"
                  className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-700 bg-gray-50 focus:outline-none focus:border-purple-400 text-sm"
                />
              </div>
              <div>
                <label className="text-gray-600 text-sm font-medium mb-1.5 block">Last Name</label>
                <input
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  placeholder="Dela Cruz"
                  className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-700 bg-gray-50 focus:outline-none focus:border-purple-400 text-sm"
                />
              </div>
            </div>
            <div className="flex gap-3 p-5 pt-0">
              <button type="button" onClick={onClose} className="flex-1 py-2.5 bg-gray-100 text-gray-600 rounded-xl text-sm hover:bg-gray-200 transition-colors">
                Cancel
              </button>
              <button type="submit" disabled={saving} className="flex-1 py-2.5 bg-purple-500 hover:bg-purple-600 text-white rounded-xl text-sm font-medium transition-colors disabled:opacity-50">
                {saving ? "Creating…" : "Create Account"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export function AdminUsers({ navigate, user, onLogout }) {
  const [roleFilter, setRoleFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");
  const [page, setPage] = useState(1);

  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  const [counts, setCounts] = useState({ learner: 0, facilitator: 0, admin: 0 });

  const [selectedUser, setSelectedUser] = useState(null);
  const [showAdd, setShowAdd] = useState(false);

  const fetchList = () => {
    setLoading(true);
    setLoadError("");
    adminApi
      .listUsers({
        page,
        page_size: PAGE_SIZE,
        role: roleFilter === "All" ? undefined : roleFilter.toLowerCase(),
        is_active: statusFilter === "All" ? undefined : statusFilter === "Active",
      })
      .then((res) => {
        setItems(res.items);
        setTotal(res.total);
      })
      .catch((err) => setLoadError(getErrorMessage(err, "Couldn't load users.")))
      .finally(() => setLoading(false));
  };

  const fetchCounts = () => {
    Promise.all([
      adminApi.listUsers({ page: 1, page_size: 1, role: "learner" }),
      adminApi.listUsers({ page: 1, page_size: 1, role: "facilitator" }),
      adminApi.listUsers({ page: 1, page_size: 1, role: "admin" }),
    ])
      .then(([l, f, a]) => setCounts({ learner: l.total, facilitator: f.total, admin: a.total }))
      .catch(() => {
        // Summary tiles are non-critical - leave at last-known values on failure.
      });
  };

  useEffect(() => {
    fetchList();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, roleFilter, statusFilter]);

  useEffect(() => {
    fetchCounts();
  }, []);

  const changeRoleFilter = (f) => { setRoleFilter(f); setPage(1); };
  const changeStatusFilter = (f) => { setStatusFilter(f); setPage(1); };

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage="admin-users">
      {selectedUser && (
        <UserModal
          u={selectedUser}
          onClose={() => setSelectedUser(null)}
          onChanged={() => { fetchList(); fetchCounts(); }}
        />
      )}
      {showAdd && (
        <CreateUserModal
          onClose={() => { setShowAdd(false); fetchList(); fetchCounts(); }}
          onCreated={() => {}}
        />
      )}

      <div className="p-5 space-y-5">
        <div className="bg-gradient-to-r from-[#0B1F3A] to-[#1a3a5c] rounded-2xl p-5 text-white flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2"><span className="text-xs bg-white/15 px-2 py-0.5 rounded font-mono">ADMIN</span><span className="text-blue-300 text-xs">User Account Management</span></div>
            <h2 className="mb-1" style={{ fontSize: "1.25rem", fontWeight: 700 }}>User Accounts</h2>
            <p className="text-blue-200/70 text-sm">
              {counts.learner + counts.facilitator + counts.admin} total users — {counts.learner} learners · {counts.facilitator} facilitators · {counts.admin} admins
            </p>
          </div>
          <button onClick={() => setShowAdd(true)} className="flex items-center gap-2 px-4 py-2.5 bg-purple-500 hover:bg-purple-400 text-white rounded-xl text-sm font-medium transition-colors">
            <Plus className="w-4 h-4" /> Add Account
          </button>
        </div>

        {/* Role summary */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: "Learners", value: counts.learner, icon: BookOpen, cls: "text-green-600 bg-green-50" },
            { label: "Facilitators", value: counts.facilitator, icon: ShieldCheck, cls: "text-orange-600 bg-orange-50" },
            { label: "Admins", value: counts.admin, icon: Shield, cls: "text-purple-600 bg-purple-50" },
          ].map((s) => {
            const Icon = s.icon;
            return (
              <div key={s.label} className="bg-white rounded-2xl border border-gray-100 p-4 flex items-center gap-4">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${s.cls}`}><Icon className="w-5 h-5" /></div>
                <div><div className="text-gray-800 text-xl font-bold">{s.value}</div><div className="text-gray-500 text-xs">{s.label}</div></div>
              </div>
            );
          })}
        </div>

        {/* Filters */}
        <div className="bg-white rounded-2xl border border-gray-100 p-4 flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-1.5">
            <span className="text-gray-500 text-xs">Role:</span>
            {["All", "Learner", "Facilitator", "Admin"].map((f) => (
              <button key={f} onClick={() => changeRoleFilter(f)}
                className={`px-3 py-1.5 rounded-lg text-xs transition-colors ${roleFilter === f ? "bg-purple-500 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>{f}</button>
            ))}
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-gray-500 text-xs">Status:</span>
            {["All", "Active", "Inactive"].map((f) => (
              <button key={f} onClick={() => changeStatusFilter(f)}
                className={`px-3 py-1.5 rounded-lg text-xs transition-colors ${statusFilter === f ? "bg-purple-500 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>{f}</button>
            ))}
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>{["Name", "ID Number", "Role", "Status", "Joined", "Actions"].map((h) => (
                <th key={h} className="text-left px-4 py-3 text-xs text-gray-500 font-semibold">{h}</th>
              ))}</tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {loading && (
                <tr><td colSpan={6} className="px-4 py-10 text-center text-gray-400 text-sm">Loading users…</td></tr>
              )}

              {!loading && loadError && (
                <tr><td colSpan={6} className="px-4 py-10 text-center text-red-500 text-sm">{loadError}</td></tr>
              )}

              {!loading && !loadError && items.length === 0 && (
                <tr><td colSpan={6} className="px-4 py-10 text-center text-gray-400 text-sm">No users found.</td></tr>
              )}

              {!loading && !loadError && items.map((u) => {
                const Icon = roleIcon[u.role];
                return (
                  <tr key={u.id} className="hover:bg-purple-50/20 transition-colors">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-gradient-to-br from-purple-400 to-indigo-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                          {displayName(u)[0]?.toUpperCase()}
                        </div>
                        <span className="text-gray-800 text-sm font-medium">{displayName(u)}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-gray-500 text-xs font-mono">{u.id_no}</td>
                    <td className="px-4 py-3">
                      <span className={`flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full w-fit ${roleColor[u.role]}`}>
                        <Icon className="w-3 h-3" />{roleLabel[u.role]}
                      </span>
                    </td>
                    <td className="px-4 py-3"><span className={`text-xs px-2 py-1 rounded-full ${u.is_active ? "text-green-600 bg-green-50" : "text-gray-500 bg-gray-100"}`}>{u.is_active ? "Active" : "Inactive"}</span></td>
                    <td className="px-4 py-3 text-gray-400 text-xs">{new Date(u.created_at).toLocaleDateString()}</td>
                    <td className="px-4 py-3">
                      <button onClick={() => setSelectedUser(u)} className="text-purple-500 hover:text-purple-700 transition-colors"><Eye className="w-3.5 h-3.5" /></button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          {/* Pagination */}
          <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100">
            <span className="text-gray-400 text-xs">
              {total === 0 ? "0 users" : `Page ${page} of ${totalPages} — ${total} users`}
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1 || loading}
                className="p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 disabled:opacity-40 transition-colors"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages || loading}
                className="p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 disabled:opacity-40 transition-colors"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
