from app.core.exceptions import StrandTestNotFoundError
from app.enums.attempt import AttemptStatus
from app.enums.strand_test import StrandTestType
from app.repositories.strand_test import StrandTestRepository
from app.schemas.strand_test import (
    StrandTestItemOptionResponse,
    StrandTestItemWithOptionsResponse,
    StrandTestResponse,
    StrandTestWithAttemptStatus,
    StrandTestWithAttemptStatusResponse,
    StrandTestWithItemsResponse,
)
from app.services.learner import LearnerService
from app.storage import get_read_url


class StrandTestService:
    def __init__(
        self,
        test_repository: StrandTestRepository,
        learner_service: LearnerService,
    ):
        self._test_repository = test_repository
        self._learner_service = learner_service

    async def get_by_type_with_attempt_status(
        self, user_id: int, test_type: StrandTestType
    ) -> StrandTestWithAttemptStatusResponse:
        learner = await self._learner_service.get_by_user_id(user_id)

        # Contains [(StrandTest, LearningStrand, StrandTestAttempt)...]
        tests_consolidated = await self._test_repository.get_by_type_with_attempt(
            learner.id, test_type
        )

        # Iterate through consolidated tests, format it, then put in tests
        tests = []

        for data in tests_consolidated:
            test, strand, test_attempt = data

            tests.append(
                StrandTestWithAttemptStatus(
                    test_id=test.id,
                    title=test.title,
                    image_url=test.image_url,
                    strand_id=strand.id,
                    strand_code=strand.code,
                    strand_name=strand.name,
                    attempt_status=(
                        AttemptStatus.COMPLETED
                        if test_attempt is not None
                        else AttemptStatus.PENDING
                    ),
                )
            )

        return StrandTestWithAttemptStatusResponse(tests=tests)

    async def get_by_id(
        self,
        test_id: int,
        include_items: bool,
    ) -> StrandTestResponse | StrandTestWithItemsResponse:
        """
        Get a single test by ID.

        If include_items is True, includes Test Item and Options.
        Else return Test information only.
        """

        """
        {
            test_information...
            items: [
                {

                }
            ]
        }
        """

        if include_items:
            consolidated_data = await self._test_repository.get_by_id_with_items(
                test_id
            )  # Returns [(StrandTest, StrandTestItem, StrandTestOption), ...]

            if not consolidated_data:
                raise StrandTestNotFoundError()
            
            #  Initialized a temporary dictionary for items with options. This facilitates pydantic model intialization
            items_with_options_dict = {}

            for data in consolidated_data:
                _, item, option, asset = data

                if item.id not in items_with_options_dict:
                    items_with_options_dict[item.id] = {
                        "item_id": item.id,
                        "question_text": item.question_text,
                        "options": [],
                    }

                items_with_options_dict[item.id]["options"].append(
                    StrandTestItemOptionResponse(
                        option_id=option.id,
                        option_text=option.option_text,
                    )
                )

                if asset is not None:
                    items_with_options_dict[item.id]["asset_url"] = get_read_url(asset.file_key, 3600)

            # Iterate through the temporary item dictionary values and create an item object for each item.
            items = []

            for item in items_with_options_dict.values():
                items.append(
                    StrandTestItemWithOptionsResponse(
                        item_id=item.get("item_id"),
                        question_text=item.get("question_text"),
                        options=item.get("options"),
                        asset_url=item.get("asset_url")
                    )
                )

            # Create the test object
            test = consolidated_data[0][0]

            return StrandTestWithItemsResponse(
                test_id=test.id,
                strand_id=test.strand_id,
                title=test.title,
                image_url=test.image_url,
                type=test.type,
                items=items,
            )

        else:
            test = await self._test_repository.get_by_id(test_id)

            if test is None:
                raise StrandTestNotFoundError()

            return StrandTestResponse.model_validate({
                "test_id": test.id,
                "strand_id": test.strand_id,
                "title": test.title,
                "image_url": test.image_url,
                "type": test.type,
            })
