import { useState } from "react";
import { useParams, useSearchParams } from "react-router";
import { Activity, ClipboardList, Clock, UserX } from "lucide-react";
import { AppLayout } from "../shared/AppLayout";
import type { PageProps } from "../../routes/ProtectedPage";
import { getLearner } from "../../../lib/api/facilitator";
import type {
  AtRiskFlagStatus,
  AtRiskFlagSummary,
  FacilitatorLearnerDetailResponse,
  LearnerMembership,
  LearnerStrandDetail,
  StrandTestResult,
} from "../../../lib/api/types";
import { FLAGS_NOT_UPDATED_TEXT, flagActions, flagReasonText, flagStatusLabel } from "../../../lib/atRisk";
import { formatDate, formatDateTime, formatLastActive } from "../../../lib/dates";
import { useFetch } from "../../../lib/hooks/useFetch";
import { DASH, cohortStatusLabel, memberStatusLabel, orDash, personName } from "../../../lib/labels";
import { detailFailureText, intakeRows, lriTile, parseIdParam, progressCell, testCell } from "../../../lib/learnersText";
import { LEARNER_COHORT_PARAM, learnerDetailPage } from "../../../lib/navigation";
import {
  AtRiskReviewDialog,
  Button,
  Card,
  DataTable,
  EmptyState,
  ErrorState,
  LoadingState,
  Notice,
  PageHeader,
  Pill,
  ProgressBar,
  ReadinessPill,
  StatTile,
  type DataTableColumn,
  type PillTone,
} from "./shared";

const LEARNERS_PAGE = "facilitator-learners";

const FLAG_STATUS_TONE: Record<AtRiskFlagStatus, PillTone> = {
  open: "warning",
  reviewed: "neutral",
  dismissed: "muted",
  resolved: "success",
};

function TestResultCell({ result }: { result: StrandTestResult | null }) {
  const cell = testCell(result);
  if (result === null) return <span className="text-gray-400">{cell.main}</span>;
  return (
    <div>
      <div className="text-gray-800 font-medium">{cell.main}</div>
      <div className="text-gray-400 text-xs">{cell.score}{cell.date ? ` · ${cell.date}` : ""}</div>
    </div>
  );
}

const STRAND_COLUMNS: DataTableColumn<LearnerStrandDetail>[] = [
  {
    key: "strand",
    header: "Strand",
    render: (strand) => (
      <div>
        <div className="text-gray-800 font-medium">{strand.strand_code}</div>
        <div className="text-gray-400 text-xs">{strand.strand_name}</div>
      </div>
    ),
  },
  { key: "pretest", header: "Pretest MPS", render: (strand) => <TestResultCell result={strand.pretest} /> },
  { key: "posttest", header: "Posttest MPS", render: (strand) => <TestResultCell result={strand.posttest} /> },
  {
    key: "progress",
    header: "Progress",
    render: (strand) => {
      const cell = progressCell(strand.progress);
      return (
        <div>
          <ProgressBar value={cell.barValue} widthClass="w-24" label={`${strand.strand_code} progress`} />
          {cell.detail && <div className="text-gray-400 text-xs mt-0.5">{cell.detail}</div>}
        </div>
      );
    },
  },
];

function MembershipPills({ membership }: { membership: Pick<LearnerMembership, "status" | "membership_status"> }) {
  return (
    <>
      {membership.membership_status === "ended" && <Pill tone="muted">Membership {memberStatusLabel(membership.membership_status).toLowerCase()}</Pill>}
      {membership.status !== "active" && <Pill tone="muted">Cohort {cohortStatusLabel(membership.status).toLowerCase()}</Pill>}
    </>
  );
}

interface LoadedProps {
  data: FacilitatorLearnerDetailResponse;
  onReview: () => void;
  onOpenCohort: (cohortId: number) => void;
}

