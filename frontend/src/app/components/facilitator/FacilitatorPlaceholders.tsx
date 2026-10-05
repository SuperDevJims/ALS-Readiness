import type { ReactNode } from "react";
import { useParams } from "react-router";
import { Hammer } from "lucide-react";
import { AppLayout } from "../shared/AppLayout";
import type { PageProps } from "../../routes/ProtectedPage";
import { Card, EmptyState, PageHeader } from "./shared";

// Titled stand-ins for the facilitator screens that have no mockup yet
// (M05 frontend plan, Phase F0). Each is replaced by the real page in its own
// phase: Curriculum in F3, My Cohorts in F5, Strand Tests in F6. (Learner
// Detail was replaced in F2 by FacilitatorLearnerDetail.tsx.) They hold no
// data, real or mock.

interface PlaceholderProps extends PageProps {
  /** The sidebar entry to highlight and the top bar title to show. */
  currentPage: string;
  title: string;
  subtitle: ReactNode;
  eyebrow: string;
  phase: string;
}

function Placeholder({ navigate, user, onLogout, currentPage, title, subtitle, eyebrow, phase }: PlaceholderProps) {
  return (
    <AppLayout navigate={navigate} user={user} onLogout={onLogout} currentPage={currentPage}>
      <div className="p-5 space-y-5">
        <PageHeader title={title} subtitle={subtitle} eyebrow={eyebrow} />
        <Card padding="none">
          <EmptyState
            icon={Hammer}
            title="This screen is not built yet"
            description={`It arrives in phase ${phase} of the M05 frontend plan.`}
          />
        </Card>
      </div>
    </AppLayout>
  );
}

/** `/facilitator-curriculum` */
export function FacilitatorCurriculum(props: PageProps) {
  return (
    <Placeholder
      {...props}
      currentPage="facilitator-curriculum"
      title="Curriculum"
      subtitle="Structure is shared across cohorts; only content assignment differs."
      eyebrow="Curriculum"
      phase="F3"
    />
  );
}

/** `/facilitator-tests` */
export function FacilitatorTests(props: PageProps) {
  return (
    <Placeholder
      {...props}
      currentPage="facilitator-tests"
      title="Strand Tests"
      subtitle="The pretests and posttests for each learning strand. View only."
      eyebrow="Strand Tests"
      phase="F6"
    />
  );
}

/** `/facilitator-tests/:testId` */
export function FacilitatorTestDetail(props: PageProps) {
  const { testId } = useParams();
  return (
    <Placeholder
      {...props}
      currentPage="facilitator-tests"
      title="Strand Test"
      subtitle={`Test ${testId}`}
      eyebrow="Strand Tests"
      phase="F6"
    />
  );
}

/** `/facilitator-cohorts` */
export function FacilitatorCohorts(props: PageProps) {
  return (
    <Placeholder
      {...props}
      currentPage="facilitator-cohorts"
      title="My Cohorts"
      subtitle="The cohorts you are assigned to, with their rosters."
      eyebrow="My Cohorts"
      phase="F5"
    />
  );
}
