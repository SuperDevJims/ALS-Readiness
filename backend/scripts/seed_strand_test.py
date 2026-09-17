# This script seeds strand tests (pretest and posttest per strand),
# along with their items and item options.
# Scope: LS1-EN, LS1-FIL, LS3 only, per thesis Delimitation.
#
# Item content sourced from: Practice Test for A&E Test (Junior High School
# Level), Bureau of Alternative Education (BAE), 2024 — as reproduced in the
# ALS Pre-Test / Post-Test Form (Part III) and cross-checked against the
# accompanying answer key. Per the study design, pretest and posttest use
# the SAME item set (post-test is administered after TRIBEv2-informed
# stimulus content delivery, using identical items for comparability), so
# each strand's item list is defined once and reused for both.
#
# Run 'uv run python -m scripts.seed_strand_test'.

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.models.strand_test import StrandTest, StrandTestItem, StrandTestItemOption
from app.models.test_item_asset import TestItemAsset
from app.repositories.learning_strand import LearningStrandRepository
from app.repositories.strand_test import StrandTestRepository
from app.repositories.strand_test_item import StrandTestItemRepository
from app.repositories.strand_test_item_option import StrandTestItemOptionRepository
from app.repositories.test_item_asset import TestItemAssetRepository

# Each strand gets ONE pretest and ONE posttest, built from the same item
# set. Each item has options with exactly one marked is_correct=True.

