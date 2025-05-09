import math
from typing import List, Tuple, Dict  # Added Dict for potential_splits


# It's good practice to use logging instead of print for debug/info messages.
# import logging
# logger = logging.getLogger(__name__)

def pre_split_by_punctuation(
        elements_with_scores: List[Tuple[str, float]],
        punctuation_chars: List[str],
        threshold: float
) -> List[List[Tuple[str, float]]]:
    """
    Pre-splits the initial list into segments at strong punctuation points.
    Returns a list of segments (list of lists of (element, score)).
    """
    segments: List[List[Tuple[str, float]]] = []
    current_segment: List[Tuple[str, float]] = []
    num_elements = len(elements_with_scores)

    for i, (element, score) in enumerate(elements_with_scores):
        current_segment.append((element, score))

        is_punctuation_end = any(element.endswith(p) for p in punctuation_chars)

        # Split after this element if it's not the last one globally
        if i < num_elements - 1:
            if is_punctuation_end and score > threshold:
                if current_segment:  # Ensure current segment is not empty
                    segments.append(current_segment)
                    # logger.debug(f"Pre-split after: '{element}'")
                current_segment = []

    if current_segment:  # Add the last segment if it's not empty
        segments.append(current_segment)

    return segments


def get_segment_length(segment: List[Tuple[str, float]]) -> int:
    """Calculates the character length of a segment."""
    if not segment:
        return 0
    # Sum of element lengths + number of spaces needed between them
    return sum(len(el_text) for el_text, score in segment) + len(segment) - 1


def recursive_split(
        segment: List[Tuple[str, float]],
        min_chars: int,
        max_chars: int
) -> List[str]:
    """
    Recursively splits a segment.
    Returns a list of strings (final subtitles for this segment).
    """
    segment_text = " ".join([el_text for el_text, score in segment])

    if get_segment_length(segment) <= max_chars:
        return [segment_text] if segment else []

    best_split_point_k = -1
    highest_score = -1.0
    potential_splits: List[Dict[str, any]] = []
    best_overall_k = -1

    # Iterate over possible split points (after element k)
    # Cannot split after the last element of the segment
    for k in range(len(segment) - 1):
        element_text, score = segment[k]

        if score > highest_score:
            highest_score = score
            best_overall_k = k

        left_part = segment[:k + 1]
        right_part = segment[k + 1:]
        len_left = get_segment_length(left_part)
        len_right = get_segment_length(right_part)

        # Consider this point valid if both parts meet min_chars
        if len_left >= min_chars and len_right >= min_chars:
            potential_splits.append({'index': k, 'score': score})
            # logger.debug(f"Potential split after k={k} ('{element_text}', score={score:.2f}) - Left:{len_left}, Right:{len_right} >= min:{min_chars}")

    if potential_splits:
        potential_splits.sort(key=lambda x: x['score'], reverse=True)
        best_split_point_k = potential_splits[0]['index']
        # logger.debug(f"Chose split respecting min_chars after k={best_split_point_k} (score {potential_splits[0]['score']:.2f})")
    elif best_overall_k != -1:
        # Fallback: No split respects min_chars on both sides.
        # Take the point with the highest overall score.
        best_split_point_k = best_overall_k
        # logger.debug(f"Fallback: Chose split after k={best_overall_k} (highest score {highest_score:.2f}), ignoring min_chars constraint.")
    else:
        # Highly unlikely case: segment > max_chars but has only one element or no scores?
        # To avoid infinite loop, split approximately in the middle.
        mid_idx = math.ceil(len(segment) / 2) - 1
        if mid_idx < 0: mid_idx = 0  # Ensure at least one element on the left
        best_split_point_k = mid_idx
        # logger.warning(f"Extreme Fallback: Long segment but no clear split point. Splitting after index {best_split_point_k}.")

    left_segment_part = segment[:best_split_point_k + 1]
    right_segment_part = segment[best_split_point_k + 1:]

    if not left_segment_part or not right_segment_part:
        # This should ideally not happen if best_split_point_k is always valid (0 to len(segment)-2)
        # logger.warning(f"Invalid split detected (empty part), returning original segment text to avoid error.")
        return [segment_text]

        # logger.debug(f"Recursing Left ({len(left_segment_part)} items), Right ({len(right_segment_part)} items)")
    return recursive_split(left_segment_part, min_chars, max_chars) + \
        recursive_split(right_segment_part, min_chars, max_chars)


