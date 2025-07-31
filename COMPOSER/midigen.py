from mido import Message, MidiFile, MidiTrack, MetaMessage

NOTE_TO_MIDI = {
    'C': 60,
    'C#': 61,
    'D': 62,
    'D#': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'G': 67,
    'G#': 68,
    'A': 69,
    'A#': 70,
    'B': 71,
    '0': 0
}

CHORD_FORMULAS = {
    '': [0, 4, 7],
    'm': [0, 3, 7],
    '6': [0, 4, 7, 9],
    'm6': [0, 3, 7, 9],
    '4': [0, 5, 7],
    'dim': [0, 3, 6],
    'dim7': [0, 4, 6, 10],
    'dim7+': [0, 4, 6, 11],
    'dim6': [0, 4, 6, 9],
    'mdim7': [0, 3, 6, 10],
    'mdim7+': [0, 3, 6, 11],
    'mdim6': [0, 3, 6, 9],
    '7': [0, 4, 7, 10],
    'm7': [0, 3, 7, 10],
    '7+': [0, 4, 7, 11],
    'm7+': [0, 3, 7, 11],
    'sus1': [0, 5, 7],
    'sus2': [0, 2, 7],
    'sus': [0, 2, 7],
}


def parse_chord(chord_name):
    """
    Esempi di chord_name: "A", "A6", "A4", "Adim", "A7", "A7+", "A#7", ecc.
    Restituisce la lista di note MIDI corrispondenti all'accordo.
    """
    # 1) Estrarre la radice (eventualmente con #)
    if len(chord_name) > 1 and chord_name[1] == '#':
        root = chord_name[:2]  # es. "A#"
        suffix = chord_name[2:]  # es. "7"
    else:
        root = chord_name[0]  # es. "A"
        suffix = chord_name[1:]  # es. "7", "m", "dim", ecc.

    # Verifica che la radice sia presente nel dizionario NOTE_TO_MIDI
    if root not in NOTE_TO_MIDI:
        raise ValueError(f"La radice '{root}' non è nel dizionario NOTE_TO_MIDI.")

    # 2) Se il suffix non è presente (accordo maggiore base), forziamo suffix=''
    if suffix == '':
        suffix = ''

    # Verifica che il suffisso esista nelle formule
    if suffix not in CHORD_FORMULAS:
        raise ValueError(f"Il suffisso '{suffix}' non è supportato.")

    root_midi = NOTE_TO_MIDI[root]
    intervals = CHORD_FORMULAS[suffix]

    # 3) Calcola le note finali
    return [root_midi + interval for interval in intervals]


def chord_to_notes(chord_letter):
    """
    Se maiuscolo -> accordo maggiore
    Se minuscolo -> accordo minore
    """
    """root = NOTE_TO_MIDI[chord_letter.upper()]
    if chord_letter.isupper():
        # accordo maggiore: R, R+4, R+7
        return [root, root + 4, root + 7]
    else:
        # accordo minore: R, R+3, R+7
        return [root, root + 3, root + 7]"""

    return parse_chord(chord_letter)


def get_best_voicing(prev_voicing, chord_notes):
    """
    Esempio molto semplificato:
    - prova le inversioni
    - per ciascuna nota dell’inversione cerca la trasposizione ±12 semitoni più vicina
    - Ritorna l’inversione con distanza complessiva minore
    """
    # Tutte le inversioni di una triade (root, first, second)
    # Esempio base: [R, R+4, R+7]
    # 1° inversione: [R+4, R+7, R+12]
    # 2° inversione: [R+7, R+12, R+16]
    # NB: L’aggiunta di 12 semitoni fa salire un’ottava
    # Qui potresti voler aggiungere logica più sofisticata.
    inversioni = [
        chord_notes,
        [chord_notes[1], chord_notes[2], chord_notes[0] + 12],
        [chord_notes[2], chord_notes[0] + 12, chord_notes[1] + 12]
    ]
    best = None
    best_distance = float('inf')

    for inv in inversioni:
        # Creiamo un voicing “adattato” al precedente
        # cercando di spostare ogni nota di ±12 se necessario
        voicing = []
        for i, note in enumerate(inv):
            # Cerchiamo la nota (tra note-12, note, note+12) più vicina alla voce corrispondente
            candidati = [note + 12 * k for k in (-1, 0, 1)]
            try:
                best_note = min(candidati, key=lambda x: abs(x - prev_voicing[i]))
            except IndexError:
                pass

            voicing.append(best_note)
        try:
            distanza = sum(abs(voicing[i] - prev_voicing[i]) for i in range(len(voicing)))
        except:
            distanza = sum(abs(voicing[i] - prev_voicing[i]) for i in range(len(voicing)-1))

        if distanza < best_distance:
            best_distance = distanza
            best = voicing

    return best


