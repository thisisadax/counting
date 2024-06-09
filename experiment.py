import psynet.experiment
from psynet.consent import NoConsent # MainConsent
from psynet.modular_page import (
    ModularPage,
    NumberControl,
    ImagePrompt
)
from psynet.asset import CachedAsset, LocalStorage
from psynet.page import InfoPage, SuccessfulEndPage
from psynet.timeline import (
    Timeline,
)
from psynet.trial import compile_nodes_from_directory
from psynet.trial.static import StaticNode, StaticTrial, StaticTrialMaker
from psynet.utils import get_logger
import random
import os

logger = get_logger()
class CustomTrial(StaticTrial):
    time_estimate = 5
    def show_trial(self, experiment, participant):
        return ModularPage(
                "counting_page",
                ImagePrompt(self.assets['prompt'].url,
                            'How many objects were in the image?',
                            '25%',
                            '25%',
                            hide_after=0.2,
                            text_align='center'),
                NumberControl(),
                time_estimate=self.time_estimate
        )

class Exp(psynet.experiment.Experiment):
    label = 'Counting task'
    asset_storage = LocalStorage()
    timeline = Timeline(
        NoConsent(),
        InfoPage('We begin the counting task.', time_estimate=5),
        StaticTrialMaker(
            id_="counting",
            trial_class=CustomTrial,
            nodes=compile_nodes_from_directory(input_dir='src/experiment', media_ext='.png', node_class=StaticNode),
            target_n_participants=10,
            recruit_mode='n_participants',
            expected_trials_per_participant=100,
            max_trials_per_participant=100,
            choose_participant_group=lambda participant: random.choice(os.listdir('src/experiment')),
        ),
        SuccessfulEndPage()
    )