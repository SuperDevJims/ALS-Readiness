// PARKED (M05 frontend plan, F2): moved here unchanged from FacilitatorCohort.tsx
// when that page became the Learners list. Nothing imports it and it has no
// route. It is kept for Phase F3 (Curriculum), which reuses it as the picker
// for assigning content to a cohort. It still uses mock data: the
// contentLibrary array below, and "assigning" only shows a message.
import { useState } from "react";
import { CheckCircle, Send, X } from "lucide-react";

const contentLibrary = [
  { id:1, title:"Basic Operations & Word Problems", type:"auditory", subject:"Math",    strand:"LS3" },
  { id:2, title:"Philippine History Video Series",   type:"visual",   subject:"AP",     strand:"LS6" },
  { id:3, title:"English Grammar Guide",            type:"reading",  subject:"English", strand:"LS1" },
  { id:4, title:"Photosynthesis Explained",         type:"visual",   subject:"Science", strand:"LS4" },
  { id:5, title:"Filipino Literature: Balagtasan",  type:"auditory", subject:"Filipino",strand:"LS1" },
];

export function AssignContentModal({ learner, onClose }) {
  const [selected, setSelected] = useState([]);
  const [sent,     setSent]     = useState(false);

  const toggle = (id) => setSelected(p => p.includes(id) ? p.filter(i => i !== id) : [...p, id]);
  const handleAssign = () => { setSent(true); setTimeout(onClose, 1500); };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between p-5 border-b border-gray-100">
          <div>
            <h3 className="text-gray-800 font-bold">Assign Content</h3>
            <p className="text-gray-500 text-xs mt-0.5">Assigning to: <span className="font-medium text-gray-700">{learner?.name}</span></p>
          </div>
          <button onClick={onClose} className="p-1.5 hover:bg-gray-100 rounded-lg"><X className="w-4 h-4 text-gray-500" /></button>
        </div>
        <div className="p-5">
          <p className="text-gray-500 text-xs mb-3">Select content to assign. Stimulus type matches learner's <span className="text-[#3535C5] font-medium">{learner?.stimulus}</span> profile.</p>
          <div className="space-y-2 mb-4">
            {contentLibrary.map(c => {
              const isSel = selected.includes(c.id);
              const isMatch = c.type === learner?.stimulus?.toLowerCase();
              return (
                <button key={c.id} onClick={() => toggle(c.id)}
                  className={`w-full flex items-center gap-3 p-3 rounded-xl border-2 text-left transition-all ${isSel ? "border-[#3535C5] bg-blue-50" : "border-gray-200 hover:border-gray-300"}`}>
                  <div className={`w-5 h-5 rounded-md border-2 flex items-center justify-center flex-shrink-0 ${isSel ? "border-[#3535C5] bg-[#3535C5]" : "border-gray-300"}`}>
                    {isSel && <CheckCircle className="w-3.5 h-3.5 text-white" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-gray-700 text-sm font-medium truncate">{c.title}</div>
                    <div className="flex items-center gap-2 text-xs text-gray-400"><span>{c.subject}</span><span>·</span><span>{c.type}</span></div>
                  </div>
                  {isMatch && <span className="text-[10px] text-[#3535C5] bg-blue-50 px-1.5 py-0.5 rounded-full border border-blue-200 flex-shrink-0">Best Match</span>}
                </button>
              );
            })}
          </div>
          {sent ? (
            <div className="p-3 bg-green-50 border border-green-200 rounded-xl flex items-center gap-2 text-green-700 text-sm">
              <CheckCircle className="w-4 h-4" /> Content assigned! Learner will see it in their feed.
            </div>
          ) : (
            <div className="flex gap-3">
              <button onClick={onClose} className="flex-1 py-2.5 bg-gray-100 text-gray-600 rounded-xl text-sm hover:bg-gray-200 transition-colors">Cancel</button>
              <button onClick={handleAssign} disabled={selected.length === 0}
                className="flex-1 py-2.5 bg-orange-500 hover:bg-orange-600 text-white rounded-xl text-sm font-medium disabled:opacity-40 transition-colors flex items-center justify-center gap-2">
                <Send className="w-3.5 h-3.5" /> Assign {selected.length > 0 ? `(${selected.length})` : ""}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
