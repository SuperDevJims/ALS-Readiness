import { ChevronLeft, ChevronRight } from "lucide-react";

interface PaginationProps {
  /** 1-based, as the API sends it. */
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
  /** What is being counted, plural: "learners", "items". Default: "items". */
  noun?: string;
  /** Disables both buttons while a page is loading. */
  disabled?: boolean;
}

/** The footer under a paginated table: "Page 2 of 5 — 93 learners" and previous / next buttons. */
export function Pagination({ page, pageSize, total, onPageChange, noun = "items", disabled = false }: PaginationProps) {
  const totalPages = Math.max(1, Math.ceil(total / Math.max(1, pageSize)));

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100">
      <span className="text-gray-400 text-xs">
        {total === 0 ? `0 ${noun}` : `Page ${page} of ${totalPages} — ${total} ${noun}`}
      </span>
      <div className="flex items-center gap-2">
        <button
          type="button"
          aria-label="Previous page"
          onClick={() => onPageChange(Math.max(1, page - 1))}
          disabled={page <= 1 || disabled}
          className="p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 disabled:opacity-40 transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
        <button
          type="button"
          aria-label="Next page"
          onClick={() => onPageChange(Math.min(totalPages, page + 1))}
          disabled={page >= totalPages || disabled}
          className="p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 disabled:opacity-40 transition-colors"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