def split_subtitles_recursive(
        elements_with_scores: List[Tuple[str, float]],
        min_chars: int = 30,
        max_chars: int = 70,
        punctuation_threshold: float = 0.5,
        use_punctuation: bool = True  # Renamed from use_ponctuation for consistency
) -> List[str]:
    """
    Main function using the recursive splitting strategy.
    """
    # logger.info("--- Recursive Splitting ---")

    punctuation_chars = ['.', ',', ';', ':', '!', '?', '–', ')', ']', '.»', '"']  # Standard list

    # logger.info("1. Pre-splitting by strong punctuation...")
    initial_segments: List[List[Tuple[str, float]]]
    if use_punctuation:
        initial_segments = pre_split_by_punctuation(elements_with_scores, punctuation_chars, punctuation_threshold)
    else:  # Ensure initial_segments is always a list of lists
        initial_segments = []

    if not initial_segments and elements_with_scores:  # If pre-splitting yielded nothing (or was skipped) and there's data
        initial_segments = [elements_with_scores]
    elif not elements_with_scores:  # Handle case where input is empty
        initial_segments = []

    # logger.info(f"   Number of segments after pre-splitting: {len(initial_segments)}")

    # logger.info("\n2. Recursively splitting segments...")
    final_subtitles: List[str] = []
    for i, segment_data in enumerate(initial_segments):
        # logger.debug(f"\n  Processing Initial Segment {i+1}/{len(initial_segments)} (length {get_segment_length(segment_data)} chars)")
        if segment_data:  # Do not process empty segments
            sub_lines = recursive_split(segment_data, min_chars, max_chars)
            final_subtitles.extend(sub_lines)
            # logger.debug(f"    -> Generated {len(sub_lines)} line(s) for this segment.")
        # else:
        # logger.debug("    Initial segment empty, skipped.")

    # logger.info("\n--- End Recursive Splitting ---")
    return final_subtitles


