from intomido.drums import PercussionPattern
from intomido.composers import Pianoroll

roll = Pianoroll(16, 16)

hh = PercussionPattern(16)
hh.genmod((8, 16))
hh.add_roll(16*2, 4, scaleup=True)
hh.add_roll(16*6, 6, mod=3)
roll.add_rythmic_pattern_list(hh.velocities)
roll.plot()
roll.save_to('hh1.mid')


