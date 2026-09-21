from fastapi import APIRouter

from .routes import (
    admin,
    auth,
    cohort_facilitators,
    cohort_learners,
    cohorts,
    lri_test,
    lri_test_attempt,
    participant_intake,
    strand_test,
    strand_test_attempt,
    users,
)

router = APIRouter(prefix="/api")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(admin.router)
router.include_router(strand_test_attempt.router)
router.include_router(strand_test.router)
router.include_router(lri_test_attempt.router)
router.include_router(lri_test.router)
router.include_router(participant_intake.router)
router.include_router(cohorts.router)
router.include_router(cohort_facilitators.router)
router.include_router(cohort_learners.router)
