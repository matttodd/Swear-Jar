import speech_recognition as sr
import os
from twilio.rest import Client


class SwearJar:
    """
    Forward facing swear jar interface.
    """

    def __init__(self, recipient, source_number, bad_words=None, threshold=0.1):
        if bad_words is None:
            bad_words = {'balls': 0.01, 'cat': 0.02}
        self.threshold = threshold
        self.bad_words: dict = bad_words
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.1
        self.recognizer.phrase_threshold = 0.1
        self.recognizer.non_speaking_duration = 0.1

        self.mic = sr.Microphone()

        self.messenger = Client("REDACTED", "REDACTED")
        self.recipient = recipient
        self.twilio_number = source_number

    def start_rec(self):
        with self.mic as source:
            while True:
                audio = self.recognizer.listen(source)
                try:
                    phrase = self.recognizer.recognize_google(audio)
                    print(phrase)

                    bad_words_said = []
                    for word in phrase.split():
                        if word in self.bad_words:
                            bad_words_said.append(word)
                    if bad_words_said:
                        self.send_message(bad_words_said)
                except sr.UnknownValueError:
                    pass
                    # print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def send_message(self, words):
        total_cost = 0
        for word in words:
            total_cost += self.bad_words[word]

        message = "Your dirty boy said \'{}\'! Make sure you collect the ${:,.2f} they owe " \
                  "you!".format(", ".join(words), total_cost)
        print(message)
        self.messenger.messages.create(to=self.recipient, from_=self.twilio_number, body=message)


def main():
    client = SwearJar("REDACTED", "REDACTED")
    client.start_rec()


if __name__ == '__main__':
    main()
