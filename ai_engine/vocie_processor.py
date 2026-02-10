import speech_recognition as sr
from pydub import AudioSegment
import io
import streamlit as st


class VoiceTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_file):
        """무료 구글 STT 엔진을 사용하여 텍스트로 변환합니다."""
        try:
            # 1. 업로드된 파일을 pydub으로 읽기
            audio = AudioSegment.from_file(audio_file)

            # 2. WAV 포맷으로 변환 (구글 엔진 필수 조건)
            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)

            # 3. 음성 인식 진행
            with sr.AudioFile(wav_io) as source:
                audio_data = self.recognizer.record(source)
                # 구글 무료 API 사용 (한국어 설정)
                text = self.recognizer.recognize_google(audio_data, language="ko-KR")
                return text

        except Exception as e:
            return f"❌ 음성 인식 실패: {str(e)}\n(주의: 너무 긴 파일은 무료 API에서 거절될 수 있습니다.)"