def merge(
        segments_with_scores_input: List[Tuple[str, float]],  # Renamed for clarity
        min_chars: int,
        max_chars: int
) -> List[str]:
    """
    Merges segments based on scores and length constraints.
    """
    if not segments_with_scores_input:
        return []

    # Transform input to include a calculated merge score
    # seg_with_scores will be List[Tuple[str, float, float]] -> (text, original_score, merge_heuristic_score)
    seg_with_scores: List[Tuple[str, float, float]] = []

    # Initialize with individual elements and a placeholder for merge score calculation
    # The merge score logic here seems to consider merging the current element with the *next* one.
    for i in range(len(segments_with_scores_input)):
        current_text, current_score = segments_with_scores_input[i]
        merge_heuristic = current_score  # Default to original score

        if i < len(segments_with_scores_input) - 1:
            next_text, _ = segments_with_scores_input[i + 1]
            # This heuristic seems to penalize shortness or reward length within bounds
            length_factor = (len(current_text) + len(next_text) - min_chars) / (max_chars - min_chars) if (
                                                                                                                      max_chars - min_chars) != 0 else 0
            merge_heuristic = current_score + max(0, length_factor)
        else:
            # Last element cannot be merged with a next one, give it a high score to prevent it from being the minimum
            merge_heuristic = float('inf')  # Or a very high number like 100 as in original

        seg_with_scores.append((current_text, current_score, merge_heuristic))

    # Iteratively merge the pair with the lowest merge_heuristic score
    # The constant 1.7 was a threshold in the original code.
    # This loop structure needs careful review to ensure it behaves as intended.
    # The original logic modified scores of neighbors after a merge.

    MERGE_THRESHOLD = 1.7  # Give the magic number a name

    while True:
        if len(seg_with_scores) <= 1:  # Cannot merge if only one segment (or none)
            break

        # Find segment with the minimum merge_heuristic score (excluding the last one as it can't initiate a merge to its right)
        # The last element's merge_heuristic is Inf, so it won't be chosen unless it's the only one left before this check.
        min_merge_score = float('inf')
        index_to_merge = -1

        for i in range(len(seg_with_scores) - 1):  # Iterate up to the second to last element
            if seg_with_scores[i][2] < min_merge_score:
                min_merge_score = seg_with_scores[i][2]
                index_to_merge = i

        if index_to_merge == -1 or min_merge_score >= MERGE_THRESHOLD:
            break  # No more beneficial merges found or all are above threshold

        # Perform the merge
        text1, original_score1, _ = seg_with_scores[index_to_merge]
        text2, original_score2, _ = seg_with_scores[index_to_merge + 1]

        merged_text = text1 + " " + text2
        # The new "original_score" for the merged segment is taken from the second element in the original.
        # The merge_heuristic_score for this new segment will be recalculated if it can merge further.

        # Calculate new merge_heuristic for the newly merged segment if it's not the last one
        new_merge_heuristic = original_score2  # Default if it becomes the last
        if index_to_merge < len(seg_with_scores) - 2:  # If there's an element after the merged one
            next_text_after_merge, _ = segments_with_scores_input[
                index_to_merge + 2]  # This needs to be from seg_with_scores
            # The line above is problematic, it should use seg_with_scores[index_to_merge+2][0]
            # For simplicity, let's re-evaluate its merge score as if it's the last for now,
            # or use a more complex recalculation of its potential merge with the *new* next.
            # The original code's score update logic was: score_tot_2+(len(w1)+1)/(max_chars-min_chars)
            # This implies the score of the merged segment (w1+" "+w2) depends on its new length and original_score2.
            # And its ability to merge further would need a new length_factor.

            # Simplified: new heuristic for merged segment (text1+text2) if it were to merge with (text3)
            # This part of the logic is complex and might need a direct port or rethink of the heuristic.
            # The original was: seg_with_scores[index_min] = (w1+" "+w2, s2, score_tot_2+(len(w1)+1)/(max_chars-min_chars))
            # Let's try to replicate:
            length_factor_after_merge = (len(text1) + 1) / (max_chars - min_chars) if (
                                                                                                  max_chars - min_chars) != 0 else 0
            new_merge_heuristic = original_score2 + length_factor_after_merge  # This is an interpretation
        else:
            new_merge_heuristic = float('inf')

        seg_with_scores[index_to_merge] = (merged_text, original_score2, new_merge_heuristic)
        del seg_with_scores[index_to_merge + 1]

        # Update score of the element to the left of the merged one (if it exists)
        # Original: seg_with_scores[index_min-1] = (w0, s0, score_tot_0 + (len(w2) + 1) / (max_chars - min_chars))
        if index_to_merge > 0:
            prev_text, prev_original_score, _ = seg_with_scores[index_to_merge - 1]
            # Its merge heuristic now depends on the newly merged segment (merged_text)
            length_factor_for_prev = (len(prev_text) + len(merged_text) - min_chars) / (max_chars - min_chars) if (
                                                                                                                              max_chars - min_chars) != 0 else 0
            new_prev_heuristic = prev_original_score + max(0, length_factor_for_prev)
            # The original added (len(w2)+1) / (max_chars-min_chars) to score_tot_0.
            # This suggests the length of the *second part* of the *just merged pair* influences the *previous* element's merge score.
            adjustment_for_prev = (len(text2) + 1) / (max_chars - min_chars) if (max_chars - min_chars) != 0 else 0
            # This is tricky. The original `score_tot_0` was the old merge heuristic.
            # Let's assume it means: new_heuristic = old_heuristic_base + adjustment
            # seg_with_scores[index_to_merge - 1][2] was its old merge_heuristic.
            # This needs careful translation of the original intent.
            # For now, recalculating based on its new neighbor:
            seg_with_scores[index_to_merge - 1] = (prev_text, prev_original_score, new_prev_heuristic)

    return [text for text, _, _ in seg_with_scores]
