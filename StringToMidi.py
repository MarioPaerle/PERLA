from intomido.composers import Chords as c

def from_string_to_progression(stringa):
    """Parse Strings like: F G C C7, or Am F Dm E"""
    splitted = stringa.split()
    progression = []
    for chord in splitted:
        if chord in CHORD_TO_INTOMIDO:
            progression.append(chord)


CHORD_TO_INTOMIDO = {
    "A": c.VImaj,
    "Am": c.VImin,
    "B": c.VIImin, # B is the 7th degree, typically diminished in C major, but if we're just doing maj/min, it's often represented as minor in simple contexts.
    "Bm": c.VIImin, # In C major, B is naturally the 7th degree, leading to Bdim (B-D-F). If 'c.VIImin' specifically represents a minor chord built on the 7th, this would be the closest.
    "C": c.Imaj,
    "Cm": c.Imin, # Cm is not diatonic to C major, but would be the minor I chord
    "D": c.IImin,
    "Dm": c.IImin, # Dm is diatonic to C major
    "E": c.IIImin,
    "Em": c.IIImin, # Em is diatonic to C major
    "F": c.IVmaj,
    "Fm": c.IVmin, # Fm is not diatonic to C major, but would be the minor IV chord
    "G": c.Vmaj,
    "Gm": c.Vmin, # Gm is not diatonic to C major, but would be the minor V chord
}