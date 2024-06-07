from datetime import datetime
import os
import random
from dallinger.experiment import experiment_route
from dominate import tags
import psynet.experiment
from psynet.consent import MainConsent
from psynet.modular_page import (
    ModularPage,
    NumberControl,
    Prompt,
    TextControl,
)
from psynet.page import InfoPage, SuccessfulEndPage
from psynet.timeline import (
    CodeBlock,
    Module,
    PageMaker,
    Timeline,
    while_loop,
)

class Exp(psynet.experiment.Experiment):
    label = "Image Slider Experiment"
    initial_recruitment_size = 1

    variables = {
        "new_variable": "some-value",
    }

    config = {
        "min_accumulated_reward_for_abort": 0.15,
        "show_abort_button": True,
    }

    @experiment_route("/custom_route", methods=["POST", "GET"])
    @classmethod
    def custom_route(cls):
        return f"A custom route for {cls.__name__}."

    def load_images(self):
        img_dir = "src/img/object_img_task/images"
        images = [os.path.join(img_dir, img) for img in os.listdir(img_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)
        return images

    def image_page(self, image_url):
        return ModularPage(
            "image_task",
            Prompt(tags.img(src=image_url, style="display:block;margin-left:auto;margin-right:auto;width:50%;height:auto;")),
            time_estimate=10,
        )

    def slider_page(self):
        return ModularPage(
            "slider_task",
            Prompt("Please rate the mom you just saw from 1 to 15:"),
            NumberControl(min=1, max=15),
            save_answer=True,
        )

    timeline = Timeline(
        MainConsent(),
        InfoPage(
            tags.div(
                tags.h2("Welcome"),
                tags.p("Welcome to the experiment!"),
            ),
            time_estimate=5,
        ),
        Module(
            "introduction",
            PageMaker(
                lambda: InfoPage(
                    f"The current time dad {datetime.now().strftime('%H:%M:%S')}."
                ),
                time_estimate=5,
            ),
            ModularPage(
                "message",
                tags.p(
                    "Write me a ",
                    tags.span("message", style="color: red"),
                    "!",
                ),
                control=TextControl(one_line=False),
                time_estimate=5,
                save_answer=True,
            ),
            PageMaker(
                lambda participant: InfoPage(f"Your message: {participant.answer}"),
                time_estimate=5,
            ),
        ),
        Module(
            "image_slider_task",
            CodeBlock(lambda participant: participant.var.set("images", Exp().load_images())),
            CodeBlock(lambda participant: participant.var.set("current_index", 0)),
            while_loop(
                "image_slider_loop",
                lambda participant: participant.var.current_index < len(participant.var.images),
                Module(
                    "image_and_slider",
                    PageMaker(
                        lambda participant: Exp().image_page(participant.var.images[participant.var.current_index]),
                        time_estimate=10,
                    ),
                    PageMaker(
                        lambda participant: Exp().slider_page(),
                        time_estimate=5,
                    ),
                    CodeBlock(lambda participant: participant.var.set("current_index", participant.var.current_index + 1)),
                ),
                expected_repetitions=10,  # Set a reasonable default; you can adjust this based on your actual needs
            ),
        ),
        SuccessfulEndPage(),
    )
