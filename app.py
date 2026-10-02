import gradio as gr

from text_validation import text_validation
from calling_model import analyze_text
from summary_length_validation import summary_length_validation

SUMMARY_BOUNDS = {
    'short': (1, 2),
    'medium': (3, 5),
    'long': (6, 10),
}

EXAMPLE_TEXT = """
Nikola Tesla (10 July 1856 – 7 January 1943) was a Serbian-American engineer, futurist, and inventor. He is known for his contributions to the design of the modern alternating current (AC) electricity supply system.

Born and raised in the Austro-Hungarian Empire, Tesla first studied engineering and physics in the 1870s without receiving a degree. He then gained practical experience in the early 1880s working in telephony and at Continental Edison in the new electric power industry. In 1884, he migrated to the United States, where he became a naturalized citizen. He worked for a short time at the Edison Machine Works in New York City before he struck out on his own. With the help of partners to finance and market his ideas, Tesla set up laboratories and companies in New York to develop a range of electrical and mechanical devices. His AC induction motor and related polyphase AC patents, licensed by Westinghouse Electric in 1888, earned him a considerable amount of money and became the cornerstone of the polyphase system, which Westinghouse marketed.

Tesla conducted a range of experiments with mechanical oscillators/generators, electrical discharge tubes, and early X-ray imaging among other things, in an attempt to develop inventions he could patent and market. He built a wirelessly controlled boat, one of the first wirelessly controlled vehicles ever produced. Tesla became well known as an inventor and demonstrated his achievements to celebrities and wealthy patrons at his lab. He was noted for his showmanship at public lectures. Throughout the 1890s, Tesla pursued his ideas for wireless lighting and worldwide wireless electric power distribution in his high-voltage, high-frequency power experiments in New York and Colorado Springs. In 1893, he made pronouncements on the possibility of wireless communication with his devices. Tesla tried to put these ideas to practical use in his unfinished Wardenclyffe Tower project, an intercontinental wireless communication and power transmitter, but ran out of funding before he could complete it.

After Wardenclyffe, Tesla experimented with a series of inventions in the 1910s and 1920s with varying degrees of success. Having spent most of his money, Tesla lived in a series of New York hotels, leaving behind unpaid bills. He died in New York City in January 1943. Tesla's work fell into relative obscurity following his death, until 1960, when the General Conference on Weights and Measures named the International System of Units (SI) measurement of magnetic flux density the tesla in his honor. There has been a resurgence in popular interest in Tesla since the 1990s. In 2013, Time magazine named him one of the 100 most significant figures of all time.
""".strip()


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


# ---------- Gradio glue ----------

def run(text: str, length: str):
    if not text or not text.strip():
        raise gr.Error("Paste some text first.")

    try:
        result = pipeline(text, length)
    except Exception as e:  # validation / retry failures -> toast in the UI
        raise gr.Error(str(e))

    if "error" in result:
        raise gr.Error(str(result["error"]))

    return (
        result.get("title", ""),
        result.get("main_topic", ""),
        result.get("sentiment", ""),
        result.get("summary", ""),
    )


with gr.Blocks(title="Text Summarizer") as demo:
    gr.Markdown("# Text Summarizer")

    with gr.Row():
        # Left side: input
        with gr.Column():
            text_in = gr.Textbox(label="Input text", lines=18, placeholder="Paste the text to summarize...")
            length_in = gr.Radio(["short", "medium", "long"], value="short", label="Summary length")
            submit_btn = gr.Button("Summarize", variant="primary")

        # Right side: output
        with gr.Column():
            title_out = gr.Textbox(label="Title", interactive=False)
            with gr.Row():
                topic_out = gr.Textbox(label="Main topic", interactive=False)
                sentiment_out = gr.Textbox(label="Sentiment", interactive=False)
            summary_out = gr.Textbox(label="Summary", lines=10, interactive=False)

    gr.Examples(examples=[[EXAMPLE_TEXT, "short"]], inputs=[text_in, length_in])

    submit_btn.click(
        fn=run,
        inputs=[text_in, length_in],
        outputs=[title_out, topic_out, sentiment_out, summary_out],
    )


if __name__ == "__main__":
    demo.launch()