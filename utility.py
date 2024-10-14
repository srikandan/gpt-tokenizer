import unicodedata

class Utility:

    def read_text_file(self, file_path):
        """
        Reads text file

        Args:
            file_path (str): file path

        Returns:
            str: text file data
        """
        return open(file_path, "r", encoding="utf-8").read()
    
    def get_pair_count(self, tokens, counts=None):
        """
        Return pairs with repetition count

        Args:
            tokens (list): UTF-8 encoded ids

        Returns:
            list: pairs with repetition count
        """
        pair_count = counts if counts else {}
        for pair in zip(tokens, tokens[1:]):
            pair_count[pair] = pair_count.get(pair, 0) + 1
        return pair_count
    
    def merge_pair(self, tokens, pair, new_token_id):
        """
        Merges pair with new token id

        Args:
            tokens (list): UTF-8 encoded ids
            pair (set): pair to be replaced
            new_token_id (int): New token id, which will replace pair

        Returns:
            list: updated token ids
        """
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i+1] == pair[1]:
                new_tokens.append(new_token_id)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        return new_tokens
    
    def replace_control_characters(self, s: str) -> str:
        # we don't want to print control characters
        # which distort the output (e.g. \n or much worse)
        # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python/19016117#19016117
        # http://www.unicode.org/reports/tr44/#GC_Values_Table
        chars = []
        for ch in s:
            if unicodedata.category(ch)[0] != "C":
                chars.append(ch) # this character is ok
            else:
                chars.append(f"\\u{ord(ch):04x}") # escape
        return "".join(chars)
    
    def render_token(self, t: bytes) -> str:
        # pretty print a token, escaping control characters
        s = t.decode('utf-8', errors='replace')
        s = self.replace_control_characters(s)
        return s