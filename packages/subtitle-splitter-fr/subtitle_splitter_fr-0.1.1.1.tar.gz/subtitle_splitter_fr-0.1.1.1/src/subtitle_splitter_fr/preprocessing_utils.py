import re
from typing import List, Tuple, Optional

# Define token types
T_OPEN_PUNC = "OPEN_PUNC"
T_WORD = "WORD"
T_CLOSE_PUNC_UNIT = "CLOSE_PUNC_UNIT"
T_SPACE = "SPACE"
T_OTHER = "OTHER"  # Catch-all for unexpected characters


def _get_next_non_space(tokens: List[Tuple[str, Optional[str]]], start_index: int) -> Tuple[Optional[int], str]:
    """Helper to find the next non-space token and capture intermediate spaces."""
    space = ""
    idx = start_index
    while idx < len(tokens):
        if tokens[idx][1] == T_SPACE:
            space += tokens[idx][0]
            idx += 1
        else:
            return idx, space  # Found non-space token
    return None, space  # No non-space token found


def split_text_into_elements(text: str) -> List[str]:
    """
    Splits text into elements suitable for subtitling based on specific rules.

    Rules:
    1. Words (including hyphenated, elided) are base elements.
    2. Closing punctuation/units attach to the preceding word, preserving intermediate space.
    3. Opening punctuation attaches to the following word, preserving intermediate space.
    4. Spaces separate elements unless preserved by rules 2 & 3.
    5. Punctuation/units not adjacent to a word become separate elements.

    Args:
        text: The input string to split.

    Returns:
        A list of strings, where each string is a subtitle element.
    """
    token_regex = re.compile(
        r"([«(\[{“‘])"  # Group 1: Opening punctuation
        r"|(\w+(?:[-'’]\w+)*)"  # Group 2: Word (incl. hyphen, apostrophe)
        r"|([»)}\]”’?!;:,.$€%])"  # Group 3: Closing punctuation or unit
        r"|(\s+)"  # Group 4: Whitespace
        r"|(\S)"  # Group 5: Any other non-whitespace char
    )

    tokens: List[Tuple[str, Optional[str]]] = []
    for match in token_regex.finditer(text):
        token_text = match.group(0)
        token_type: Optional[str] = None  # Initialize token_type
        if match.group(1):
            token_type = T_OPEN_PUNC
        elif match.group(2):
            token_type = T_WORD
        elif match.group(3):
            token_type = T_CLOSE_PUNC_UNIT
        elif match.group(4):
            token_type = T_SPACE
        elif match.group(5):
            token_type = T_OTHER
        else:
            continue  # Should not happen if regex is exhaustive for non-empty matches
        tokens.append((token_text, token_type))

    elements: List[str] = []
    i = 0
    num_tokens = len(tokens)

    while i < num_tokens:
        token_text, token_type = tokens[i]

        if token_type == T_SPACE:
            i += 1
            continue

        current_element = token_text

        if token_type == T_OPEN_PUNC:
            idx_after_open, leading_space = _get_next_non_space(tokens, i + 1)

            if idx_after_open is not None and tokens[idx_after_open][1] == T_WORD:
                word_idx = idx_after_open
                word_text = tokens[word_idx][0]
                current_element += leading_space + word_text

                idx_after_word, trailing_space_after_word = _get_next_non_space(tokens, word_idx + 1)

                # Check for and consume sequence of closing punctuation/units
                last_consumed_idx_for_open_punc_sequence = word_idx  # Start after the word
                if idx_after_word is not None and tokens[idx_after_word][1] == T_CLOSE_PUNC_UNIT:
                    current_element += trailing_space_after_word + tokens[idx_after_word][0]
                    last_consumed_idx_for_open_punc_sequence = idx_after_word

                    # Consume further T_CLOSE_PUNC_UNIT
                    while True:
                        next_idx, space_before_next_punc = _get_next_non_space(tokens,
                                                                               last_consumed_idx_for_open_punc_sequence + 1)
                        if next_idx is not None and tokens[next_idx][1] == T_CLOSE_PUNC_UNIT:
                            current_element += space_before_next_punc + tokens[next_idx][0]
                            last_consumed_idx_for_open_punc_sequence = next_idx
                        else:
                            i = next_idx if next_idx is not None else num_tokens
                            break
                else:  # Word not followed by closing punctuation
                    i = idx_after_word if idx_after_word is not None else num_tokens

                elements.append(current_element)

            else:  # Opening punctuation not followed by a word
                elements.append(current_element)
                i += 1  # Move to the token after the opening punctuation

        elif token_type == T_WORD or token_type == T_OTHER:
            last_consumed_idx_for_word_sequence = i

            # Consume trailing T_CLOSE_PUNC_UNIT
            while True:
                idx_after_last, trailing_space = _get_next_non_space(tokens, last_consumed_idx_for_word_sequence + 1)
                if idx_after_last is not None and tokens[idx_after_last][1] == T_CLOSE_PUNC_UNIT:
                    current_element += trailing_space + tokens[idx_after_last][0]
                    last_consumed_idx_for_word_sequence = idx_after_last
                else:
                    i = idx_after_last if idx_after_last is not None else num_tokens
                    break
            elements.append(current_element)

        elif token_type == T_CLOSE_PUNC_UNIT:  # Standalone closing punctuation
            elements.append(current_element)
            i += 1

        else:  # Should not be reached if all types are handled
            i += 1

    return elements
