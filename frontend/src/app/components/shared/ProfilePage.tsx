import { useEffect, useState } from "react";
import { AlertCircle, Lock, Save } from "lucide-react";
import { AppLayout } from "./AppLayout";
import { Banner } from "./Banner";
import { ChangePasswordForm } from "./ChangePasswordForm";
import * as authApi from "../../../lib/api/auth";
import { getErrorMessage } from "../../../lib/api/errors";
import { useAuthStore } from "../../../lib/store/authStore";

const emptyForm = {
  first_name: "",
  last_name: "",
  middle_name: "",
  birthdate: "",
  gender: "",
  address: "",
  contact_number: "",
  contact_email: "",
};

export function ProfilePage({ navigate, user, onLogout }) {
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [me, setMe] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [saveResult, setSaveResult] = useState(null);

  useEffect(() => {
    let active = true;

    authApi
      .getMe()
      .then((data) => {
        if (!active) return;
        setMe(data);
        setForm({
          first_name: data.profile.first_name ?? "",
          last_name: data.profile.last_name ?? "",
          middle_name: data.profile.middle_name ?? "",
          birthdate: data.profile.birthdate ?? "",
          gender: data.profile.gender ?? "",
          address: data.profile.address ?? "",
          contact_number: data.profile.contact_number ?? "",
          contact_email: data.profile.contact_email ?? "",
        });
      })
      .catch((err) => {
        if (active) setLoadError(getErrorMessage(err, "Couldn't load your profile."));
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  const update = (key, value) => setForm((f) => ({ ...f, [key]: value }));

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveResult(null);

    try {
      const updated = await authApi.updateMe({
        first_name: form.first_name,
        last_name: form.last_name,
        middle_name: form.middle_name || null,
        birthdate: form.birthdate || null,
        gender: form.gender || null,
        address: form.address || null,
        contact_number: form.contact_number || null,
        contact_email: form.contact_email || null,
      });
      setMe(updated);
      useAuthStore.getState().refreshUser(updated);
      setSaveResult({ type: "success", text: "Profile updated." });
    } catch (err) {
      setSaveResult({ type: "error", text: getErrorMessage(err, "Couldn't save your profile.") });
    } finally {
      setSaving(false);
    }
  };

  return (
    <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage="profile">
      <div className="max-w-3xl mx-auto p-6 space-y-6">
        {/* ── Profile Information ── */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-gray-800 mb-1" style={{ fontSize: "1.1rem", fontWeight: 700 }}>
            Profile Information
          </h2>
          <p className="text-gray-400 text-sm mb-5">Your account details and personal information.</p>

          {loading && <div className="text-gray-400 text-sm py-6 text-center">Loading your profile…</div>}

          {!loading && loadError && (
            <div className="flex items-start gap-2.5 p-3.5 rounded-xl border border-red-200 bg-red-50 text-red-700 text-sm">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{loadError}</span>
            </div>
          )}

          {!loading && !loadError && me && (
            <form onSubmit={handleSave}>
              <Banner result={saveResult} />

              {/* Read-only fields */}
              <div className="grid grid-cols-2 gap-4 mb-5 pb-5 border-b border-gray-100">
                <div>
                  <span className="text-gray-400 text-xs block mb-1">ID Number</span>
                  <span className="text-gray-700 text-sm font-medium">{me.id_no}</span>
                </div>
                <div>
                  <span className="text-gray-400 text-xs block mb-1">Role</span>
                  <span className="text-gray-700 text-sm font-medium capitalize">{me.role}</span>
                </div>
                <div>
                  <span className="text-gray-400 text-xs block mb-1">Status</span>
                  <span className={`text-sm font-medium ${me.is_active ? "text-green-600" : "text-gray-500"}`}>
                    {me.is_active ? "Active" : "Inactive"}
                  </span>
                </div>
                <div>
                  <span className="text-gray-400 text-xs block mb-1">Member since</span>
                  <span className="text-gray-700 text-sm font-medium">
                    {new Date(me.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>

              {/* Editable fields */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">First Name</label>
                  <input
                    value={form.first_name}
                    onChange={(e) => update("first_name", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  />
                </div>
                <div>
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">Last Name</label>
                  <input
                    value={form.last_name}
                    onChange={(e) => update("last_name", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  />
                </div>
                <div>
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">Middle Name</label>
                  <input
                    value={form.middle_name}
                    onChange={(e) => update("middle_name", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  />
                </div>
                <div>
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">Birthdate</label>
                  <input
                    type="date"
                    value={form.birthdate}
                    onChange={(e) => update("birthdate", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  />
                </div>
                <div>
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">Gender</label>
                  <select
                    value={form.gender}
                    onChange={(e) => update("gender", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  >
                    <option value="">Not set</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div>
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">Contact Number</label>
                  <input
                    value={form.contact_number}
                    onChange={(e) => update("contact_number", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  />
                </div>
                <div className="col-span-2">
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">Address</label>
                  <input
                    value={form.address}
                    onChange={(e) => update("address", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  />
                </div>
                <div className="col-span-2">
                  <label className="text-gray-600 text-sm font-medium mb-1.5 block">Contact Email</label>
                  <input
                    type="email"
                    value={form.contact_email}
                    onChange={(e) => update("contact_email", e.target.value)}
                    className="w-full border border-gray-200 rounded-xl py-2.5 px-4 text-gray-800 text-sm bg-gray-50 focus:outline-none focus:border-[#1a3a6c] transition-colors"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={saving}
                className="mt-5 flex items-center gap-2 px-5 py-2.5 bg-[#1a3a6c] hover:bg-[#152e56] text-white rounded-xl text-sm font-medium transition-colors disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                {saving ? "Saving…" : "Save Changes"}
              </button>
            </form>
          )}
        </div>

        {/* ── Change Password ── */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-gray-800 mb-1 flex items-center gap-2" style={{ fontSize: "1.1rem", fontWeight: 700 }}>
            <Lock className="w-4 h-4" /> Change Password
          </h2>
          <p className="text-gray-400 text-sm mb-5">
            Changing your password keeps this device signed in and signs out every other session.
          </p>

          <ChangePasswordForm />
        </div>
      </div>
    </AppLayout>
  );
}