_LS1_EN_ITEMS = [
    {
        "question_text": (
            "Elsa was tickled pink when her boyfriend surprised her with a "
            "marriage proposal on her birthday. What does the underlined "
            "phrase mean?"
        ),
        "items": [
            ("anxious", False),
            ("confused", False),
            ("happy", True),
            ("lucky", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Kevin accused us of stealing his phone until he found it. Although "
            "he realized his mistake, he was trying to sweep it under the rug. "
            "What does the underlined expression mean?"
        ),
        "items": [
            ("Clean the floor.", False),
            ("Make up for his mistake.", False),
            ("Hide his phone under the rug.", False),
            ("Pretend that the incident never happened.", True),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Which of the following statements implies the negative effects of "
            "traffic jams in the paragraph?"
        ),
        "items": [
            ("Road accidents lead to road rage.", False),
            ("Road accidents cause traffic jams.", False),
            (
                "Hassles of traffic cause chronic stress and low productivity.",
                True,
            ),
            (
                "The productivity of employees depends on their short temper.",
                False,
            ),
        ],
        "asset": {
            "key": "test-assets/9d178c14-4564-44af-8e49-7e6d3bdbe9b9_en-01.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": "What is the main cause of the failure?",
        "items": [
            ("He made late requests.", False),
            ("He did trivial tasks first.", False),
            ("He did not plan right away.", True),
            ("His output was not yet edited.", False),
        ],
        "asset": {
            "key": "test-assets/4a499882-6d7d-4873-ab8a-88f671c8d63e_en-02.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": "What event is most likely to occur next?",
        "items": [
            ("He took a shower because he was dirty.", False),
            ("Mang Danny returned and closed the barn.", False),
            (
                "Animals stayed inside the barn, and no one came out.",
                False,
            ),
            (
                "The animals went out because the door was not locked.",
                True,
            ),
        ],
        "asset": {
            "key": "test-assets/cde03220-a11e-4418-9b7a-0ca5ba7dffbb_en-03.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": (
            "The story of \u201cIbong Adarna\u201d revolves around the three "
            "princes who vie for the throne and kingship, and are trained in "
            "sword fighting and combat. The most courageous one would inherit "
            "the throne.\n\nUnder what literary form does the story belong?"
        ),
        "items": [
            ("epic", True),
            ("drama", False),
            ("novel", False),
            ("prose", False),
        ],
        "asset": None,
    },
    {
        
        "question_text": (
            "Which literary form is written in an ordinary, non-metrical "
            "language and communicates facts or opinions about reality?"
        ),
        "items": [
            ("play", False),
            ("story", False),
            ("fiction", False),
            ("non-fiction", True),
        ],
        "asset": None,
    },
    {
        "question_text": "What is the topic sentence of the paragraph?",
        "items": [
            (
                ("It allows individuals to prioritize tasks, set achievable "
                "goals, and allocate time efficiently."),
                False,
            ),
            (
                ("Effective time management is crucial for success in both "
                "personal and professional life."),
                True,
            ),
            (
                ("Using tools such as calendars and to-do lists can help "
                "individuals stay on track and meet deadlines."),
                False,
            ),
            (
                ("Ultimately, mastering time management leads to a more "
                "balanced life and improved overall well-being."),
                False,
            ),
        ],
        "asset": {
            "key": "test-assets/daa546eb-5cbd-42ee-8f33-267abe265041_en-04.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": (
            "Which of the following sentences provides additional information "
            "about the benefits of effective time management?"
        ),
        "items": [
            (
                "Mastering time management requires practice and dedication over time.",
                False,
            ),
            (
                ("People can feel overwhelmed when they have too many "
                "tasks to complete."),
                False,
            ),
            (
                ("By organizing their schedules, people can minimize "
                "stress and increase productivity."),
                True,
            ),
            (
                ("Effective time management allows individuals to take "
                "breaks and enjoy leisure activities."),
                False,
            ),
        ],
        "asset": {
            "key": "test-assets/daa546eb-5cbd-42ee-8f33-267abe265041_en-04.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": (
            "How will the sentences above be properly sequenced to make up a "
            "story?"
        ),
        "items": [
            ("1-2-4-3", True),
            ("2-1-3-4", False),
            ("3-4-1-2", False),
            ("4-3-2-1", False),
        ],
        "asset": {
            "key": "test-assets/e9165dc2-04c8-4169-b877-7e65e37acc18_en-05.png",
            "content_type": "image/png"
        },
    },
    {
        
        "question_text": (
            "He was a walking encyclopedia.\n\n"
            "What figure of speech is used in the sentence above?"
        ),
        "items": [
            ("hyperbole", False),
            ("metaphor", True),
            ("oxymoron", False),
            ("simile", False),
        ],
        "asset": None,
    },
    {
        
        "question_text": (
            "What should the applicant do if he wants to respond to the "
            "advertisement above?"
        ),
        "items": [
            ("visit the place during weekends", False),
            ("call the given number during weekends", False),
            ("call the given number during weekdays", True),
            ("submit resume in person between 8:00 - 5:00 pm", False),
        ],
        "asset": {
            "key": "test-assets/3f41dd02-6231-44aa-a374-fef3a4f8db3d_en-06.jpg",
            "content_type": "image/jpeg",
        },
    },
    {
        
        "question_text": (
            "Alvin obtained his Community Tax Certificate (cedula) in Puerto "
            "Princesa, Palawan. Where should the information \u201cPuerto "
            "Princesa, Palawan\u201d be placed in the form given above?"
        ),
        "items": [
            ("place of issue", True),
            ("home address", False),
            ("place of birth", False),
            ("date issued", False),
        ],
        "asset": {
            "key": "test-assets/1636f180-06f8-4551-ac54-cc3784dab563_en-07.jpg",
            "content_type": "image/jpeg"
        },
    },
    {
        
        "question_text": (
            "Gina B. Toledo was born in Bangkok, Thailand on October 12, 1990, "
            "but moved to the Philippines in 1995 and is now a Filipino "
            "citizen. What will she check on item 8A in the passport "
            "application above?"
        ),
        "items": [
            ("by birth", False),
            ("by election", False),
            ("by legislation", False),
            ("by naturalization", True),
        ],
        "asset": {
            "key": "test-assets/d41cba04-125a-4268-8410-7cd1d188cd20_en-08.jpg",
            "content_type": "image/jpeg"
        },
    },
    {
        
        "question_text": "How will she write her birth date in the application form?",
        "items": [
            ("Oct/12/90", False),
            ("Oct/12/1990", False),
            ("12/Oct/1990", True),
            ("12/Oct/90", False),
        ],
        "asset": {
            "key": "test-assets/d41cba04-125a-4268-8410-7cd1d188cd20_en-08.jpg",
            "content_type": "image/jpeg"
        },
    },
    {
        "question_text": (
            "Based on the story, what is the correct sequence of the events "
            "listed above?"
        ),
        "items": [
            ("1-4-2-3", False),
            ("1-4-3-2", True),
            ("2-4-3-1", False),
            ("4-2-1-3", False),
        ],
        "asset": {
            "key": "test-assets/9eae1531-ef5b-481e-9584-d42054db5d51_en-09.png",
            "content_type": "image/png"
        },
    },
    {
        
        "question_text": (
            "From the popular English proverb, \u201cA journey of a thousand "
            "miles begins with a single step\u201d, what does the message "
            "imply?"
        ),
        "items": [
            ("Accept difficulties during travel.", False),
            ("It takes patience to reach success.", False),
            ("A journey can take forever to achieve.", False),
            ("Begin something if one hopes to finish it.", True),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Which sentences are relevant to the claim that more people are "
            "able to study today than in the past?"
        ),
        "items": [
            ("sentences 1, 2 and 4 only", False),
            ("sentences 3, 4 and 5 only", True),
            ("sentences 1, 2, 4 and 5 only", False),
            ("sentences 2, 3, 4 and 5 only", False),
        ],
        "asset": {
            "key": "test-assets/40fb07c0-42da-4196-9120-9661ea70de4f_en-10.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": (
            "Based from the selection, the phrase \u201cpotentially "
            "problematic\u201d may pertain to"
        ),
        "items": [
            ("addiction", True),
            ("confusion", False),
            ("loss of memory", False),
            ("withdrawal symptoms", False),
        ],
        "asset": {
            "key": "test-assets/ce94cff9-b5cc-4a80-9466-b8c6ed49ed68_en-11.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": "Cognitive skills imply",
        "items": [
            ("emotional abilities", False),
            ("mental abilities", True),
            ("physical abilities", False),
            ("social abilities", False),
        ],
        "asset": {
            "key": "test-assets/ce94cff9-b5cc-4a80-9466-b8c6ed49ed68_en-11.png",
            "content_type": "image/png",
        },
    },
]

_LS1_FIL_ITEMS = [
    {
        "question_text": (
            "Alin sa sumusunod ang nais iparating ng manunulat sa talatang "
            "nababasa sa itaas?"
        ),
        "items": [
            ("Bigyan natin ng panahon ang mga larong pisikal.", True),
            ("Sa internet ay makikita natin ang tunay na mundo.", False),
            ("Higit na makikilala natin ang ating sarili sa mata ng iba.", False),
            ("Magiging masaya tayo kung titigilan natin ang social media.", False),
        ],
        "asset": {
            "key": "test-assets/17734652-0d55-4fc9-8397-8fb105882e39_fil-01.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": "Anong katangian ng mga taga-Korea ang masasalamin sa pabula?",
        "items": [
            ("Mabait at matalino", False),
            ("Palatanong at magaling", False),
            ("Matulungin at makatarungan", True),
            ("Mapagpatawad at makatarungan", False),
        ],
        "asset": {
            "key": "test-assets/54b3e8de-fc7a-40bd-8b37-506ea9c188cb_fil-02.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": (
            "Pagkatapos ng paglulunsad ng proyektong \u201cKabataan, "
            "Kailangan Ka ng Barangay\u201d, pinuri ng kapitan ng barangay si "
            "Mariana. Nasunod daw nito ang mga hakbang sa pakikipanayam sa "
            "panauhing pandangal.\n\n"
            "Ano ang tamang pagkakaayos ng mga hakbang sa pakikipanayam?\n"
            "1. Magpasalamat sa kinakapanayam.\n"
            "2. Magtanong nang magalang sa kinakapanayam.\n"
            "3. Kilalanin ang taong kakapanayamin.\n"
            "4. Isulat nang maayos ang nakuhang impormasyon sa panayam."
        ),
        "items": [
            ("1, 4, 3, 2", False),
            ("2, 3, 4, 1", False),
            ("3, 1, 2, 4", True),
            ("4, 2, 1, 3", False),
        ],
        "asset": None,
    },
    {
        "question_text": "Anong saloobin ang ipinapahayag ni Dilma Rousef?",
        "items": [
            ("Ipinakikita ang kalakasan ng kababaihan.", False),
            ("Ikinukumpara ang kalagayan ng Brazil sa Pilipinas.", False),
            ("Ipinagpapalagay na wala nang solusyon ang ganitong suliranin.", False),
            (
                ("Ipinapahayag ang pagnanais na malutas ang suliranin ng "
                "kanilang bansa."),
                True,
            ),
        ],
        "asset": {
            "key": "test-assets/302e5a0b-f4c6-4335-8040-467a4536d408_fil-03.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": (
            "Ang gandang panlabas ay lumilipas subalit ang panloob na ganda "
            "ay nananatili, di nawawala.\n\n"
            "Ano ang ibig sabihin ng pahayag na ito?"
        ),
        "items": [
            ("Lumilipas din ang ganda ng loob.", False),
            ("Mapapanatili ang gandang panlabas.", False),
            ("Ang gandang panloob at panlabas ay laging magkasama.", False),
            (
                "Mas mabuting tingnan ang kalooban ng isang tao, kaysa ganda ng mukha.",
                True,
            ),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Dalawampung taon na po akong taxi driver. Hindi pa ganito ang "
            "Maynila. Ang daming naglalakad at abalang-abala. Noong araw, mas "
            "tahimik; kakaunti pa lang ang mga taxi driver, at "
            "di-masyadong maraming kotse at bus.\n\n"
            "Ano ang mensaheng nais ipabatid ng taxi driver?"
        ),
        "items": [
            ("Malaki na ang ipinagbago ng Maynila.", True),
            ("Magulo na ang Maynila noong araw pa.", False),
            ("Nagsasawa na siya sa pagiging taxi driver.", False),
            ("Hindi na kumikita ang mga taxi driver sa Maynila.", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Inatasan si Tricia ng kaniyang guro na pamunuan ang klase para "
            "sa pagsasagawa ng Tree Planting. Tumawag siya ng pulong para "
            "magplano ng mga dapat nilang gawin. Nakipagugnayan sila sa "
            "kapitan ng barangay at pagkatapos ay isinagawa na ang mga "
            "binalak nilang hakbang.\n\n"
            "Alin sa sumusunod ang tamang ayos ng mga hakbang sa pagsasagawa "
            "ng proyekto?\n"
            "1. Nagplano sila ng mga hakbang na gagawin.\n"
            "2. Nagsaya sila dahil naisagawa nang maayos ang proyekto.\n"
            "3. Tumawag sila ng pulong.\n"
            "4. Naisakatuparan nila ang nabuong proyekto.\n"
            "5. Nakipag-ugnayan sila sa kapitan ng barangay."
        ),
        "items": [
            ("3, 1, 5, 4, 2", True),
            ("3, 1, 5, 2, 4", False),
            ("2, 3, 4, 1, 5", False),
            ("1, 5, 3, 2, 4", False),
        ],
        "asset": None,
    },
    {
        "question_text": "Alin sa sumusunod ang may mapagkakatiwalaang batayan?",
        "items": [
            (
                ("Ang paglalagay ng barya sa ilalim ng lupa ay sinasabing "
                "nagdadala ng swerte."),
                False,
            ),
            (
                ("Ang pagtatanim ng bawang sa paligid ng mga bulaklak ay "
                "nakakapigil sa mga insekto."),
                False,
            ),
            (
                ("Ang pagsasalita sa mga halaman ay nakakatulong upang "
                "sila'y lumago nang mas mabilis."),
                False,
            ),
            (
                ("Ayon sa isang gardening book, ang wastong pagdidilig at "
                "paggamit ng tamang pataba ay mahalaga para sa magandang "
                "paglago ng mga halaman."),
                True,
            ),
        ],
        "asset": {
            "key": "test-assets/77036e4c-187a-49f9-80c8-76609db1ccc7_fil-04.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": (
            "Tuwing panahon ng eleksiyon, mahalaga ang papel na ginagampanan "
            "ng mga guro. Ang pagod nila ay walang katumbas na halaga, mula "
            "sa paghahanda ng mga kagamitan hanggang sa matapos ang "
            "bilangan. Kaya naman ang CNN Philippines ay nagbigay-pugay.\n\n"
            "Alin sa sumusunod na pangunahin at pantulong na kaisipan ang "
            "nagsasaad ng buod ng tekstong binasa?"
        ),
        "items": [
            ("Ipinalabas sa telebisyon ang pagbibigay pugay sa mga guro.", False),
            (
                "Mahalagang papel ang ginagampanan ng mga guro tuwing eleksiyon.",
                True,
            ),
            (
                "Nakararanas ng pagod at puyat kapag may eleksiyon ang mga guro.",
                False,
            ),
            (
                "Ang mga guro ang naghahanda ng mga kagamitan tuwing eleksiyon.",
                False,
            ),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Batay sa aklat na Panitikang Pandaigdig sa Filipino, ang "
            "salitang myth (mito) ay galing sa salitang Latin na mythos at sa "
            "salitang Griyego na muthos, na ang kahulugan ay"
        ),
        "items": [
            ("epiko", False),
            ("alamat", True),
            ("pabula", False),
            ("kuwento", False),
        ],
        "asset": None,
    },
    {
        "question_text": "Ano ang paksa ng tekstong binasa?",
        "items": [
            ("Kahalagahan ng paggamit ng blog", False),
            ("Halaga ng Facebook sa pakikipagkaibigan", False),
            ("Papel ng internet sa makabagong panahon", False),
            (
                "Layunin ng paggamit ng iba\u2019t ibang uri ng social media",
                True,
            ),
        ],
        "asset": {
            "key": "test-assets/c0ccc419-8e78-4d7e-91be-092723a22a87_fil-05.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": "Ano ang magiging wakas ng kuwento?",
        "items": [
            ("Babalewalain ng hari ang kasunduan.", False),
            ("Pamumunuan ni Khan ang buong kaharian.", False),
            (
                "Uuwi si Khan sa kanyang bayan at doon mamumuhay nang tahimik.",
                False,
            ),
            (
                ("Pakakasalan ni Khan ang Prinsesa at mapapasakanya ang "
                 "kalahati ng kaharian."),
                True,
            ),
        ],
        "asset": {
            "key": "test-assets/472f90c3-7b3c-4d0c-a524-0156907a776f_fil-06.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": (
            "\u201cNang tumuntong ako ng ikalabindalawang taong gulang, "
            "itinali na ako sa bahay. Ikinulong at pinagbawalang "
            "makipag-ugnayan sa mundong nasa labas ng bahay. Makikita ko "
            "lamang ang mundo kung kasama ko na ang mapapangasawang "
            "estranghero. Isang dikilalang lalaking pinili ng magulang "
            "ko.\u201d\n\n"
            "Mahihinuhang ang nagsasalita ay"
        ),
        "items": [
            ("punong-puno ng galit", False),
            ("sawang-sawa na sa kaniyang kalagayan", False),
            ("labis na pinangangalagaan ng magulang", False),
            ("walang kalayaang pumili ng mapapangasawa", True),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Ang France ay isang bansang nais puntahan ng marami. Naniniwala "
            "ang mga Pranses sa egalite o pagkakapantay-pantay na "
            "sumasagisag sa kanilang bansa.\n\n"
            "Ano ang nais ipahiwatig ng binasa?"
        ),
        "items": [
            ("Ang mamamayan ay dapat maging sunod-sunuran.", False),
            ("Huwag mamuhay nang hindi naibubuklod ng pinuno.", False),
            ("Ang mga Pranses ay may pantay-pantay na karapatan.", False),
            (
                "Karapatan ng mga tao na gawin ang anumang naisin nila.",
                True,
            ),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Sa kuwentong bayan ng Pilipinas na \u201cAng Kawayan\u201d ang "
            "natatanging puno na, bagamat mataas ay yumuyuko sa pag-ihip ng "
            "malakas na hangin.\n\n"
            "Anong katangian ng Pilipino ang masasalamin dito?"
        ),
        "items": [
            ("magalang", False),
            ("matapang", False),
            ("mapagpakumbaba", True),
            ("mapagpaumanhin", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Ayon sa Department of Social Welfare and Development (DSWD), "
            "mapanganib sa mga bata ang paglalaro ng mararahas na internet "
            "game lalo na\u2019t nasa murang isip pa lamang sila.\n\n"
            "Alin sa sumusunod ang angkop na ideya sa binasang pahayag?"
        ),
        "items": [
            ("Ipagbawal sa mga bata ang paggamit ng mga gadget.", False),
            (
                "Limitahan ang mga bata sa paglalaro ng mga internet game.",
                False,
            ),
            (
                "Dapat bantayan ng magulang kung ano ang nilalaro ng kanilang anak.",
                False,
            ),
            (
                "Huwag pabayaang maglaro ng mararahas na internet game ang mga bata.",
                True,
            ),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Alin sa sumusunod ang nagbibigay ng kumpletong kahulugan ng pahayag na nasa itaas?"
        ),
        "items": [
            ("Gawing kalakasan ang kahinaang mayroon tayo.", False),
            (
                "Bawat tao ay may kani-kaniyang katangian na dapat isaalang-alang.",
                False,
            ),
            (
                "Dapat pahalagahan at gamitin ang mga katangiang taglay ng bawat isa.",
                False,
            ),
            (
                ("Bawat isa ay may magkakaibang katangian na dapat "
                 "pahalagahan, at gamitin sa kabutihan."),
                True,
            ),
        ],
        "asset": {
            "key": "test-assets/9120b6bd-83cb-43a5-bf11-4ff270b438c2_fil-07.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": (
            "Nasa itaas ang mga hakbang sa paggawa ng simpleng \u2018project "
            "proposal\u2019. Ano ang wastong pagkasunod-sunod ng mga ito?"
        ),
        "items": [
            ("1, 2, 3, 4", False),
            ("2, 1, 4, 3", True),
            ("3, 4, 1, 2", False),
            ("4, 3, 2, 1", False),
        ],
        "asset": {
            "key": "test-assets/1481f41d-9590-4e4f-9dbf-24d637ce7618_fil-08.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": "Anong suliraning panlipunan ang dapat mabigyan ng solusyon, batay sa saknong na binasa?",
        "items": [
            ("pagkaalipin", True),
            ("diskriminasyon", False),
            ("kawalan ng katarungan", False),
            ("walang pagmamahal sa wika", False),
        ],
        "asset": {
            "key": "test-assets/029a05c2-f916-440e-8a78-a165f3e59433_fil-09.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": (
            "Ayon sa aklat na Introduction to Linguistics ni David Crystal, "
            'ang salitang "communication" ay nagmula sa Latin na '
            '"communicare," na nangangahulugang "to share" o '
            '"magbahagi." Paano ito nauugnay sa kasalukuyang layunin ng '
            "komunikasyon sa lipunan?"
        ),
        "items": [
            (
                "Ang komunikasyon ay ginagamit lamang sa pagsasalita ng maraming wika.",
                False,
            ),
            (
                "Ang komunikasyon ay ginagamit upang mapanatili ang lihim na impormasyon.",
                False,
            ),
            (
                "Ang komunikasyon ay isang paraan ng pagbabahagi ng kaalaman at ideya sa iba.",
                True,
            ),
            (
                "Ang komunikasyon ay ginagamit upang makipagtalo at makipagkompetisyon sa iba.",
                False,
            ),
        ],
        "asset": None,
    },
]

_LS3_ITEMS = [
    {
        "question_text": "What kind of angle is formed if the clock shows 3:50?",
        "items": [
            ("Acute angle", False),
            ("Reflex angle", True),
            ("Right angle", False),
            ("Obtuse angle", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Which values of x will satisfy the absolute value equation x - 6 = 4?"
        ),
        "items": [
            ("10, 2", True),
            ("12, 4", False),
            ("14, 6", False),
            ("16, 8", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "A group of 1500 ALS completers needs to be surveyed to find out "
            "which academic track they would like to take in senior high "
            "school. For this survey, a 0.05 margin of error was considered "
            "for accuracy. Using Slovin\u2019s Formula, which of the "
            "following is the correct sample survey size?"
        ),
        "items": [
            ("313", False),
            ("314", False),
            ("315", False),
            ("316", True),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "The time to complete a project varies inversely with the number "
            "of employees. If three employees can complete the project in "
            "eight days, how long will it take for two employees to finish "
            "the project?"
        ),
        "items": [
            ("8 days", False),
            ("10 days", False),
            ("12 days", True),
            ("14 days", False),
        ],
        "asset": None,
    },
    {
        "question_text": "Which of the following functions has a graph of parallel lines?",
        "items": [
            ("g(x) = \u00bdx - 4 and h(x) = -2x + 2", False),
            ("f(x) = 3x + 3 and j(x) = 3x - 6", True),
            ("g(x) = \u00bdx - 4 and f(x) = 2x + 3", False),
            ("j(x) = 2x - 6 and h(x) = -2x + 2", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "The table above shows the lumber needed by Mang Lito. Using the "
            "formula, T x W x L \u00f7 12, where T is thickness, W is width "
            "and L is length, which size of lumber has the highest number of "
            "board feet needed by Mang Lito?"
        ),
        "items": [
            ("1\u201d x 2\u201d x 8\u201d", False),
            ("2\u201d x 2\u201d x 24\u201d", False),
            ("2\u201d x 4\u201d x 16\u201d", True),
            ("4\u201d x 4\u201d x 14\u201d", False),
        ],
        "asset": {
            "key": "test-assets/e5a45f63-7a11-4f4a-b679-9476f0992e34_math-01.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": (
            "A survey has been conducted on the preference of 200 women for "
            "healthy drink. The results of the survey were the following: "
            "100 preferred water infused with lemon; 90 preferred water "
            "infused with cucumber; 60 preferred water infused with lemon "
            "and cucumber.\n\n"
            "Based on the data given above, how many respondents preferred "
            "either lemon or cucumber?"
        ),
        "items": [
            ("70", True),
            ("75", False),
            ("80", False),
            ("85", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Kiko wanted to be at least 69 inches tall in height. At present, "
            "he is 56 inches tall in height. Which of the following "
            "mathematical statements represents the given situation?"
        ),
        "items": [
            ("56 + x \u2265 69 : x \u2265 13", True),
            ("56 \u2013 x \u2264 69 : x \u2264 13", False),
            ("69 + x < 56 : x > 13", False),
            ("69 \u2013 x > 56 : x < 13", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Which of the following statements correctly describe a "
            "population and a sample?\n"
            "I. A population is a group of persons or things that will be "
            "studied.\n"
            "II. A sample is a part of the population.\n"
            "III. A population is a part of the sample.\n"
            "IV. A sample is larger than the population to be studied."
        ),
        "items": [
            ("I and II only", True),
            ("I and IV only", False),
            ("II and III only", False),
            ("III and IV only", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Which of the following lines will be shown in the graph of the "
            "system of linear equations above?"
        ),
        "items": [
            ("Parallel lines", False),
            ("Coincident lines", True),
            ("Intersecting lines in the third quadrant", False),
            ("Intersecting lines in the second quadrant", False),
        ],
        "asset": {
            "key": "test-assets/6bc1a5c6-ee5a-4baa-b1a5-ab1bffc4b9e6_math-02.png", 
            "content_type": "image/png",
        },
    },
    {
        "question_text": (
            "Which of the following polynomials satisfies the given "
            "conditions?\n"
            "I. It consists of variables and coefficients.\n"
            "II. It involves the four fundamental operations.\n"
            "III. The exponents of variables are non-negative."
        ),
        "items": [
            ("4x\u00b9\u2070\u2070 + 6x\u2076 + 3x\u2074 + 8", False),
            ("2x\u00b2 + x\u207b\u2075 - 3x\u2074 + x\u207b\u00b3 + 3", False),
            ("\u221a(x\u2074 + 2x\u00b3 + 4)", False),
            ("(x\u00b2 - 3)/(x\u00b3 + 4x\u00b2) \u00d7 (x + 4)", True),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Joven\u2019s car tire exploded in his garage one afternoon. He "
            "knew the tire\u2019s pressure limit is 60 psi, but it had only a "
            "reading of 35 psi that morning, when the temperature was 20\u00b0C. "
            "If the tire pressure varies directly with its temperature, how "
            "hot did the tire get before it exploded?"
        ),
        "items": [
            ("11.7\u00b0C", False),
            ("34.3\u00b0C", True),
            ("60\u00b0C", False),
            ("105\u00b0C", False),
        ],
        "asset": None,
    },
    {
        "question_text": "Which of the following mathematical statements is correct?",
        "items": [
            ("(x\u00b3 + 2)(x \u2013 2) = x\u2074 \u2013 2x\u00b3 + 2x \u2013 4", True),
            ("(x\u00b3 - 2)(x \u2013 2) = x\u2074 \u2013 2x\u00b3 + 2x + 4", False),
            (
                "(3x\u00b3 + 2)(2x + 4) = 6x\u00b3 \u2013 12x\u00b2 \u2013 4x \u2013 8",
                False,
            ),
            ("(3x\u00b3 \u2013 2)(2x + 4) = 6x\u00b3 + 12x + 4x + 8", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "The King, Queen, and Jack of diamonds are removed from the deck "
            "of 52 playing cards. A card is drawn from the remaining cards "
            "after shuffling them. What is the probability of getting a "
            "diamond?"
        ),
        "items": [
            ("Three (3) out of 49", False),
            ("Three (3) out of 52", False),
            ("Ten (10) out of 49", True),
            ("Ten (10) out of 52", False),
        ],
        "asset": None,
    },
    {
        "question_text": "What are the 3 geometric means between 8 and 128?",
        "items": [
            ("16, 32, 64", True),
            ("24, 48, 72", False),
            ("40, 64, 80", False),
            ("40, 80, 120", False),
        ],
        "asset": None,
    },
    {
        "question_text": (
            "Based on the rules on exponents above, which of the following "
            "mathematical equations is correct?"
        ),
        "items": [
            ("(m\u00b3)(m\u00b2) = m\u00b2", False),
            ("m\u00b3/m\u00b2 = m\u2075", False),
            ("(m\u00b3)(m\u00b2) = m\u2075", True),
            ("(m\u00b3)\u00b2 = m\u2075", False),
        ],
        "asset": {
            "key": "test-assets/37108d10-8b44-4a19-a990-9a4eff03a8e9_math-03.png",
            "content_type": "image/png"
        },
    },
    {
        "question_text": (
            "Which of the following is described as its distance from zero "
            "to any point along the real number line?"
        ),
        "items": [
            ("absolute value", True),
            ("negative value", False),
            ("natural number", False),
            ("rational number", False),
        ],
        "asset": None,
    },
    {
        "question_text": "Which of the following are the factors of x\u2074 + 4x\u00b2 + 3?",
        "items": [
            ("(x + 1)(3x + 1)", False),
            ("(x\u00b2 \u2013 1)(x + 3)", False),
            ("(x\u00b2 + 3)(x\u00b2 + 1)", True),
            ("(x\u00b2 \u2013 3)(x\u00b2 \u2013 3)", False),
        ],
        "asset": None,
    },
    {
        "question_text": "What type of variation is illustrated in the table above?",
        "items": [
            ("combined", False),
            ("direct", False),
            ("inverse", True),
            ("joint", False),
        ],
        "asset": {
            "key": "test-assets/a5cef6f6-74d4-4d0a-8ac6-ed1e271d9c55_math-04.png",
            "content_type": "image/png",
        },
    },
    {
        "question_text": (
            "In how many ways can the letters of the word above be "
            "arranged, when no letter is repeated?"
        ),
        "items": [
            ("120", True),
            ("140", False),
            ("150", False),
            ("160", False),
        ],
        "asset": {
            "key": "test-assets/5bd733dc-8b60-4ee3-8a9f-a861df919aa1_math-05.png",
            "content_type": "image/png"
        },
    },
]


STRAND_TEST_DATA = {
    "LS1-EN": {
        "pretest": {"title": "LS1-EN Diagnostic Pre-test", "items": _LS1_EN_ITEMS},
        "posttest": {"title": "LS1-EN Post-test", "items": _LS1_EN_ITEMS},
    },
    "LS1-FIL": {
        "pretest": {"title": "LS1-FIL Diagnostic Pre-test", "items": _LS1_FIL_ITEMS},
        "posttest": {"title": "LS1-FIL Post-test", "items": _LS1_FIL_ITEMS},
    },
    "LS3": {
        "pretest": {"title": "LS3 Diagnostic Pre-test", "items": _LS3_ITEMS},
        "posttest": {"title": "LS3 Post-test", "items": _LS3_ITEMS},
    },
}


async def create_strand_tests(session: AsyncSession) -> list[StrandTest]:
    strand_repo = LearningStrandRepository(session)
    test_repo = StrandTestRepository(session)
    item_repo = StrandTestItemRepository(session)
    option_repo = StrandTestItemOptionRepository(session)
    asset_repo = TestItemAssetRepository(session)

    tests = []

    for code, test_types in STRAND_TEST_DATA.items():
        strand = await strand_repo.get_by_code(code)
        if not strand:
            print(f"Skipped - strand not found for code: {code}")
            continue

        for test_type, test_data in test_types.items():

            test = await test_repo.create(
                StrandTest(
                    strand_id=strand.id,
                    title=test_data["title"],
                    type=test_type,
                )
            )

            tests.append(test)
            print(f"Test created - code: {code}, type: {test_type}, id: {test.id}")

            
            for item in test_data["items"]:
                item_obj = await item_repo.create(
                    StrandTestItem(
                        test_id=test.id,
                        question_text=item["question_text"]
                    )
                )

                asset = item.get("asset")
                if asset is not None:
                    _ = await asset_repo.create(
                        TestItemAsset(
                            item_id=item_obj.id,
                            file_key=asset.get("key"),
                            content_type=asset.get("content_type"),
                        )
                    )

                for option_text, is_correct in item.get("items"):
                    _ = await option_repo.create(
                        StrandTestItemOption(
                            item_id=item_obj.id,
                            option_text=option_text,
                            is_correct=is_correct,
                        )
                    )

    return tests


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await create_strand_tests(session)


if __name__ == "__main__":
    asyncio.run(main())
