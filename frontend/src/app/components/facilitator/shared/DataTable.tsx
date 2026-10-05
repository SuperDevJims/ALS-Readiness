import type { KeyboardEvent, ReactNode } from "react";

export interface DataTableColumn<T> {
  /** Unique within the table; used as the React key. */
  key: string;
  header: ReactNode;
  render: (row: T) => ReactNode;
  /** Default: "left". */
  align?: "left" | "right" | "center";
  /** Extra classes for this column's cells, e.g. "w-40" or "text-gray-500 text-xs". */
  className?: string;
}

interface DataTableProps<T> {
  columns: DataTableColumn<T>[];
  rows: T[];
  rowKey: (row: T) => string | number;
  /** Makes rows clickable (and reachable by keyboard: Enter or Space opens the row). */
  onRowClick?: (row: T) => void;
  loading?: boolean;
  loadingLabel?: string;
  /** Shown in place of the rows when the load failed. */
  error?: string | null;
  /** Shown when there are no rows. */
  emptyMessage?: ReactNode;
  /** Rendered under the table inside the same panel - normally a <Pagination />. */
  footer?: ReactNode;
}

const ALIGN = { left: "text-left", right: "text-right", center: "text-center" } as const;

/**
 * The table the existing pages hand-write: white rounded panel, grey header
 * row, hairline row dividers, a soft orange row hover. Loading, error and
 * empty are shown as one full-width row, as AdminUsers does.
 */
export function DataTable<T>({
  columns,
  rows,
  rowKey,
  onRowClick,
  loading = false,
  loadingLabel = "Loading…",
  error = null,
  emptyMessage = "Nothing to show.",
  footer,
}: DataTableProps<T>) {
  const message = (text: ReactNode, tone: string) => (
    <tr>
      <td colSpan={columns.length} className={`px-4 py-10 text-center text-sm ${tone}`}>{text}</td>
    </tr>
  );

  const onRowKeyDown = (event: KeyboardEvent<HTMLTableRowElement>, row: T) => {
    if (event.target !== event.currentTarget) return; // a button inside the row handles its own keys
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onRowClick?.(row);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr>
              {columns.map((column) => (
                <th key={column.key} scope="col" className={`${ALIGN[column.align ?? "left"]} px-4 py-3 text-xs text-gray-500 font-semibold`}>
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50" aria-busy={loading}>
            {loading && message(loadingLabel, "text-gray-400")}
            {!loading && error && message(error, "text-red-500")}
            {!loading && !error && rows.length === 0 && message(emptyMessage, "text-gray-400")}
            {!loading && !error && rows.map((row) => (
              <tr
                key={rowKey(row)}
                className={onRowClick ? "hover:bg-orange-50/30 transition-colors cursor-pointer focus:outline-none focus-visible:bg-orange-50/60" : "hover:bg-orange-50/30 transition-colors"}
                onClick={onRowClick ? () => onRowClick(row) : undefined}
                onKeyDown={onRowClick ? (event) => onRowKeyDown(event, row) : undefined}
                tabIndex={onRowClick ? 0 : undefined}
              >
                {columns.map((column) => (
                  <td key={column.key} className={`px-4 py-3 text-sm text-gray-700 ${ALIGN[column.align ?? "left"]} ${column.className ?? ""}`}>
                    {column.render(row)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {footer}
    </div>
  );
}
