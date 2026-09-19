import { STRAND_CODES, STRAND_SHORT_LABEL, isStrandCode } from "../../../lib/api/diagnostic";
import type {
  Gender,
  ParticipantIntake,
  ParticipantIntakeUpsert,
  StrandCode,
} from "../../../lib/api/types";

// Form state <-> API shape for the participant intake. Kept free of React so the
// conversions (notably strand codes) can be exercised on their own.

/** Form values as the inputs hold them: numbers and booleans are strings until submit. */
export interface IntakeFormState {
  age: string;
  sex: Gender | "";
  civil_status: string;
  highest_educational_attainment: string;
  /** Strand codes (LS1-EN / LS1-FIL / LS3) - never labels. */
  als_learning_strands: StrandCode[];
  als_enrollment_months: string;
  has_taken_ae_test: "" | "true" | "false";
  ae_test_attempt_count: string;
}

export const initialIntakeForm: IntakeFormState = {
  age: "",
  sex: "",
  civil_status: "",
  highest_educational_attainment: "",
  als_learning_strands: [],
  als_enrollment_months: "",
  has_taken_ae_test: "",
  ae_test_attempt_count: "0",
};

/** The strands a learner can pick, in display order: one per strand code. */
export const INTAKE_STRAND_OPTIONS: readonly { code: StrandCode; label: string }[] = STRAND_CODES.map((code) => ({
  code,
  label: `${STRAND_SHORT_LABEL[code]} (${code})`,
}));

/** Pre-fill the form from a saved intake. Saved strands that aren't in-scope codes are dropped. */
export function intakeFormFromIntake(intake: ParticipantIntake): IntakeFormState {
  return {
    age: String(intake.age),
    sex: intake.sex,
    civil_status: intake.civil_status,
    highest_educational_attainment: intake.highest_educational_attainment,
    als_learning_strands: intake.als_learning_strands.filter(isStrandCode),
    als_enrollment_months: String(intake.als_enrollment_months),
    has_taken_ae_test: intake.has_taken_ae_test ? "true" : "false",
    ae_test_attempt_count: String(intake.ae_test_attempt_count),
  };
}

/** Build the request body. Only real strand codes are sent. */
export function toIntakeUpsert(form: IntakeFormState): ParticipantIntakeUpsert {
  return {
    age: Number(form.age),
    sex: form.sex as Gender,
    civil_status: form.civil_status,
    highest_educational_attainment: form.highest_educational_attainment,
    als_learning_strands: form.als_learning_strands.filter(isStrandCode),
    als_enrollment_months: Number(form.als_enrollment_months),
    has_taken_ae_test: form.has_taken_ae_test === "true",
    ae_test_attempt_count: Number(form.ae_test_attempt_count),
  };
}
