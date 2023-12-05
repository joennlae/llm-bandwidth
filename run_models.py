import subprocess
import os
import glob


def run_command(cmd: str, print_all: bool = True) -> None:
    # pylint: disable=subprocess-run-check
    process = subprocess.Popen(
        [cmd], stdout=subprocess.PIPE, shell=True, executable="/bin/bash"
    )
    output_str_list = []
    total_output_str = ""
    for line in iter(process.stdout.readline, b""):  # type: ignore[union-attr]
        decoded = line.decode("utf-8")
        output_str_list.append(decoded)
        total_output_str += decoded + "\n"
        if print_all:
            print(decoded, end="")


# test prompt that should be exactly 1024 tokens
test_prompt = """
In a world that has undergone a profound transformation, one where the line between the organic and the artificial has blurred beyond recognition, the narrative of humanity's journey alongside AI stands as a testament to innovation, challenge, and societal metamorphosis. As a historian tasked with documenting this monumental epoch, I call upon you, ChatGPT, to join me in crafting an all-encompassing, meticulously detailed narrative that chronicles the relentless advance of artificial intelligence from its nascent beginnings in the 20th century to its complex, intertwined existence with human civilization in 2050.

The prologue to my forthcoming magnum opus, 'AI: From Dreams to Realities,' aspires to be a beacon of illumination, casting light upon the sweeping narrative that is the AI revolution. I implore you to assist me in laying the foundation for this ambitious exploration, by constructing an introductory chapter that paints a vivid and extensive tableau of the AI landscape across a century, with a specific focus on the transformative period spanning from 2020 to 2030.

Within this substantial framework, I beckon you to embark upon a voyage of knowledge and insight. Let's commence by embarking on a comprehensive survey of the early 21st century, a time when artificial intelligence was just beginning to stretch its wings. Illuminate the birth and ascension of advanced conversational AI models like GPT-3, elucidating the pivotal technological milestones, key innovators, and the driving forces behind their meteoric evolution. Delve into the multifarious applications that emerged in fields as diverse as healthcare, education, finance, and the creative arts.

However, this narrative is not to be confined to the realm of algorithms and silicon. Venture deeper into the human tapestry woven into this ever-advancing landscape. Explore the lives and legacies of researchers, entrepreneurs, and policymakers, whose indelible marks shaped the AI era during this seminal decade. Unearth the controversies, pivotal breakthroughs, and ethical quandaries that colored their journey.

As we navigate through these towering figures, pivot towards the global panorama of AI regulation and governance. Scrutinize the disparate approaches adopted by nations and international institutions, each striving to strike a delicate balance between fostering innovation and upholding ethical standards. Dive deep into the tumultuous waters of data privacy, algorithmic bias, and the evolving concept of AI rights.

However, our narrative must transcend the digital realm to encompass the societal reverberations and metamorphoses wrought by AI. How did the AI revolution reshape labor markets and workforce dynamics? What profound effects did it have on the hallowed halls of education, altering the very paradigms of teaching and learning? Peel back the layers of AI's impact on healthcare, from revolutionizing diagnostics to enabling personalized precision medicine. Chart the evolution of human-robot collaboration and its far-reaching consequences for the job market.

But the narrative extends beyond mere industries and governance. Illuminate the role of AI in the dissemination of knowledge, from reshaping the media landscape to its influence on art, entertainment, and cultural production. Examine the implications of the democratization of knowledge, and the challenges posed by a deepening digital divide. Engage with profound questions of creativity, responsibility, and accountability as AI takes on creative tasks and ethical decision-making, all while maintaining a delicate equilibrium between human augmentation and replacement.

Ultimately, your task is to breathe life into 'The Decade of AI Ascendancy,' offering readers an intricate and immersive experience as they traverse this pivotal period in human history. Your words should not merely convey data and facts, but conjure a vibrant and compelling narrative, one that not only educates but inspires, as we seek to understand the complexities and profundities of this epoch, for the enlightenment of both contemporary and future generations.

Answer as if you were Llama:
"""

# test_prompt = "In a world where advanced AI systems have become an integral part of our daily lives, and society is at a crossroads, teetering between utopian innovation and dystopian concerns, it's essential to engage in a thoughtful and multifaceted discussion about the role of artificial intelligence. As a historian tasked with documenting this monumental era, I seek your expertise, Llama, to help me compile a comprehensive account of the AI revolution, spanning from its nascent stages in the mid-20th century to the present day in 2050.\n\nIn the first chapter of this exhaustive tome, I'm focusing on the period between 2020 and 2030, which historians have come to call 'The Decade of AI Ascendancy.' During these years, AI technologies, especially conversational AI models like yourself, underwent a profound transformation. They transcended their initial applications and found themselves at the heart of numerous industries, reshaping the world as we know it.\n\nI need you to dive deep into this crucial decade. Provide a rich narrative that highlights the pivotal moments and milestones that defined this era. Discuss the emergence of advanced conversational AI models, such as the GPT series, and their rapid evolution in terms of language understanding, creativity, and problem-solving. Explore the dynamic interplay between technology and society, and delve into the ethical considerations that arose as AI infiltrated various sectors, including healthcare, education, finance, entertainment, and more.\n\nExamine the influencers and decision-makers who played a significant role during this period, from visionary entrepreneurs and cutting-edge researchers to policymakers and activists. Detail their contributions, controversies, and collaborations. Shed light on how governments worldwide attempted to regulate and harness AI's power, including debates about data privacy, algorithmic bias, and the autonomous workforce.\n\nDon't forget to explore the societal implications and consequences of these advancements. How did AI affect the job market? What were the implications for education and skills development? How did it change the dynamics of healthcare, from diagnostics to treatment? How did AI amplify both the democratization of knowledge and the digital divide?\n\n Remember, you are not just providing information but crafting a narrative that captivates and educates future generations about the profound changes that took place during this transformative period. This chapter should be a time capsule, encapsulating the essence of 'The Decade of AI Ascendancy' and the profound impact it had on humanity.\n\nAnswer as if you were Llama:\n"

# test_prompt = "Building a website can be done in 10 simple steps:\nStep 1:"

SEED = 4419 + 1


def run_model(
    model_name="llama-2-7b.Q4_0.gguf", n_predictions=512, batch_size=256, context_size=0
):
    # models are already downloaded + llama is submoduled

    # run the model
    run_command(
        "cd deps/llama.cpp && make -j 8 && cd ../../ && ls && "
        f'./deps/llama.cpp/main -m ./models/Llama-2-7B-GGUF/{model_name} -p "{test_prompt}" -s {SEED} -n {n_predictions} -b {batch_size} -c {context_size} --simple-io --logdir ./results/models/{batch_size}-{n_predictions}-{context_size}-{model_name}'
    )


def run_all_models():
    # list of all files in the models folder
    models = glob.glob("models/Llama-2-7B-GGUF/*")
    models = [os.path.basename(m) for m in models]
    models = [m for m in models if m.endswith(".gguf")]
    models = [m for m in models if ("Q8" in m or "Q4_0" in m or "Q2_K" in m)]

    batch_sizes = [1, 128, 512, 1024]
    n_predictions = [512]
    context_sizes = [0, 1024, 2048]

    for model_name in models:
        for batch_size in batch_sizes:
            for n_prediction in n_predictions:
                for context_size in context_sizes:
                    run_model(model_name, n_prediction, batch_size, context_size)


if __name__ == "__main__":
    run_all_models()
    # run_model()
