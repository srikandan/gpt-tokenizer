import regex as re

from utility import Utility

class Tokenizer:
    def __init__(self, merges_path, current_vocab_size, regex_split_pattern=None):
        self.utility = Utility()
        self.merges_path = merges_path
        self.current_vocab_size = current_vocab_size
        self.regex_split_pattern = regex_split_pattern
        self.compiled_pattern = re.compile(self.regex_split_pattern) if self.regex_split_pattern else None

        self.build_merges()
        self.build_vocabulary()

    def build_merges(self):
        """
        Loads merges
        """
        self.merges = {}
        idx = self.current_vocab_size
        with open(self.merges_path, "r") as file:
            for line in file:
                idx1, idx2 = map(int, line.split())
                self.merges[(idx1, idx2)] = idx
                idx += 1

    def build_vocabulary(self):
        """
        Builds vocabulary from merges
        """
        self.vocabulary = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            self.vocabulary[idx] = self.vocabulary[p0] + self.vocabulary[p1]

    def encode(self, text):
        """
        Encodes the text into token ids

        Args:
            text (str): text

        Returns:
            list: encoded - token ids
        """
        if self.regex_split_pattern:
            text_chunks = re.findall(self.compiled_pattern, text)
        else:
            text_chunks = [text]

        tokens = []
        for chunk in text_chunks:
            chunk_bytes = list(chunk.encode("utf-8"))
            while len(chunk_bytes) >= 2:
                pairs_count = self.utility.get_pair_count(chunk_bytes)
                pair = min(pairs_count, key=lambda x: self.merges.get(x, float("inf")))
                if pair not in self.merges:
                    break
                chunk_bytes = self.utility.merge_pair(chunk_bytes, pair, self.merges[pair])
            tokens.extend(chunk_bytes)
        return tokens

    def decode(self, tokens):
        """
        Decodes token ids into text

        Args:
            tokens (list): list of token ids

        Returns:
            text (str): decoded text
        """
        if self.regex_split_pattern:
            part_bytes = []
            for idx in tokens:
                if idx in self.vocabulary:
                    part_bytes.append(self.vocabulary[idx])
            text_bytes = b"".join(part_bytes)
            return text_bytes.decode("utf-8", errors="replace")
        else:
            tokens = b''.join([self.vocabulary[tk] for tk in tokens])
            text = tokens.decode("utf-8", errors="replace")
            return text
