from text_validation import text_validation
from calling_model import analyze_text
from summary_length_validation import summary_length_validation

SUMMARY_BOUNDS = {
    'short': (1, 2),
    'medium': (3, 5),
    'long': (6, 10),
}


text = """
Ancient Egypt was a cradle of civilization concentrated along the lower reaches of the Nile River in the eastern part of North Africa[1][2][3]. It emerged from prehistoric Egypt around 3150 BC (according to conventional Egyptian chronology),[4] when Upper and Lower Egypt were united by Menes, who is believed by the majority of Egyptologists to have been the same person as Narmer.[5] The history of ancient Egypt unfolded as a series of stable kingdoms interspersed by the "Intermediate Periods" of relative instability. These stable kingdoms existed in one of three periods: the Old Kingdom of the Early Bronze Age; the Middle Kingdom of the Middle Bronze Age; or the New Kingdom of the Late Bronze Age.

The pinnacle of ancient Egyptian power was achieved during the New Kingdom, which extended its rule to much of Nubia and a considerable portion of the Levant. After this period, Egypt entered an era of slow decline. Over the course of its history, it was invaded or conquered by a number of foreign civilizations, including the Hyksos, the Kushites, the Assyrians, the Persians, the Greeks and the Romans. The end of ancient Egypt is variously defined as occurring with the end of the Late Period during the Wars of Alexander the Great in 332 BC or with the end of the Greek-ruled Ptolemaic Kingdom during the Roman conquest of Egypt in 30 BC.[6] In AD 642, the Arab conquest of Egypt brought an end to the region's millennium-long Greco-Roman period.

The success of ancient Egyptian civilization came partly from its ability to adapt to the Nile's conditions for agriculture. The predictable flooding of the Nile and controlled irrigation of its fertile valley produced surplus crops which supported a more dense population and thereby substantial social and cultural development. With resources to spare, the administration sponsored the mineral exploitation of the valley and its surrounding desert regions, the early development of an independent writing system, the organization of collective construction and agricultural projects, trade with other civilizations, and a military to assert Egyptian dominance throughout the Near East. Motivating and organizing these activities was a bureaucracy of elite scribes, religious leaders, and administrators under the control of the reigning pharaoh, who ensured the cooperation and unity of the Egyptian people in the context of an elaborate system of religious beliefs.[7]

Among the many achievements of ancient Egypt are: the quarrying, surveying, and construction techniques that supported the building of monumental pyramids, temples, and obelisks; a system of mathematics; a practical and effective system of medicine; irrigation systems and agricultural production techniques; the first known planked boats;[8] Egyptian faience and glass technology; new forms of literature; and the earliest known peace treaty, which was ratified with the Anatolia-based Hittite Empire.[9] Its art and architecture were widely copied and its antiquities were carried off to be studied, admired, or coveted in the far corners of the world. Likewise, its monumental ruins inspired the imaginations of travelers and writers for millennia. A newfound European and Egyptian respect for antiquities and excavations that began in earnest in the early modern period has led to much scientific investigation of ancient Egypt and its society, as well as a greater appreciation of its cultural legacy.[10]
"""

length = 'long'


def pipeline(text: str, length: str, max_retries: int = 1):
    text_val = text_validation(text, length)
    min_s, max_s = SUMMARY_BOUNDS[text_val['length']]

    correction_message = None

    for attempt in range(max_retries + 1):
        summarizer = analyze_text(text_val, correction_feedback=correction_message)

        if "error" in summarizer:
            return summarizer


        sentence_count = len(summarizer['summary'])

        if min_s <= sentence_count <= max_s:

            summarizer['summary'] = " ".join(summarizer['summary'])
            

            summary_length_validation(summarizer['summary'], text_val['length'])
            return summarizer


        correction_message = (
            f"Your previous output was rejected because you gave {sentence_count} sentences, "
            f"need {min_s}–{max_s}. Ensure the `summary` array contains between "
            f"{min_s} and {max_s} discrete sentences."
        )

    raise ValueError(
        f"Failed after {max_retries} retry: Expected {min_s}–{max_s} sentences for '{length}', "
        f"received {sentence_count} sentences."
    )


app = pipeline(text, length)
print(app)