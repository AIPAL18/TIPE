# I used https://www.codeconvert.ai/ because idk Ruby at all
#   and I approximately don't have the time to learn Ruby's OOP...
#   Though, it needed some adjustments cause it was wrong
"""
NOTE: 
    - **Namespace/Module Structure**: Ruby's `module BentleyMcIlroy` was translated into a Python class `BentleyMcIlroy` containing nested classes to maintain the same organizational structure.
    - **Naming Conventions**: 
        - Ruby's snake_case methods and variables were preserved as snake_case in Python (e.g., `block_size`, `find_for_compress`).
        - Private methods in Ruby (under the `private` keyword) were prefixed with a single underscore in Python (e.g., `_find`, `_compress_encode`) to indicate internal use.
    - **String Slicing**: 
        - Ruby's `target[0, block_size]` (start, length) was converted to Python's `target[0:block_size]` (start:end).
        - Ruby's `source[block.position + block_size..-1]` was converted to `source[block.position + block_size:]`.
        - Ruby's `text[position, 1]` was converted to `text[position]`.
    - **Regex Scan**: Ruby's `@text.scan(/.(?:.?){#{@block_size-1}}/ )` is used to split the string into non-overlapping chunks of `block_size`. In Python, `re.findall` with the same pattern and `re.DOTALL` (to handle newlines) achieves the same result.
    - **Inject/Reduce**: Ruby's `inject` (or `reduce`) was converted to standard `for` loops in Python for clarity and idiomatic performance, as Python's `functools.reduce` is less commonly used for string concatenation.
    - **Type Checking**: Ruby's `is_a?(Array)` was converted to Python's `isinstance(i, list)`.
    - **RollingHash**: As per instructions, the `rolling_hash` module is imported and used. Note that in Ruby, `hasher.next_hash(text[position-1 + block_size, 1])` passes a string of length 1. In Python, `text[position - 1 + block_size]` passes the character at that index.
    - **Logic Adjustment in `produce_match`**: In the original Ruby code, `produce_match` used `source[0..end_index]`. However, `source` in that context was the remainder of the string *after* the block. I adjusted the Python implementation to pass `source_match` and use `source_match[0:end_index + 1]` to correctly append the matching suffix.
    - **Boolean Logic**: Ruby's `nil` and empty strings/lists are falsy in many contexts. Python's `None` and empty collections behave similarly, but explicit checks (e.g., `is not None`) were used where appropriate to ensure exact logic preservation.
"""
import rolling_hash
import re


class BentleyMcIlroy:
    class Block:
        def __init__(self, text, position):
            self._text = text
            self._position = position

        @property
        def text(self):
            return self._text

        @property
        def position(self):
            return self._position

        def hash(self):
            return rolling_hash.RollingHash().hash(self.text)

    class BlockSequencedText:
        def __init__(self, text, block_size):
            self._text = text
            self._block_size = block_size
            self._blocks = []

            # Ruby's .scan(/.(?:.?){#{@block_size-1}}/) captures chunks of block_size.
            # In Python, we can achieve this with a regex or a simple loop.
            # The regex equivalent for Ruby's scan with this pattern:
            pattern = r'.(?:.?){' + str(self._block_size - 1) + r'}'
            matches = re.findall(pattern, self._text, re.DOTALL)
            
            for index, text_block in enumerate(matches):
                self._blocks.append(BentleyMcIlroy.Block(text_block, index * self._block_size))

        @property
        def blocks(self):
            return self._blocks

        @property
        def text(self):
            return self._text

    class BlockFingerprintTable:
        def __init__(self, block_sequenced_text):
            self._blocked_text = block_sequenced_text
            self._hash = {}

            for block in self._blocked_text.blocks:
                block_hash = block.hash()
                if block_hash not in self._hash:
                    self._hash[block_hash] = []
                self._hash[block_hash].append(block)

        def find_for_compress(self, fingerprint, block_size, target, position):
            source = self._blocked_text.text
            return self._find(fingerprint, block_size, source, target, position)

        def find_for_diff(self, fingerprint, block_size, target):
            source = self._blocked_text.text
            return self._find(fingerprint, block_size, source, target)

        def _find(self, fingerprint, block_size, source, target, position=None):
            blocks = self._hash.get(fingerprint)
            if not blocks:
                return None
            
            for block in blocks:
                if block.text != target[0:block_size]:
                    continue
                
                # in compression, since we don't have true source and target strings as
                # separate things, we have to ensure that we don't use a fingerprinted
                # block which appears _after_ the current position, otherwise
                #
                # a<x, 0> with x > 0
                #
                # might happen, or similar. since blocks are ordered left to right in the
                # string, we can just return nil, because we know there's not going to be
                # a valid block for compression.
                if position is not None and block.position >= position:
                    return None
                
                # we know that block matches, so cut it from the beginning,
                # so we can then see how much of the rest also matches
                source_match = source[block.position + block_size:]
                target_match = target[block_size:]
                
                if not source_match or not target_match:
                    return block

                end_index = self._find_end_index(source_match, target_match)
                match = self._produce_match(end_index, block, source_match)
                return match

            return None
        
        def _find_end_index(self, source, target):
            end_index = 0
            any_match = False
            while end_index < len(source) and end_index < len(target) and source[end_index] == target[end_index]:
                any_match = True
                end_index += 1
            
            end_index -= 1
            
            return end_index if any_match else None

        def _produce_match(self, end_index, block, source_match):
            text = block.text
            if end_index is not None:
                text += source_match[0:end_index + 1]
            return BentleyMcIlroy.Block(text, block.position)

    class Codec:
        @staticmethod
        def decompress(sequence):
            result = ""
            for i in sequence:
                if isinstance(i, list):
                    index, length = i
                    for k in range(length):
                        result += result[index + k]
                else:
                    result += i
            return result
        
        @staticmethod
        def decode(source, delta):
            result = ""
            for i in delta:
                if isinstance(i, list):
                    index, length = i
                    result += source[index:index + length]
                else:
                    result += i
            return result

        @staticmethod
        def compress(text, block_size):
            return BentleyMcIlroy.Codec._compress_encode(text, None, block_size)

        @staticmethod
        def encode(source, target, block_size):
            return BentleyMcIlroy.Codec._compress_encode(source, target, block_size)

        @staticmethod
        def _compress_encode(source, target, block_size):
            if source == target:
                return []
            
            block_sequenced_text = BentleyMcIlroy.BlockSequencedText(source, block_size)
            table = BentleyMcIlroy.BlockFingerprintTable(block_sequenced_text)
            output = []
            buffer = ""
            current_hash = None
            hasher = rolling_hash.RollingHash()
            
            mode = "diff" if target is not None else "compress"
            
            if mode == "compress":
                text = source
            else:
                text = target

            position = 0
            while position < len(text):

                if len(text) - position < block_size:
                    break
                
                if current_hash is None:
                    current_hash = hasher.hash(text[position:position + block_size])
                else:
                    current_hash = hasher.next_hash(text[position - 1 + block_size])

                if target is not None:
                    match = table.find_for_diff(current_hash, block_size, target[position:])
                else:
                    match = table.find_for_compress(current_hash, block_size, text[position:], position)

                if match:
                    if buffer:
                        output.append(buffer)
                        buffer = ""

                    output.append([match.position, len(match.text)])
                    position += len(match.text)
                    current_hash = None
                    hasher = rolling_hash.RollingHash()
                else:
                    buffer += text[position]
                    position += 1

            remainder = buffer + text[position:]
            if remainder:
                output.append(remainder)
            return output

