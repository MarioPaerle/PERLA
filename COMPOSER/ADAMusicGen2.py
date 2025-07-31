import re
from mido import Message, MidiFile, MidiTrack
import random


class DrumMIDI:
    def __init__(self, resolution=480, beats_per_measure=4):
        # resolution: tick per battuta (quarter note)
        # beats_per_measure: numero di battute per misura (es. 4 per il 4/4)
        self.resolution = resolution
        self.beats_per_measure = beats_per_measure
        self.events = []  # Lista di eventi: (time_in_ticks, note, velocity, event_type)

    def add_event(self, time, note, velocity, event_type):
        """Aggiunge un evento alla timeline."""
        self.events.append((time, note, velocity, event_type))

    def note_to_midi(self, note_str):
        """
        Converte una stringa nota (es. 'c5' o 'c#4') in numero MIDI.
        Per esempio, 'c5' diventa 72.
        """
        note_str = note_str.lower()
        note_map = {'c': 0, 'c#': 1, 'd': 2, 'd#': 3, 'e': 4, 'f': 5,
                    'f#': 6, 'g': 7, 'g#': 8, 'a': 9, 'a#': 10, 'b': 11}
        m = re.match(r'([a-g]#?)(\d+)', note_str)
        if not m:
            raise ValueError("Formato nota non valido. Usa ad es. 'c5' o 'f#4'.")
        name, octave = m.groups()
        octave = int(octave)
        # Formula: (octave+1)*12 + semitono
        return (octave + 1) * 12 + note_map[name]

    def add_rhythm_pattern(self, start, end, subdivision, note, velocity=100,
                           shift=0, alternate_shift=False, random_shift=0, alternate_velocity=False):
        """
        Aggiunge un pattern ritmico:
          - start ed end sono in misure (es. start=0, end=16 per 16 misure)
          - subdivision è il valore in unità di misura; per esempio,
            in 4/4 un ottavo è 1/8 (perché 1 misura = 1 e un ottavo = 0.125)
          - note è la stringa (es. 'c5')
        Ogni nota viene "triggerata" e poi stoppata dopo una frazione della durata.
        """
        current = start
        note_number = self.note_to_midi(note)
        subdivision_ticks = subdivision * self.beats_per_measure * self.resolution
        duration_ticks = int(subdivision_ticks * 0)
        i = 1
        while current < end:
            i += 1
            if shift and alternate_shift:
                tick = int(current * self.beats_per_measure * self.resolution) + shift * (i % 2)

            else:
                tick = int(current * self.beats_per_measure * self.resolution) + shift + (
                    shift * 2 if random.random() < random_shift else -shift)
            self.add_event(tick, note_number,
                           velocity + (int(-velocity / 3) if (alternate_velocity and i % 2 == 1) else 0), 'note_on')
            self.add_event(tick + duration_ticks, note_number, 0, 'note_off')
            current += subdivision

    def add_pattern(self, pattern, start=0, subdivision=0.125):
        """
        Aggiunge un pattern ritmico:
          - start ed end sono in misure (es. start=0, end=16 per 16 misure)
          - subdivision è il valore in unità di misura; per esempio,
            in 4/4 un ottavo è 1/8 (perché 1 misura = 1 e un ottavo = 0.125)
          - note è la stringa (es. 'c5')
        Ogni nota viene "triggerata" e poi stoppata dopo una frazione della durata.
        """
        current = start
        subdivision_ticks = subdivision * self.beats_per_measure * self.resolution
        duration_ticks = int(subdivision_ticks * 0)
        for i, (velocity, note) in enumerate(pattern):
            if note == 0:
                continue
            note_number = self.note_to_midi(note)
            tick = int(i * subdivision_ticks)
            self.add_event(tick, note_number, int(velocity), 'note_on')
            self.add_event(tick + duration_ticks, note_number, 0, 'note_off')
            current += subdivision

    def add_numeric_pattern(self, pattern, start=0, subdivision=0.125):
        """
        Aggiunge un pattern ritmico dato da una lista di tuple (velocity, note).
        Il parametro 'start' è il tempo d'inizio in misure.
        'subdivision' è la durata di ogni step in unità di misura.
        Ogni step occupa un intervallo fisso; qui la durata della nota è uguale all'intero step.
        """
        # Convertiamo il tempo d'inizio (in misure) in tick
        start_tick = int(start * self.beats_per_measure * self.resolution)
        # Calcoliamo quanti tick dura ogni subdivision
        subdivision_ticks = int(subdivision * self.beats_per_measure * self.resolution)
        duration_ticks = subdivision_ticks  # Puoi modificare questo valore se vuoi note più corte
        for i, (velocity, note) in enumerate(pattern):
            if note == 0:  # Salta gli step vuoti
                continue
            tick = start_tick + i * subdivision_ticks
            self.add_event(tick, note, velocity, 'note_on')
            self.add_event(tick + duration_ticks, note, 0, 'note_off')


    def add_fixednote_pattern(self, pattern, start=0, subdivision=0.125, note='c4'):
        """
        Aggiunge un pattern ritmico:
          - start ed end sono in misure (es. start=0, end=16 per 16 misure)
          - subdivision è il valore in unità di misura; per esempio,
            in 4/4 un ottavo è 1/8 (perché 1 misura = 1 e un ottavo = 0.125)
          - note è la stringa (es. 'c5')
        Ogni nota viene "triggerata" e poi stoppata dopo una frazione della durata.
        """
        current = start
        note_number = self.note_to_midi(note)
        subdivision_ticks = subdivision * self.beats_per_measure * self.resolution
        duration_ticks = int(subdivision_ticks * 0)
        for i, velocity in enumerate(pattern):
            if note == 0:
                continue
            tick = int(i * subdivision_ticks)
            self.add_event(tick, note_number, velocity, 'note_on')
            self.add_event(tick + duration_ticks, note_number, 0, 'note_off')
            current += subdivision

    def add_roll(self, bar, type_str, number_of_notes, mode='before_beat', note='c5', velocity=60):
        """
        Aggiunge un roll:
          - bar: numero di misura (1-indexed) dove inserire il roll.
          - type_str: stringa frazionaria, es. '1/12', che indica la durata di ogni nota in unità di misura.
          - number_of_notes: numero di note da inserire.
          - mode: 'before_beat' (il roll viene inserito appena prima dell'inizio della misura bar)
                   oppure 'after_beat' (appena dopo l'inizio della misura bar).
          - note: la nota da usare (default 'c5').
        La funzione calcola la posizione di partenza in base al mode:
          * before_beat: la prima nota del roll viene posizionata a (bar - number_of_notes * roll_interval)
            in modo che l'ultima nota arrivi esattamente al confine della misura.
          * after_beat: il roll inizia all'inizio della misura (bar-1).
        """
        # Calcola il roll_interval in unità di misura (1 misura = 1)
        num, den = type_str.split('/')
        roll_interval = int(num) / int(den)
        if mode == 'before_beat':
            # Target: l'inizio della misura "bar" (1-indexed)
            target_time = bar - 1
            start_time = target_time - number_of_notes * roll_interval
        elif mode == 'after_beat':
            target_time = bar - 1
            start_time = target_time
        else:
            raise ValueError("Mode non riconosciuto: usa 'before_beat' o 'after_beat'.")

        note_number = self.note_to_midi(note)
        duration_ticks = int((roll_interval * self.beats_per_measure * self.resolution) * 0)
        current = start_time
        for i in range(number_of_notes):
            tick = int(current * self.beats_per_measure * self.resolution) // 4
            if mode == 'before_beat':
                self.add_event(tick, note_number, velocity - velocity // 2 + velocity // 8 * i, 'note_on')
            elif mode == 'after_beat':
                self.add_event(tick, note_number, velocity - velocity // 8 * i, 'note_on')
            self.add_event(tick + duration_ticks, note_number, 0, 'note_off')
            current += roll_interval


    def add_decaying_roll(self, bar, type_str, number_of_notes, mode='before_beat', velocity=60):
        """
        Aggiunge un roll:
          - bar: numero di misura (1-indexed) dove inserire il roll.
          - type_str: stringa frazionaria, es. '1/12', che indica la durata di ogni nota in unità di misura.
          - number_of_notes: numero di note da inserire.
          - mode: 'before_beat' (il roll viene inserito appena prima dell'inizio della misura bar)
                   oppure 'after_beat' (appena dopo l'inizio della misura bar).
          - note: la nota da usare (default 'c5').
        La funzione calcola la posizione di partenza in base al mode:
          * before_beat: la prima nota del roll viene posizionata a (bar - number_of_notes * roll_interval)
            in modo che l'ultima nota arrivi esattamente al confine della misura.
          * after_beat: il roll inizia all'inizio della misura (bar-1).
        """
        # Calcola il roll_interval in unità di misura (1 misura = 1)
        num, den = type_str.split('/')
        roll_interval = int(num) / int(den)
        if mode == 'before_beat':
            # Target: l'inizio della misura "bar" (1-indexed)
            target_time = bar - 1
            start_time = target_time - number_of_notes * roll_interval
        elif mode == 'after_beat':
            target_time = bar - 1
            start_time = target_time
        else:
            raise ValueError("Mode non riconosciuto: usa 'before_beat' o 'after_beat'.")

        duration_ticks = int((roll_interval * self.beats_per_measure * self.resolution) * 0)
        current = start_time
        for i in range(number_of_notes):
            note_number = 65 - i
            tick = int(current * self.beats_per_measure * self.resolution) // 4
            if mode == 'before_beat':
                vel = int((velocity/number_of_notes) * i + 30)
                self.add_event(tick, note_number, max(0, min(vel, 127)), 'note_on')
            elif mode == 'after_beat':
                vel = int(velocity - (velocity/number_of_notes) * i + 30)
                self.add_event(tick, note_number, max(0, min(vel, 127)), 'note_on')
            self.add_event(tick + duration_ticks, note_number, 0, 'note_off')
            current += roll_interval

    def generate_midi(self, filename='output.mid'):
        """
        Genera e salva un file MIDI a partire dagli eventi inseriti.
        Gli eventi vengono ordinati in base al tempo e trasformati in delta time.
        """
        # Ordina gli eventi in ordine temporale
        self.events.sort(key=lambda e: e[0])
        mid = MidiFile(ticks_per_beat=self.resolution)
        track = MidiTrack()
        mid.tracks.append(track)
        current_tick = 0
        for tick, note, velocity, event_type in self.events:
            delta = tick - current_tick
            current_tick = tick
            if event_type == 'note_on':
                track.append(Message('note_on', note=note, velocity=max(0, min(velocity, 127)), time=delta))
            elif event_type == 'note_off':
                track.append(Message('note_off', note=note, velocity=max(0, min(velocity, 127)), time=delta))
        mid.save(filename)
        print(f"MIDI salvato in {filename}")


if __name__ == '__main__':
    drum = DrumMIDI()
    drum.add_fixednote_pattern([127, 127, 0, 0, 0, 0, 0, 0, 0, 127, 127, 0, 0, 0, 0, 127] * 1, subdivision=1 / 8)
    drum.add_fixednote_pattern([127, 0, 0, 127, 0, 0, 127, 0, 0, 127, 127, 0, 0, 127, 0, 80] * 1, subdivision=1 / 8)
    drum.add_fixednote_pattern([127, 0, 0, 127, 0, 0, 127, 0, 0, 127, 127, 0, 0, 127, 0, 80] * 1, subdivision=1 / 8)


    drum.generate_midi('drum_pattern.mid')
