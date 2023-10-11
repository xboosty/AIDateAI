import argparse
import speech_recognition as sr
from conversations.conversations import Conversation
from transcription.transcription import Transcriptor
from files.files import Files

presentation = "Hello, I am the virtual assistant designed to conduct our interview with you."

conversation = Conversation(presentation, [])
transcriptor = Transcriptor()
files = Files()
path_audio = files.getConcatPathToRoot("audio_users_temp")

def createNewPresentation(presentation):
    conversation.setPresentation(presentation)
    
def speakMessage(message):
    conversation.speakAny(message)
    
def speakPresentation():
    conversation.speakPresentation()
    
def getTranscription(path_audio):
    return transcriptor.transcribe_audio_to_text(path_audio)
    
def main():
    parser = argparse.ArgumentParser(description="COMMAND API WITH PYTHON")
    subparsers = parser.add_subparsers(dest="function")
    
    # Subcomando: createNewPresentation
    parser_create = subparsers.add_parser("createNewPresentation")
    parser_create.add_argument("presentation", type=str, help="New presentation")

    # Subcomando: speakMessage
    parser_speak = subparsers.add_parser("speakMessage")
    parser_speak.add_argument("message", type=str, help="Message to speak")
    
    # Subcomando: speakPresentation
    parser_create = subparsers.add_parser("speakPresentation")

    # Subcomando: getTranscription
    parser_transcribe = subparsers.add_parser("getTranscription")
    parser_transcribe.add_argument("path_audio", type=str, help="Path to audio for text extraction")

    args = parser.parse_args()

    if args.function == "createNewPresentation":
        createNewPresentation(args.presentation)
    elif args.function == "speakMessage":
        speakMessage(args.message)
    elif args.function == "speakPresentation":
        speakPresentation()
    elif args.function == "getTranscription":
        result = getTranscription(args.path_audio)
        print(result)


if __name__ == "__main__":
    main()
