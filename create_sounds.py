import wave
import math
import struct


def create_sound(filename, frequency, duration, volume=0.5):
    sample_rate = 44100
    samples = int(sample_rate * duration)

    with wave.open(filename, "w") as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(sample_rate)

        for i in range(samples):
            t = i / sample_rate
            value = int(
                32767
                * volume
                * math.sin(2 * math.pi * frequency * t)
            )

            sound.writeframes(
                struct.pack("<h", value)
            )


create_sound(
    "assets/sounds/jump.wav",
    700,
    0.12
)

create_sound(
    "assets/sounds/score.wav",
    1000,
    0.12
)

create_sound(
    "assets/sounds/game_over.wav",
    250,
    0.5
)

print("Sound files created successfully.")