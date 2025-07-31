import numpy as np


class SCM:
    def __init__(self):
        self.correlation_dict = dict()
        self.hashable = False

    def fit(self, data, hashable=False):
        self.hashable = hashable
        if hashable:
            for entry in data:
                for seq, seqp1 in zip(entry[:-1], entry[1:]):
                    if seq not in self.correlation_dict:
                        self.correlation_dict[seq] = dict()
                    if seqp1 in self.correlation_dict[seq]:
                        self.correlation_dict[seq][seqp1] += 1
                    else:
                        self.correlation_dict[seq][seqp1] = 1
        else:
            for entry in data:
                for seq, seqp1 in zip(entry[:-1], entry[1:]):
                    seq = tuple(seq)
                    seqp1 = tuple(seqp1)
                    if seq not in self.correlation_dict:
                        self.correlation_dict[seq] = dict()
                    if seqp1 in self.correlation_dict[seq]:
                        self.correlation_dict[seq][seqp1] += 1
                    else:
                        self.correlation_dict[seq][seqp1] = 1
        # print(self.correlation_dict)

    def predict(self, seq, temperature=1, astype=None):
        if self.hashable:
            diz = self.correlation_dict[seq]
            single_btl = [(np.exp((1 / temperature) * v), i) for i, v in diz.items()]
            Z = sum([a[0] for a in single_btl])
            probabilities = [(s[0] / Z, s[1]) for s in single_btl]
            #print(probabilities)
            if astype is None:
                return np.random.choice(a=[p[1] for p in probabilities], p=[p[0] for p in probabilities])
            else:
                return [astype(a) for a in
                        np.random.choice(a=[p[1] for p in probabilities], p=[p[0] for p in probabilities]).split(', ')]

        else:
            seq = tuple(seq)
            diz = self.correlation_dict[seq]
            single_btl = [(np.exp((1/temperature)*v), i) for i, v in diz.items()]
            Z = sum([a[0] for a in single_btl])
            probabilities = [(s[0] / Z, str(s[1])[1:-1]) for s in single_btl]
            return [int(a) for a in np.random.choice(a=[p[1] for p in probabilities], p=[p[0] for p in probabilities]).split(', ')]

    def sequential_predict(self, seq, temperature=1, size=4):
        generated = [seq]
        for i in range(size):
            generated.append(self.predict(generated[-1], temperature=temperature))

        return generated


class DeepSCM:
    def __init__(self, max_distance=3):
        self.correlation_dict = dict()
        self.hashable = False
        self.max_distance = max_distance  # Profondità di correlazione

    def fit(self, data, hashable=False):
        self.hashable = hashable
        if hashable:
            for entry in data:
                for i in range(len(entry)):
                    for j in range(1, self.max_distance + 1):
                        if i + j < len(entry):
                            seq, seqp = entry[i], entry[i + j]
                            if seq not in self.correlation_dict:
                                self.correlation_dict[seq] = dict()
                            if seqp in self.correlation_dict[seq]:
                                self.correlation_dict[seq][seqp] += 1 / j  # Peso inverso alla distanza
                            else:
                                self.correlation_dict[seq][seqp] = 1 / j
        else:
            for entry in data:
                for i in range(len(entry)):
                    for j in range(1, self.max_distance + 1):
                        if i + j < len(entry):
                            seq, seqp = tuple(entry[i]), tuple(entry[i + j])
                            if seq not in self.correlation_dict:
                                self.correlation_dict[seq] = dict()
                            if seqp in self.correlation_dict[seq]:
                                self.correlation_dict[seq][seqp] += 1 / j  # Peso inverso alla distanza
                            else:
                                self.correlation_dict[seq][seqp] = 1 / j

    def predict(self, seq, temperature=1, astype=None):
        if self.hashable:
            seq_dict = self.correlation_dict.get(seq, {})
        else:
            seq_dict = self.correlation_dict.get(tuple(seq), {})

        if not seq_dict:
            return None  # Nessuna predizione possibile

        # Softmax con temperatura
        exp_values = {k: np.exp((1 / temperature) * v) for k, v in seq_dict.items()}
        Z = sum(exp_values.values())
        probabilities = [(v / Z, k) for k, v in exp_values.items()]

        if astype is None:
            return np.random.choice(a=[p[1] for p in probabilities], p=[p[0] for p in probabilities])
        else:
            return [astype(a) for a in
                    np.random.choice(a=[p[1] for p in probabilities], p=[p[0] for p in probabilities]).split(', ')]

    def sequential_predict(self, seq, temperature=1, size=4):
        generated = [seq]
        for _ in range(size):
            next_seq = self.predict(generated[-1], temperature=temperature)
            if next_seq is None:
                break
            generated.append(next_seq)
        return generated




