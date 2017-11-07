from adapt.intent import IntentBuilder
import datetime
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.configuration import ConfigurationManager
from mycroft.util import (
    create_signal,
    check_for_signal
)

__author__ = 'reginaneon'
globdate = str(datetime.date.today())
config = ConfigurationManager.get()

LOGGER = getLogger(__name__)


class CPIKeepTranscriptionsSkill(MycroftSkill):
    """
            Class name: CPIKeepTranscriptionsSkill

            Purpose:  This skill allows the user to
            modify their audio and text recording permissions.
            Audio and text files are written to /var/log/mycroft.

            Note: Intent utterance example:
                user: 'Start/stop audio transcription'
                     or 'Start/stop audio recording'
                mycroft: "Should I start/stop audio transcription?"
                user: 'yes'
                mycroft: 'Audio Transcription Enabled.'
                or
                user: 'no'
                mycroft: 'O K. Not doing anything.'

        """

    def __init__(self):
        # name the new class:
        super(CPIKeepTranscriptionsSkill, self)\
            .__init__(name="CPIKeepTranscriptionsSkill")

    def initialize(self):
        # name intent and build it:
        permit_recording = IntentBuilder("PermitAudioRecording")\
            .require("Permit1")\
            .require("Recording2")\
            .require("Recording3")\
            .build()
        # register:
        self.register_intent(permit_recording, self.handle_permit_recording)

        deny_recording = IntentBuilder("DenyAudioRecording")\
            .require("Deny1")\
            .require("Recording2")\
            .require("Recording3")\
            .build()
        # register:
        self.register_intent(deny_recording, self.handle_deny_recording)

        permit_transcription = IntentBuilder("PermitAudioTranscription")\
            .require("Permit1")\
            .require("Transcription2")\
            .require("Transcription3")\
            .build()
        # register:
        self.register_intent(permit_transcription,
                             self.handle_permit_transcription)

        deny_transcription = IntentBuilder("DenyAudioTranscription")\
            .require("Deny1")\
            .require("Transcription2")\
            .require("Transcription3")\
            .build()
        # register:
        self.register_intent(deny_transcription,
                             self.handle_deny_transcription)

        self.confirm_yes = IntentBuilder("ConfirmYes") \
            .require("ConfirmYes") \
            .build()
        # register:
        self.register_intent(self.confirm_yes,
                             self.handle_confirm_yes)

        self.confirm_no = IntentBuilder("ConfirmNo") \
            .require("ConfirmNo") \
            .build()
        # register:
        self.register_intent(self.confirm_no,
                             self.handle_confirm_no)

        self.disable_intent('ConfirmYes')
        self.disable_intent('ConfirmNo')

    def handle_permit_recording(self, message):
        self.speak("Should I start audio recording?", True)

        self.enable_intent('ConfirmYes')
        self.enable_intent('ConfirmNo')

        create_signal('PermitAudioRecording')
        create_signal('WaitingToConfirm')

    def handle_deny_recording(self, message):

        self.speak("Should I stop audio recording?", True)

        self.enable_intent('ConfirmYes')
        self.enable_intent('ConfirmNo')

        create_signal('DenyAudioRecording')
        create_signal('WaitingToConfirm')

    def handle_permit_transcription(self, message):
        self.speak("Should I start audio transcription?", True)

        self.enable_intent('ConfirmYes')
        self.enable_intent('ConfirmNo')

        create_signal('PermitAudioTranscription')
        create_signal('WaitingToConfirm')

    def handle_deny_transcription(self, message):

        self.speak("Should I stop audio transcription?", True)

        self.enable_intent('ConfirmYes')
        self.enable_intent('ConfirmNo')

        create_signal('DenyAudioTranscription')
        create_signal('WaitingToConfirm')

    def handle_confirm_yes(self, message):

        if check_for_signal('PermitAudioRecording', 0):
            check_for_signal('keep_audio_permission', 0)
            create_signal('keep_audio_permission')
            self.speak("Audio Recording Enabled.", False)

        elif check_for_signal("DenyAudioRecording", 0):
            check_for_signal('keep_audio_permission', 0)
            self.speak("Audio Recording Disabled.", False)

        elif check_for_signal('PermitAudioTranscription', 0):
            check_for_signal('transcribe_text_permission', 0)
            create_signal('transcribe_text_permission')
            self.speak("Audio Transcription Enabled.", False)

        elif check_for_signal("DenyAudioTranscription", 0):
            check_for_signal('transcribe_text_permission', 0)
            self.speak("Audio Transcription Disabled.", False)

        self.disable_intent('ConfirmYes')
        self.disable_intent('ConfirmNo')

    def handle_confirm_no(self, message):
        self.speak("O K. Not doing anything.", False)

        self.disable_intent('ConfirmYes')
        self.disable_intent('ConfirmNo')

    def stop(self):
        pass


def create_skill():
    return CPIKeepTranscriptionsSkill()