def generate_midi(chord_string, output_file="output.mid", tempo=500000):
    """
    chord_string es: "AAAA|CCCC|FFGG|AAAA"
    Ogni lettera è un quarto (4/4).
    """
    # Separiamo in misure
    measures = chord_string.split("|")

    # Creiamo la lista di tutti i quarti (lettere) in sequenza
    # Esempio: "AAAA|CCCC" -> ["A","A","A","A","C","C","C","C"]
    chord_sequence = []
    for m in measures:
        chord_sequence.extend(m.split())

    # Preparazione MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    quarter_note_ticks = 480  # risoluzione standard (1 quarter note = 480 tick)

    if len(chord_sequence) == 0:
        print("Nessun accordo trovato!")
        return

    prev_voicing = chord_to_notes(chord_sequence[0])
    prev_voicing.sort()

    # Primo accordo: lo suoniamo subito
    # Accensione di tutte le note insieme
    track.append(Message('note_on', note=prev_voicing[0], velocity=64, time=0))
    for note in prev_voicing[1:]:
        track.append(Message('note_on', note=note, velocity=64, time=0))

    # Spegnimento di tutte le note insieme dopo 1/4
    track.append(Message('note_off', note=prev_voicing[0], velocity=64, time=quarter_note_ticks))
    for note in prev_voicing[1:]:
        track.append(Message('note_off', note=note, velocity=64, time=0))

    # Ora generiamo i restanti
    for chord_letter in chord_sequence[1:]:
        chord_notes = chord_to_notes(chord_letter)
        current_voicing = get_best_voicing(prev_voicing, chord_notes)
        actual_current_voicing = current_voicing.copy()
        actual_current_voicing[1] += 12
        # Accensione di tutte le note insieme
        track.append(Message('note_on', note=actual_current_voicing[0], velocity=64, time=0))
        for note in actual_current_voicing[1:]:
            track.append(Message('note_on', note=note, velocity=64, time=0))

        # Spegnimento di tutte le note insieme dopo 1/4
        track.append(Message('note_off', note=actual_current_voicing[0], velocity=64, time=quarter_note_ticks))
        for note in actual_current_voicing[1:]:
            track.append(Message('note_off', note=note, velocity=64, time=0))

        prev_voicing = current_voicing

    mid.save(output_file)
    print(f"File MIDI salvato come {output_file}")

def generate_midi_numeric(chords, output_file="output.mid", tempo=500000):
    """
    chord_string es: "AAAA|CCCC|FFGG|AAAA"
    Ogni lettera è un quarto (4/4).
    """
    """# Separiamo in misure
    measures = chord_string.split("|")

    # Creiamo la lista di tutti i quarti (lettere) in sequenza
    # Esempio: "AAAA|CCCC" -> ["A","A","A","A","C","C","C","C"]
    chord_sequence = []
    for m in measures:
        chord_sequence.extend(m.split())"""

    # Preparazione MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    quarter_note_ticks = 480  # risoluzione standard (1 quarter note = 480 tick)
    """
    if len(chord_sequence) == 0:
        print("Nessun accordo trovato!")
        return"""
    chord_sequence = chords
    prev_voicing = chords[0]
    prev_voicing.sort()

    # Primo accordo: lo suoniamo subito
    # Accensione di tutte le note insieme
    track.append(Message('note_on', note=prev_voicing[0], velocity=64, time=0))
    for note in prev_voicing[1:]:
        track.append(Message('note_on', note=note, velocity=64, time=0))

    # Spegnimento di tutte le note insieme dopo 1/4
    track.append(Message('note_off', note=prev_voicing[0], velocity=64, time=quarter_note_ticks))
    for note in prev_voicing[1:]:
        track.append(Message('note_off', note=note, velocity=64, time=0))

    # Ora generiamo i restanti
    for chord_letter in chord_sequence[1:]:
        chord_notes = chord_letter
        current_voicing = get_best_voicing(prev_voicing, chord_notes)

        # Accensione di tutte le note insieme
        track.append(Message('note_on', note=current_voicing[0], velocity=64, time=0))
        for note in current_voicing[1:]:
            track.append(Message('note_on', note=note, velocity=64, time=0))

        # Spegnimento di tutte le note insieme dopo 1/4
        track.append(Message('note_off', note=current_voicing[0], velocity=64, time=quarter_note_ticks))
        for note in current_voicing[1:]:
            track.append(Message('note_off', note=note, velocity=64, time=0))

        prev_voicing = current_voicing

    mid.save(output_file)
    print(f"File MIDI salvato come {output_file}")


def get_simple_voicing(chord_notes, octave=4):
    """
    Restituisce sempre l'accordo in root position
    spostato nell'ottava desiderata
    """
    # chord_notes sono [root, root+3/4, root+7] in notazione MIDI
    # li portiamo tutti all’ottava 4 (intorno a C4 = 60)
    # Trovando la differenza tra root e 60 e spostando in base a quell’ottava.
    base_root = chord_notes[0]
    # Supponiamo che C4=60, se la root è C -> 60, D -> 62, ...
    # Se vuoi esattamente l’ottava 4, puoi calcolare:
    shift = (octave * 12 + (base_root % 12)) - base_root
    # e applicarlo a tutte le note
    voicing = [n + shift for n in chord_notes]
    return voicing


if __name__ == '__main__':
    chord_string = "Dm6 A A A | C C C C | F F G G | A A A A"
    generate_midi(chord_string)
    # current_voicing = get_simple_voicing(chord_notes, octave=4)
