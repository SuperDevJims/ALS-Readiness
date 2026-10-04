from typing import Annotated

from app.enums.content import ContentStatus, ContentType
from app.schemas.cohort import SchoolYear
from app.schemas.cohort_content import CohortContentCreate, CohortContentResponse
from app.schemas.facilitator_cohort import (
    FacilitatorCohortDetailResponse,
    FacilitatorCohortListResponse,
    FacilitatorSchoolYearsResponse,
)
from app.schemas.facilitator_content import (
    ContentLibraryDetailResponse,
    ContentLibraryItem,
    ContentLibraryListResponse,
    ContentLibraryStatus,
    ContentUpdate,
)
from app.schemas.facilitator_curriculum import (
    LessonCreate,
    LessonListResponse,
    LessonResponse,
    LessonUpdate,
    ModuleCreate,
    ModuleListResponse,
    ModuleResponse,
    ModuleUpdate,
    ReorderRequest,
    StrandItem,
    StrandListResponse,
)
from fastapi import APIRouter, Depends, Query, status

from ..deps import (
    CohortContentServiceDep,
    ContentLibraryServiceDep,
    CurrentFacilitatorDep,
    FacilitatorCohortServiceDep,
    LessonServiceDep,
    ModuleServiceDep,
    StrandServiceDep,
    get_current_facilitator,
)

router = APIRouter(
    prefix="/facilitator",
    tags=["Facilitator"],
    dependencies=[Depends(get_current_facilitator)],
)


# ================ Cohorts ================

@router.get("/school-years", response_model=FacilitatorSchoolYearsResponse)
async def get_my_school_years(
    current_user: CurrentFacilitatorDep,
    service: FacilitatorCohortServiceDep,
):
    return await service.get_school_years(current_user)


@router.get("/cohorts", response_model=FacilitatorCohortListResponse)
async def get_my_cohorts(
    current_user: CurrentFacilitatorDep,
    service: FacilitatorCohortServiceDep,
    school_year: SchoolYear | None = None,
):
    return await service.get_cohorts(current_user, school_year)


@router.get("/cohorts/{cohort_id}", response_model=FacilitatorCohortDetailResponse)
async def get_my_cohort(
    cohort_id: int,
    current_user: CurrentFacilitatorDep,
    service: FacilitatorCohortServiceDep,
):
    return await service.get_cohort_detail(current_user, cohort_id)


# ================ Content assignment ================

@router.post(
    "/cohorts/{cohort_id}/contents",
    status_code=status.HTTP_201_CREATED,
    response_model=CohortContentResponse,
)
async def assign_content(
    cohort_id: int,
    data: CohortContentCreate,
    current_user: CurrentFacilitatorDep,
    service: CohortContentServiceDep,
):
    return await service.assign(current_user, cohort_id, data.content_id)


@router.delete(
    "/cohorts/{cohort_id}/contents/{content_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unassign_content(
    cohort_id: int,
    content_id: int,
    current_user: CurrentFacilitatorDep,
    service: CohortContentServiceDep,
):
    await service.unassign(current_user, cohort_id, content_id)


# ================ Content library ================

@router.get("/contents", response_model=ContentLibraryListResponse)
async def get_library_contents(
    current_user: CurrentFacilitatorDep,
    service: ContentLibraryServiceDep,
    strand_id: int | None = None,
    module_id: int | None = None,
    lesson_id: int | None = None,
    type: ContentType | None = None,
    evaluated: bool | None = None,
    mine: bool = False,
    status: ContentLibraryStatus = "active",
    search: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return await service.get_list(
        current_user,
        status=ContentStatus(status),
        mine=mine,
        strand_id=strand_id,
        module_id=module_id,
        lesson_id=lesson_id,
        type=type,
        evaluated=evaluated,
        search=search,
        page=page,
        page_size=page_size,
    )


@router.get("/contents/{content_id}", response_model=ContentLibraryDetailResponse)
async def get_library_content(
    content_id: int,
    current_user: CurrentFacilitatorDep,
    service: ContentLibraryServiceDep,
):
    return await service.get_detail(current_user, content_id)


@router.patch("/contents/{content_id}", response_model=ContentLibraryItem)
async def update_library_content(
    content_id: int,
    data: ContentUpdate,
    current_user: CurrentFacilitatorDep,
    service: ContentLibraryServiceDep,
):
    return await service.update(current_user, content_id, data)


# ================ Strands and structure ================
# Structure is global per strand, not per cohort (D4), so no cohort check applies.

@router.get("/strands", response_model=StrandListResponse)
async def get_strands(service: StrandServiceDep):
    strands = await service.get_active_strands()
    items = [StrandItem.model_validate(strand) for strand in strands]
    return StrandListResponse(items=items, total=len(items))


@router.post(
    "/strands/{strand_id}/modules",
    status_code=status.HTTP_201_CREATED,
    response_model=ModuleResponse,
)
async def create_module(
    strand_id: int,
    data: ModuleCreate,
    current_user: CurrentFacilitatorDep,
    service: ModuleServiceDep,
):
    return await service.create(current_user, strand_id, data)


@router.put("/strands/{strand_id}/modules/order", response_model=ModuleListResponse)
async def reorder_modules(
    strand_id: int,
    data: ReorderRequest,
    service: ModuleServiceDep,
):
    modules = await service.reorder(strand_id, data.ids)
    items = [ModuleResponse.model_validate(module) for module in modules]
    return ModuleListResponse(items=items, total=len(items))


@router.patch("/modules/{module_id}", response_model=ModuleResponse)
async def update_module(
    module_id: int,
    data: ModuleUpdate,
    service: ModuleServiceDep,
):
    return await service.update(module_id, data)


@router.post(
    "/modules/{module_id}/lessons",
    status_code=status.HTTP_201_CREATED,
    response_model=LessonResponse,
)
async def create_lesson(
    module_id: int,
    data: LessonCreate,
    current_user: CurrentFacilitatorDep,
    service: LessonServiceDep,
):
    return await service.create(current_user, module_id, data)


@router.put("/modules/{module_id}/lessons/order", response_model=LessonListResponse)
async def reorder_lessons(
    module_id: int,
    data: ReorderRequest,
    service: LessonServiceDep,
):
    lessons = await service.reorder(module_id, data.ids)
    items = [LessonResponse.model_validate(lesson) for lesson in lessons]
    return LessonListResponse(items=items, total=len(items))


@router.patch("/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: int,
    data: LessonUpdate,
    service: LessonServiceDep,
):
    return await service.update(lesson_id, data)
