import { AlertCircle, CheckCircle2 } from "lucide-react";

/** Inline success/error result for a form. `result` is `{ type: "success" | "error", text }` or null. */
export function Banner({ result }) {
  if (!result) return null;
  const isSuccess = result.type === "success";
  return (
    <div
      className={`flex items-start gap-2.5 p-3.5 rounded-xl border text-sm mb-4 ${
        isSuccess ? "bg-green-50 border-green-200 text-green-700" : "bg-red-50 border-red-200 text-red-700"
      }`}
    >
      {isSuccess ? <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" /> : <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />}
      <span>{result.text}</span>
    </div>
  );
}