function LoadedDetail({ data, onReview, onOpenCohort }: LoadedProps) {
  const lri = lriTile(data.lri);

  const flagColumns: DataTableColumn<AtRiskFlagSummary>[] = [
    { key: "reason", header: "Reason", render: (flag) => flagReasonText(flag) },
    { key: "status", header: "Status", render: (flag) => <Pill tone={FLAG_STATUS_TONE[flag.status]}>{flagStatusLabel(flag.status)}</Pill> },
    { key: "detected", header: "Detected", className: "text-gray-500 text-xs", render: (flag) => formatDate(flag.detected_at) ?? DASH },
    { key: "resolved", header: "Resolved", className: "text-gray-500 text-xs", render: (flag) => formatDate(flag.resolved_at) ?? DASH },
    { key: "reviewed-by", header: "Reviewed by", className: "text-gray-500 text-xs", render: (flag) => orDash(flag.reviewed_by_name) },
    { key: "note", header: "Note", className: "text-gray-500 text-xs max-w-xs whitespace-pre-wrap", render: (flag) => orDash(flag.note) },
    {
      key: "review",
      header: "Review",
      render: (flag) => (flagActions(flag.status).length > 0 ? <Button variant="link" onClick={onReview}>Review</Button> : null),
    },
  ];

  return (
    <>
      <div className="grid grid-cols-3 gap-3">
        <StatTile
          label="Readiness"
          icon={Activity}
          tone="teal"
          value={<ReadinessPill readiness={data.readiness} />}
          hint="Readiness appears once EEG profiling is available."
        />
        <StatTile
          label="Last active"
          icon={Clock}
          tone="blue"
          value={formatLastActive(data.last_active_at)}
          hint={formatDateTime(data.last_active_at) ?? undefined}
        />
        <StatTile label="LRI score" icon={ClipboardList} tone="purple" value={lri.value} hint={lri.hint ?? undefined} />
      </div>

      <section className="space-y-3">
        <h3 className="text-gray-800 font-semibold text-sm">Performance by strand</h3>
        <DataTable
          columns={STRAND_COLUMNS}
          rows={data.strands}
          rowKey={(strand) => strand.strand_id}
          emptyMessage="No active learning strands."
        />
      </section>

      <Card title="Intake summary">
        {data.intake === null ? (
          <p className="text-gray-400 text-sm">No intake form submitted yet</p>
        ) : (
          <dl className="grid grid-cols-3 gap-x-6 gap-y-4">
            {intakeRows(data.intake).map((row) => (
              <div key={row.label}>
                <dt className="text-gray-500 text-xs">{row.label}</dt>
                <dd className="text-gray-800 text-sm font-medium mt-0.5">{row.value}</dd>
              </div>
            ))}
          </dl>
        )}
      </Card>

      <section className="space-y-3">
        <h3 className="text-gray-800 font-semibold text-sm">At-risk history</h3>
        {data.cohort.status !== "active" && <Notice>{FLAGS_NOT_UPDATED_TEXT}</Notice>}
        <DataTable
          columns={flagColumns}
          rows={data.at_risk_flags}
          rowKey={(flag) => flag.id}
          emptyMessage="No flags for this learner"
        />
      </section>

      {data.memberships.length > 0 && (
        <Card title="Other cohorts">
          <ul className="divide-y divide-gray-50">
            {data.memberships.map((membership) => (
              <li key={membership.id} className="flex items-center justify-between gap-3 py-2.5 first:pt-0 last:pb-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-gray-800 text-sm font-medium">{membership.name}</span>
                  <span className="text-gray-400 text-xs">SY {membership.school_year}</span>
                  <Pill tone={membership.membership_status === "active" ? "success" : "muted"}>
                    {memberStatusLabel(membership.membership_status)}
                  </Pill>
                </div>
                <Button variant="link" onClick={() => onOpenCohort(membership.id)}>View in this cohort</Button>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </>
  );
}

export function FacilitatorLearnerDetail({ navigate, user, onLogout }: PageProps) {
  // The learner and the cohort both come from the URL, not from the top bar's
  // selection, so a reload or a shared link shows the same view.
  const params = useParams();
  const [searchParams] = useSearchParams();
  const learnerId = parseIdParam(params.learnerId);
  // Absent (or unreadable): no cohort_id is sent and the backend chooses the membership.
  const cohortId = parseIdParam(searchParams.get(LEARNER_COHORT_PARAM));

  // Keyed on both: moving to another learner or cohort reloads, and a slow
  // earlier response is dropped by the hook.
  const detail = useFetch(
    () => getLearner(learnerId as number, cohortId ?? undefined),
    [learnerId, cohortId],
    { enabled: learnerId !== null, fallbackError: "Unable to load this learner." },
  );
  const data = detail.data;

  const [reviewing, setReviewing] = useState(false);

  let body;
  if (learnerId === null) {
    body = (
      <Card padding="none">
        <EmptyState icon={UserX} title="Learner not found" description="This link does not point to a learner. Go back to the Learners list and open one from there." />
      </Card>
    );
  } else if (detail.error) {
    const failure = detailFailureText(detail.errorStatus, detail.error);
    body = <ErrorState title={failure.title} message={failure.message} onRetry={failure.canRetry ? detail.reload : undefined} />;
  } else if (!data) {
    body = <LoadingState label="Loading the learner…" />;
  } else {
    body = (
      <LoadedDetail
        data={data}
        onReview={() => setReviewing(true)}
        onOpenCohort={(otherCohortId) => navigate(learnerDetailPage(data.learner.learner_id, otherCohortId))}
      />
    );
  }

  return (
    <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage={LEARNERS_PAGE}>
      {reviewing && data && (
        <AtRiskReviewDialog
          learner={data.learner}
          cohortId={data.cohort.id}
          onClose={() => setReviewing(false)}
          onChanged={detail.reload}
        />
      )}

      <div className="p-5 space-y-5">
        <PageHeader
          backLabel="Back to Learners"
          onBack={() => navigate(LEARNERS_PAGE)}
          eyebrow="Learner Detail"
          title={data ? personName(data.learner, "Unnamed learner") : "Learner"}
          subtitle={
            data ? (
              <span className="flex items-center gap-2 flex-wrap">
                <span>{orDash(data.learner.id_no)} · {data.cohort.name} · SY {data.cohort.school_year}</span>
                <MembershipPills membership={data.cohort} />
              </span>
            ) : undefined
          }
        />
        {body}
      </div>
    </AppLayout>
  );
}
