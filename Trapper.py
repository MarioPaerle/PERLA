from intomido.drums import PercussionPattern
from intomido.composers import Pianoroll, Chords, Group
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from PATTERNS import TRAP_MASKING_16


"""A very simple Trapper: This program generates midis file for a very basic trap beat:
Drums (hh, kick, snare), Melody (prog, pad), 808 [WIP]"""

PLOT = False

resolution_mlt = mlt = 2
progressions = [
    (Chords.VImin + Chords.IImin + Chords.Napulitan + Chords.IIImaj).to_chord_progression().enlarge().multiply(resolution_mlt*32*mlt).to_chord(),
    (Chords.IImin + Chords.VImin + Chords.IIImaj + Chords.VImin).to_chord_progression().enlarge().multiply(resolution_mlt*32*mlt).to_chord(),
    (Chords.VImin + Chords.VImin + Chords.Napulitan + Chords.IIImaj).to_chord_progression().enlarge().multiply(resolution_mlt*32*mlt).to_chord(),

    (Chords.VImin + Chords.IIImin + Chords.IVmaj + Chords.IIImaj).to_chord_progression().enlarge().multiply(resolution_mlt*32*mlt).to_chord(),
    (Chords.VImin + Chords.IIImin + Chords.IVmaj + Chords.Vmaj).to_chord_progression().enlarge().multiply(resolution_mlt*32*mlt).to_chord(),
    (Chords.Imaj + Chords.IIImin + Chords.IVmaj + Chords.IVmin).to_chord_progression().enlarge().multiply(resolution_mlt*32*mlt).to_chord(),
    (Chords.Imaj + Chords.IIImin + Chords.IVmaj + Chords.Vmaj).to_chord_progression().enlarge().multiply(resolution_mlt*32*mlt).to_chord(),
]
# HHs
if True:
    hhroll = Pianoroll(16, 16 * mlt)

    hh = PercussionPattern(16*mlt)
    hh.genmod((8*mlt, 16*mlt))
    for bar in range(1, 9):
        if rd.random() > 0.45:
            hh.add_roll(16*bar*2*mlt, rd.choice([1, 2])*rd.choice([4, 4, 4, 4, 5, 6, 6, 3, 3]), scaleup=rd.choice([True, False, True]), mod=2*mlt)

    hh.humanize(1)

    hhroll.add_rythmic_pattern_list(hh.velocities)
    if PLOT:
        hhroll.plot()
    hhroll.save_to('hh1.mid')


# Kick
if True:
    kickroll = Pianoroll(16, 16 * mlt)
    kick = PercussionPattern(16*mlt)
    kick.genmod((128*mlt, 96*mlt-16*mlt), div=2)
    if rd.random() > 0.33:
        kick.velocities[rd.choice([24*mlt, 16*mlt])] = 100
    if rd.random() > 0.45:
        kick.velocities[128*mlt + rd.choice([24*mlt, 16*mlt])] = 100
    if rd.random() > 0.33:
        kick.velocities[192*mlt + rd.choice([48*mlt, 56*mlt])] = 100
    kickroll.add_rythmic_pattern_list(kick.velocities)
    if PLOT:
        kickroll.plot()
    kickroll.save_to('kick1.mid')


# Snare
if True:
    snareroll = Pianoroll(16, 16 * mlt)
    snare = PercussionPattern(16*mlt)

    for i in range(4):
        snare.velocities[64 + i*128] = 100
        if rd.random() > 0.33:
            snare.velocities[112 + i*128] = 100
        if rd.random() > 0.33:
            if i < 3:
                snare.velocities[128+16 + i*128] = 100

    snareroll.add_rythmic_pattern_list(snare.velocities)
    if PLOT:
        snareroll.plot()
    snareroll.save_to('snare1.mid')


# Progression
if True:
    prog = rd.choice(progressions)
    tonics = [c.tonic for c in prog.get_separed_chords()]
    pad = rd.choice(progressions)
    masking = rd.choice(TRAP_MASKING_16)
    masking = [masking[i // 8] for i in range(128)]*4
    masking = np.array(masking)
    progroll = Pianoroll(16, 16 * mlt)
    progroll._add_group(prog)
    progroll.grid[:, masking == 0] = 0
    if PLOT:
        progroll.plot()
    progroll.save_to('prog.mid')
    padroll = Pianoroll(16, 16 * mlt)
    pad.transpose(-12)
    padroll._add_group(pad)
    if PLOT:
        padroll.plot()
    padroll.save_to('pad.mid')


if True:
    bassroll = Pianoroll(16, 16 * mlt)
    extended_tonics = [tonics[i//32] for i in range(128)]
    bass = Group(notes=extended_tonics)
    bassroll._add_group(bass)
    kick_mask = np.array(kick.velocities)
    kick_mask[kick_mask > 0] = 1
    kick_mask = kick_mask.astype(np.uint8)
    bassroll.grid *= kick_mask
    if PLOT:
        bassroll.plot()
    bassroll.save_to('808.mid')

