"""
Copyright (C) 2025 drd <drd.ltt000@gmail.com>

This file is part of TunEd.

TunEd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TunEd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import copy
import sys
import time
from datetime import timedelta
from threading import Thread

import sounddevice  # for silence PyAudio()

import numpy as np
from pyaudio import PyAudio, paInt16


class AudioAnalyzer(Thread):

    ZERO_PADDING = 3  # times the buffer length
    NUM_HPS = 3  # Harmonic Product Spectrum

    def __init__(self,
                 queue,
                 ref_freq=440,
                 detection='note',
                 sampling_rate=48000,
                 chunk_size=1024,
                 buffer_times=50,
                 *args,
                 **kwargs):
        Thread.__init__(self, *args, **kwargs)

        self.queue = queue
        self.detection = detection
        self.ref_freq = ref_freq
        # https://en.wikipedia.org/wiki/Sampling_(signal_processing)
        self.SAMPLING_RATE = sampling_rate  # 44100, 48000, 96000
        self.CHUNK_SIZE = chunk_size  # 256  # 512  # 1024  # number of samples
        self.BUFFER_TIMES = buffer_times  # 12  # 25  # 50  # buffer length = CHUNK_SIZE * BUFFER_TIMES

        self.buffer = np.zeros(self.CHUNK_SIZE * self.BUFFER_TIMES)
        self.hanning_window = np.hanning(len(self.buffer))
        # self.hamming_window = np.hamming(len(self.buffer))
        self.running = False

        try:
            self.audio_object = PyAudio()
            self.stream = self.audio_object.open(
                format=paInt16,
                channels=1,
                rate=self.SAMPLING_RATE,
                input=True,
                output=False,
                frames_per_buffer=self.CHUNK_SIZE
            )
        except Exception as e:
            sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))
            return

    @staticmethod
    def frequency_to_midi(frequency, ref_freq):
        """
        Converts a frequency into a MIDI note.
        Rounds to the closest midi note.

        :param frequency:
        :param ref_freq:
        :return:
        """
        if frequency == 0:
            return 0

        midi_note = int(round(69 + (12 * np.log2(frequency / ref_freq)) / np.log2(2)))

        return midi_note

    @staticmethod
    def midi_to_frequency(midi_note, ref_freq):
        """
        Converts a MIDI note into frequency.

        :param midi_note:
        :param ref_freq:
        :return:
        """
        frequency = ref_freq * 2.0**((midi_note - 69) / 12.0)

        return frequency

    @staticmethod
    def midi_to_ansi_note(midi_note):
        """
        Returns the Ansi Note name for a midi number.

        :param midi_note:
        :return:
        """
        if midi_note == 0:
            return "-", 0

        notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        num_notes = len(notes)

        note_name = notes[int((midi_note - 21) % num_notes)]
        note_number = (midi_note - 12) // num_notes

        return note_name, note_number

    # TODO
    @staticmethod
    def ainsi_note_to_midi(ainsi_note):
        """

        :param ainsi_note:
        :return:
        """
        pass

    def compute_frequency_offset(self, frequency, midi_note):
        """
        Compute offset in cent.

        :param frequency:
        :param midi_note:
        :return:
        """
        nearest_midi_note_frequency = self.midi_to_frequency(midi_note, self.ref_freq)
        frequency_offset = nearest_midi_note_frequency - frequency

        next_note = midi_note
        if frequency_offset > 0:
            next_note += 1
        elif frequency_offset < 0:
            next_note -= 1
        semitone_step = abs((nearest_midi_note_frequency - self.midi_to_frequency(next_note, self.ref_freq)) / 100)

        offset = round(frequency_offset/semitone_step)

        return offset

    def note_detection(self, magnitude_data, frequencies):
        # put the frequency of the loudest tone into the queue
        magnitude = np.max(magnitude_data)
        magnitude_to_db = 10 * np.log10(magnitude / 32768)  # reference value used for dBFS scale. 32768 for int16 and 1 for float
        index_loudest = np.argmax(magnitude_data)
        frequency = round(frequencies[index_loudest], 2)
        phase = np.angle(magnitude)
        midi_note = self.frequency_to_midi(frequency, self.ref_freq)
        note, octave = self.midi_to_ansi_note(midi_note)
        offset = self.compute_frequency_offset(frequency, midi_note)

        sound = {
            'magnitude': magnitude,
            'magnitude_to_db': 0 if np.isnan(magnitude_to_db) else magnitude_to_db,
            'phase': phase,
            'frequency': frequency,
            'note': note,
            'octave': octave,
            'offset': offset
        }

        return sound

    def run(self):

        self.running = True

        while self.running:
            try:
                # execution time
                start_time = time.perf_counter()

                # read microphone data
                frame = self.stream.read(self.CHUNK_SIZE)
                decoded_frame = np.frombuffer(frame, dtype=np.int16)

                # append data to audio buffer
                self.buffer[:-self.CHUNK_SIZE] = self.buffer[self.CHUNK_SIZE:]
                self.buffer[-self.CHUNK_SIZE:] = decoded_frame

                # apply the fourier transformation on the whole buffer (with zero-padding + hanning window)
                pad = np.pad(self.buffer * self.hanning_window, (0, len(self.buffer) * self.ZERO_PADDING), "constant")
                fft = np.fft.fft(pad)
                magnitude_data = abs(fft)

                # only use the first half of the fft output data
                magnitude_data = magnitude_data[:int(len(magnitude_data) / 2)]

                # HPS: multiply data by itself with different scalings (Harmonic Product Spectrum)
                magnitude_data_orig = copy.deepcopy(magnitude_data)
                for i in range(2, self.NUM_HPS + 1, 1):
                    hps_len = int(np.ceil(len(magnitude_data) / i))
                    magnitude_data[:hps_len] *= magnitude_data_orig[::i]  # multiply every i element

                # get the corresponding frequency array
                frequencies = np.fft.fftfreq(int((len(magnitude_data) * 2) / 1), 1. / self.SAMPLING_RATE)

                sound = self.note_detection(magnitude_data, frequencies)
                sound['execution_time'] = timedelta(seconds=time.perf_counter() - start_time).total_seconds()

                # display
                self.queue.put(sound)

            except Exception as e:
                sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))

    def stop(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio_object.terminate()
