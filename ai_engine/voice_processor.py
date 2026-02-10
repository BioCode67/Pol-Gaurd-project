# ai_engine/voice_processor.py 전체 코드
import speech_recognition as sr
from pydub import AudioSegment
import io
import streamlit as st


class VoiceTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_file):
        """mp4를 포함한 다양한 파일에서 음성을 인식합니다."""
        try:
            # 1. 파일 확장자 확인
            file_extension = audio_file.name.split(".")[-1].lower()

            # 2. pydub으로 파일 로드 (mp4도 자동으로 오디오만 읽어옵니다)
            # format 인자를 지정하면 더 정확하게 읽어옵니다.
            audio = AudioSegment.from_file(audio_file, format=file_extension)

            # 3. WAV 포맷으로 변환 (Google STT 권장 포맷)
            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)

            # 4. 음성 인식 진행
            with sr.AudioFile(wav_io) as source:
                audio_data = self.recognizer.record(source)
                # 구글 무료 API 사용
                text = self.recognizer.recognize_google(audio_data, language="ko-KR")
                return text

        except Exception as e:
            return f"❌ 분석 실패: {str(e)}\n(mp4 파일의 경우 코덱 호환성이 필요할 수 있습니다.)"
