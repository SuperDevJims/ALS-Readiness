import type { ReactNode } from "react";
import { useParams } from "react-router";
import { Hammer } from "lucide-react";
import { AppLayout } from "../shared/AppLayout";
import type { PageProps } from "../../routes/ProtectedPage";
import { Card, EmptyState, PageHeader } from "./shared";

// Titled stand-ins for the facilitator screens that have no mockup yet
// (M05 frontend plan, Phase F0). Each is replaced by the real page in its own
// phase: Strand Tests in F6. (Learner Detail was replaced in F2 by
// FacilitatorLearnerDetail.tsx, Curriculum in F3 by FacilitatorCurriculum.tsx,
// My Cohorts in F5 by FacilitatorMyCohorts.tsx.) They hold no data, real or mock.

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
