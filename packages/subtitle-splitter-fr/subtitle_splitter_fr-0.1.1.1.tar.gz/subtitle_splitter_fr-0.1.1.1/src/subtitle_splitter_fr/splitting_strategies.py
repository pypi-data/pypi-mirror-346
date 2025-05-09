import math
from typing import List, Tuple, Dict
import logging
logger = logging.getLogger(__name__)



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
                    logger.debug(f"Pre-split after: '{element}'")
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
            logger.debug(f"Potential split after k={k} ('{element_text}', score={score:.2f}) - Left:{len_left}, Right:{len_right} >= min:{min_chars}")

    if potential_splits:
        potential_splits.sort(key=lambda x: x['score'], reverse=True)
        best_split_point_k = potential_splits[0]['index']
        logger.debug(f"Chose split respecting min_chars after k={best_split_point_k} (score {potential_splits[0]['score']:.2f})")

    elif best_overall_k != -1:
        # Fallback: No split respects min_chars on both sides.
        # Take the point with the highest overall score.
        best_split_point_k = best_overall_k
        logger.debug(f"Fallback: Chose split after k={best_overall_k} (highest score {highest_score:.2f}), ignoring min_chars constraint.")
    else:
        # Highly unlikely case: segment > max_chars but has only one element or no scores?
        # To avoid infinite loop, split approximately in the middle.
        mid_idx = math.ceil(len(segment) / 2) - 1
        if mid_idx < 0: mid_idx = 0  # Ensure at least one element on the left
        best_split_point_k = mid_idx
        logger.warning(f"Extreme Fallback: Long segment but no clear split point. Splitting after index {best_split_point_k}.")

    left_segment_part = segment[:best_split_point_k + 1]
    right_segment_part = segment[best_split_point_k + 1:]

    if not left_segment_part or not right_segment_part:
        # This should ideally not happen if best_split_point_k is always valid (0 to len(segment)-2)
        # logger.warning(f"Invalid split detected (empty part), returning original segment text to avoid error.")
        return [segment_text]

        # logger.debug(f"Recursing Left ({len(left_segment_part)} items), Right ({len(right_segment_part)} items)")
    return recursive_split(left_segment_part, min_chars, max_chars) + \
        recursive_split(right_segment_part, min_chars, max_chars)


def split_rec_strat(
        elements_with_scores: List[Tuple[str, float]],
        min_chars: int = 30,
        max_chars: int = 70,
        punctuation_threshold: float = 0.5,
        use_punctuation: bool = True  # Renamed from use_ponctuation for consistency
) -> List[str]:
    """
    Main function using the recursive splitting strategy.
    """
    punctuation_chars = ['.', ',', ';', ':', '!', '?', '–', ')', ']', '.»', '"']  # Standard list

    initial_segments: List[List[Tuple[str, float]]]
    if use_punctuation:
        initial_segments = pre_split_by_punctuation(elements_with_scores, punctuation_chars, punctuation_threshold)
    else:
        initial_segments = []

    if not initial_segments and elements_with_scores:  # If pre-splitting yielded nothing (or was skipped) and there's data
        initial_segments = [elements_with_scores]
    elif not elements_with_scores:  # Handle case where input is empty
        initial_segments = []


    final_subtitles: List[str] = []
    for i, segment_data in enumerate(initial_segments):
        logger.debug(f"\n  Processing Initial Segment {i+1}/{len(initial_segments)} (length {get_segment_length(segment_data)} chars)")
        if segment_data:
            sub_lines = recursive_split(segment_data, min_chars, max_chars)
            final_subtitles.extend(sub_lines)

    return final_subtitles


def merge_strat(segments,
                min_chars,
                max_chars,
                merge_threshold = 1.7,
                return_score = False):
    seg_with_scores = []
    for seg1, seg2 in zip(segments[:-1], segments[1:]):
        w1, s1 = seg1
        w2, s2 = seg2
        score_tot_1 = s1+max(0,(len(w1)+len(w2)-min_chars)/(max_chars-min_chars))
        seg_with_scores.append((w1, s1, score_tot_1))
    wl, sl =segments[-1]
    seg_with_scores.append((wl, sl, 100))

    index_min = min(range(len(seg_with_scores)), key=lambda i: seg_with_scores[i][2])

    while seg_with_scores[index_min][2]<merge_threshold:
        w1, s1, score_tot_1= seg_with_scores[index_min]
        w2, s2, score_tot_2= seg_with_scores[index_min + 1]

        seg_with_scores[index_min] = (w1+" "+w2, s2, score_tot_2+(len(w1)+1)/(max_chars-min_chars))
        if index_min >0:
            w0, s0, score_tot_0 = seg_with_scores[index_min - 1]
            seg_with_scores[index_min-1] = (w0, s0, score_tot_0 + (len(w2) + 1) / (max_chars - min_chars))

        del seg_with_scores[index_min+1]
        index_min = min(range(len(seg_with_scores)), key=lambda i: seg_with_scores[i][2])

    if return_score:
        return_value =[t for t, _, _ in seg_with_scores]
    else:
        return_value =[(t,s) for t, s, _ in seg_with_scores]

    return return_value


def hybride_strat(
        elements_with_scores: List[Tuple[str, float]],
        min_chars: int = 30,
        max_chars: int = 70,
        punctuation_threshold: float = 0.5,
        use_punctuation_presplit: bool = True,
        merge_aggressiveness_threshold: float = 0.5,
) -> List[str]:
    """
    Hybrid splitting strategy:
    1. Pre-splits by punctuation.
    2. Merges the resulting segments aggressively.
    3. Recursively splits the merged segments.
    """
    if not elements_with_scores:
        return []

    # Step 1: Pre-split by punctuation
    punctuation_chars = ['.', ',', ';', ':', '!', '?', '–', ')', ']', '.»', '"']

    segments_after_presplit: List[List[Tuple[str, float]]]
    if use_punctuation_presplit:
        segments_after_presplit = pre_split_by_punctuation(
            elements_with_scores,
            punctuation_chars,
            punctuation_threshold
        )
    else:
        segments_after_presplit = [elements_with_scores]

    if not segments_after_presplit:  # If presplit resulted in nothing (e.g. empty input)
        return []

    segments_after_presplit_merged = []
    for segment in segments_after_presplit:
        segment_merged = merge_strat(
        segment,
        min_chars=min_chars,  # min_chars/max_chars for merge might be different
        max_chars=max_chars,  # e.g., allow longer segments here
        merge_threshold=merge_aggressiveness_threshold
    )
        segments_after_presplit_merged.append(segment_merged)

    final_subtitles: List[str] = []
    for i, segment_data in enumerate(segments_after_presplit_merged):
        logger.debug(
            f"\n  Processing Initial Segment {i + 1}/{len(segments_after_presplit_merged)} (length {get_segment_length(segment_data)} chars)")
        if segment_data:
            sub_lines = recursive_split(segment_data, min_chars, max_chars)
            final_subtitles.extend(sub_lines)

    return final_subtitles



