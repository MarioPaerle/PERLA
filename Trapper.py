from intomido.drums import PercussionPattern
from intomido.composers import Pianoroll
import random as rd

resolution_mlt = mlt = 2
# HHs
if False:
    hhroll = Pianoroll(16, 16 * mlt)

    hh = PercussionPattern(16*mlt)
    hh.genmod((8*mlt, 16*mlt))
    for bar in range(1, 9):
        if rd.random() > 0.45:
            hh.add_roll(16*bar*2*mlt, rd.choice([1, 2])*rd.choice([4, 4, 4, 4, 5, 6, 6, 3, 3]), scaleup=rd.choice([True, False, True]), mod=2*mlt)

    hh.humanize(1)

    hhroll.add_rythmic_pattern_list(hh.velocities)
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
    snareroll.plot()
    snareroll.save_to('snare1.mid')