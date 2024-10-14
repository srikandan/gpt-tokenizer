import regex as re

from utility import Utility

class TrainBPE:
    def __init__(self, current_vocab_size=0, new_vocab_size=0, regex_split_pattern=None,
                 dataset_path='', merges_path='', vocabulary_path=''):
        self.utility = Utility()
        self.current_vocab_size = current_vocab_size
        self.new_vocab_size = new_vocab_size
        self.dataset_path = dataset_path
        self.merges_path = merges_path
        self.vocabulary_path = vocabulary_path
        self.regex_split_pattern = regex_split_pattern

    def train_tokanizer(self, tokens, num_merges):
        """
        Iteratively merges the top pairs with new token id

        Args:
            tokens (list): UTF-8 encoded ids
            num_merges (int): total number of merges
            new_token_id (int): New token id, which will replace the pair

        Returns:
            dict: merges with replaced token id
        """
        new_token_id = self.current_vocab_size

        self.vocabulary = {idx: bytes([idx]) for idx in range(self.current_vocab_size)}

        self.merges = {}
        for mc in range(num_merges):
            pair_count = self.utility.get_pair_count(tokens)
            top_pair = max(pair_count, key=pair_count.get)
            tokens = self.utility.merge_pair(tokens, top_pair, new_token_id)
            self.merges[top_pair] = new_token_id
            self.vocabulary[new_token_id] = self.vocabulary[top_pair[0]] + self.vocabulary[top_pair[1]]
            new_token_id += 1
            print(f'Merges --> {mc+1} : Pair {top_pair} replaced with {new_token_id}')
        print(f'Trained token length: {len(tokens)}')
    
    def train_regex_tokanizer(self, chunk_tokens, num_merges):
        """
        Iteratively merges the top pairs with new token id

        Args:
            tokens (list): UTF-8 encoded ids
            num_merges (int): total number of merges
            new_token_id (int): New token id, which will replace the pair

        Returns:
            dict: merges with replaced token id
        """
        self.vocabulary = {idx: bytes([idx]) for idx in range(self.current_vocab_size)}

        new_token_id = self.current_vocab_size
        self.merges = {}
        for mc in range(num_merges):
            pair_count = {}
            for tk_id in chunk_tokens:
                pair_count = self.utility.get_pair_count(tk_id, pair_count)
            top_pair = max(pair_count, key=pair_count.get)
            chunk_tokens = [self.utility.merge_pair(chunk, top_pair, new_token_id) for chunk in chunk_tokens]
            self.merges[top_pair] = new_token_id
            self.vocabulary[new_token_id] = self.vocabulary[top_pair[0]] + self.vocabulary[top_pair[1]]
            new_token_id += 1
            print(f'Merges --> {mc+1} : Pair {top_pair} replaced with {new_token_id}')
        print(f'Trained token length: {len(chunk_tokens)}')
    
    def save_merges(self):
        """
        Saves Merger data as JSON file

        Args:
            merges (dict): merges data
        """
        with open(self.merges_path, "w") as file:
            for (p0, p1), _ in self.merges.items():
                file.write(f'{p0} {p1}\n')
        print(f'Merges file is saved in {self.merges_path}')

    def save_vocabulary(self):
        """
        Builds vocabulary, along with newly added vocabulary and saves it as .BPE file

        Args:
            merges (dict): merges data
        """
        inverted_merges = {idx: pair for pair, idx in self.merges.items()}

        with open(self.vocabulary_path, "w", encoding="utf-8") as file:
            for idx, token in self.vocabulary.items():
                rd_token = self.utility.render_token(token)
                if idx in inverted_merges:
                    # if this token has children, render it nicely as a merge
                    idx0, idx1 = inverted_merges[idx]
                    s0 = self.utility.render_token(self.vocabulary[idx0])
                    s1 = self.utility.render_token(self.vocabulary[idx1])
                    file.write(f"[{s0}][{s1}] -> [{rd_token}] {idx}\n")
                else:
                    # otherwise this is leaf token, just print it
                    # (this should just be the first 256 tokens, the bytes)
                    file.write(f"[{rd_token}] {idx}\n")
        print(f'Vocabulary file is saved in {self.vocabulary_path}')

    def train(self):
        """
        Main function that train tokenizer

        Args:
            text (str): dataset for training tokenizer
            current_vocab_size (int): current vocabulary size
            new_vocab_size (int): new vocabulary size

        Returns:
            dict: pairs and repalced new token id
        """
        text = self.utility.read_text_file(self.dataset_path)

        num_merges = self.new_vocab_size - self.current_vocab_size

        if self.regex_split_pattern:
            print('Regex tokenizer is loaded')
            pattern = re.compile(self.regex_split_pattern)
            splitted_text = pattern.findall(text)
            tokens = [list(chunk.encode('utf-8')) for chunk in splitted_text]
            self.train_regex_tokanizer(tokens, num_merges)
        else:
            print('Basic tokenizer is loaded')
            tokens = list(text.encode('utf-8'))
            self.train_tokanizer(tokens, num_merges)

        print('Encoding in Decimal format:', tokens)
        print('Character Length: ', len(text))
        print('Token Length: ', len(tokens))
        
        self.save_merges()
        self.save_vocabulary()
