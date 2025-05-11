import math
from typing import List, Tuple, Dict, Union, Any
import logging

THRESHOLD_MERGE_MAGIC = 1.7
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
        max_chars: int,
        return_score: bool = False  # Nouveau paramètre pour contrôler le type de retour
) -> Union[List[str], List[List[Tuple[str, float]]]]:
    """
    Divise récursivement un segment.
    Retourne une liste de chaînes de caractères (sous-titres finaux pour ce segment)
    si return_score est False.
    Sinon, retourne une liste de segments (liste de listes de (element, score))
    pour permettre une utilisation ultérieure des scores.
    """

    current_segment_length = get_segment_length(segment)

    # Cas de base : le segment est suffisamment court ou vide
    if current_segment_length <= max_chars:
        if not segment:  # Si le segment initial est vide
            return []
        if return_score:
            # Retourne le segment lui-même (liste de tuples) encapsulé dans une liste
            return [segment]
        else:
            # Retourne le texte du segment concaténé
            return [" ".join([el_text for el_text, _ in segment])]

    best_split_point_k = -1
    highest_score = -1.0
    potential_splits: List[Dict[str, Any]] = [] # Any est utilisé ici comme dans votre code original pour le score
    best_overall_k = -1

    # Itérer sur les points de division possibles (après l'élément k)
    # On ne peut pas diviser après le dernier élément du segment
    for k in range(len(segment) - 1): # k va de 0 à len(segment) - 2
        element_text, score = segment[k]

        if score > highest_score:
            highest_score = score
            best_overall_k = k

        left_part = segment[:k + 1]
        right_part = segment[k + 1:]
        len_left = get_segment_length(left_part)
        len_right = get_segment_length(right_part)

        # Considérer ce point comme valide si les deux parties respectent min_chars
        if len_left >= min_chars and len_right >= min_chars:
            potential_splits.append({'index': k, 'score': score})
            logger.debug(
                f"Potentiel split après k={k} ('{element_text}', score={score:.2f}) - "
                f"Gauche:{len_left}, Droite:{len_right} >= min:{min_chars}"
            )

    if potential_splits:
        # Trier les divisions potentielles par score (décroissant)
        potential_splits.sort(key=lambda x: x['score'], reverse=True)
        best_split_point_k = potential_splits[0]['index']
        logger.debug(
            f"Choix du split (respectant min_chars) après k={best_split_point_k} "
            f"(score {potential_splits[0]['score']:.2f})"
        )
    elif best_overall_k != -1:
        # Fallback : Aucune division ne respecte min_chars des deux côtés.
        # Prendre le point avec le score global le plus élevé.
        best_split_point_k = best_overall_k
        logger.debug(
            f"Fallback : Choix du split après k={best_overall_k} (score le plus élevé {highest_score:.2f}), "
            f"ignorant la contrainte min_chars."
        )
    else:
        # Cas très improbable : segment > max_chars mais n'a qu'un seul élément, pas de scores,
        # ou len(segment) < 2 (auquel cas la boucle for k ne s'exécute pas).
        # Si len(segment) == 1 et current_segment_length > max_chars, c'est un mot très long.
        # Pour éviter une boucle infinie si le segment ne peut pas être divisé davantage
        # (par exemple, un seul mot très long qui dépasse max_chars),
        # ou si le segment est vide (déjà géré au début).
        if len(segment) <= 1: # Ne peut pas être splitté
            logger.warning(
                f"Segment trop long ('{current_segment_length}' chars) mais ne peut pas être divisé "
                f"(len={len(segment)}). Segment: {' '.join(s[0] for s in segment)}. "
                f"Retour du segment tel quel."
            )
            if return_score:
                return [segment]
            else:
                return [" ".join([el_text for el_text, _ in segment])]

        # Si len(segment) > 1 mais best_overall_k est resté -1 (pas de scores > -1.0, ou tous les scores sont égaux à -1.0)
        # Diviser approximativement au milieu.
        mid_idx = math.ceil(len(segment) / 2) - 1
        if mid_idx < 0: mid_idx = 0 # Assurer au moins un élément à gauche
        # S'assurer que mid_idx ne mène pas à une division après le dernier élément autorisé (len(segment)-2)
        if mid_idx >= len(segment) -1 : mid_idx = len(segment) - 2

        best_split_point_k = mid_idx
        logger.warning(
            f"Fallback Extrême : Long segment mais pas de point de division clair. "
            f"Division après l'index {best_split_point_k}."
        )

    # À ce stade, best_split_point_k devrait être un index valide pour la division [0, len(segment)-2]
    # Sauf si le segment était de longueur 1 et trop long (géré ci-dessus).
    if best_split_point_k == -1 : # Ne devrait pas arriver si len(segment) > 1
         logger.error(f"Erreur critique: best_split_point_k est -1 pour un segment de longueur {len(segment)}")
         # Sécurité: retourne le segment non divisé
         if return_score: return [segment]
         else: return [" ".join([el[0] for el in segment])]


    left_segment_part = segment[:best_split_point_k + 1]
    right_segment_part = segment[best_split_point_k + 1:]

    # Vérification de sécurité : si une partie est vide, cela indique un problème avec best_split_point_k.
    # Cela ne devrait pas se produire avec la logique de fallback et les vérifications précédentes.
    if not left_segment_part or not right_segment_part:
        logger.warning(
            f"Division invalide détectée (k={best_split_point_k}, gauche_vide={not left_segment_part}, "
            f"droite_vide={not right_segment_part}). "
            f"Retour du segment original pour éviter une erreur. Segment: {' '.join(s[0] for s in segment)}"
        )
        if return_score:
            return [segment] # Retourne le segment original (avant la tentative de division)
        else:
            return [" ".join([el_text for el_text, _ in segment])]

    # Appels récursifs, en passant le paramètre return_score
    # Le type de retour de left_res et right_res dépendra de la valeur de return_score
    left_res = recursive_split(left_segment_part, min_chars, max_chars, return_score)
    right_res = recursive_split(right_segment_part, min_chars, max_chars, return_score)

    # L'opérateur + fonctionne pour concaténer List[str] et List[List[Tuple[...]]]
    return left_res + right_res



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
                merge_threshold= THRESHOLD_MERGE_MAGIC,
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
        merge_threshold=merge_aggressiveness_threshold,
        return_score = True
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


def cutting_into_2_line(
        elements_with_scores: List[Tuple[str, float]],
        min_chars_by_line: int = 10,
        max_chars_by_line: int = 40,  # Augmenté pour un exemple plus réaliste
        punctuation_threshold: float = 0.5,
        use_punctuation_presplit: bool = True,
        merge_aggressiveness_threshold: float = 0.5
) -> List[List[str]]:  # Type de retour clarifié: List[List[str]] (chaque sous-liste a 1 ou 2 lignes)
    """
    Stratégie de découpe visant à produire des sous-titres sur une ou deux lignes.
    1. Pré-découpe par ponctuation.
    2. Fusionne agressivement les segments résultants.
    3. Découpe récursivement les segments fusionnés en morceaux d'environ 1 à 1.9 fois max_chars_by_line.
    4. Formate chaque morceau en 1 ou 2 lignes, respectant max_chars_by_line par ligne.
    """
    if not elements_with_scores:
        return []

    # Étape 1: Pré-découpe par ponctuation
    punctuation_chars = ['.', ',', ';', ':', '!', '?', '–', ')', ']', '.»', '"']
    segments_after_presplit: List[List[Tuple[str, float]]]
    if use_punctuation_presplit:
        segments_after_presplit = pre_split_by_punctuation(
            elements_with_scores,
            punctuation_chars,
            punctuation_threshold
        )
    else:
        # Si pas de pré-découpe, traiter l'ensemble comme un seul segment initial
        segments_after_presplit = [elements_with_scores] if elements_with_scores else []

    if not segments_after_presplit:
        return []

    # Étape 2: Fusion des segments pré-découpés
    segments_after_presplit_merged: List[List[Tuple[str, float]]] = []
    for segment in segments_after_presplit:
        if not segment: continue
        # NOTE: Appel à merge_strat avec return_score=False pour obtenir List[Tuple[str, float]]
        # compatible avec recursive_split.
        # Les longueurs min/max pour merge_strat pourraient être différentes, ici elles sont basées sur une ligne.
        segment_merged = merge_strat(
            segment,
            min_chars=min_chars_by_line,
            max_chars=max_chars_by_line,  # Ou peut-être max_chars_by_line * 1.9 si on fusionne déjà en vue de 2 lignes
            merge_threshold=merge_aggressiveness_threshold,
            return_score=False  # Pour que segment_merged soit List[Tuple[str, float]]
        )
        if segment_merged and isinstance(segment_merged[0], tuple):  # S'assurer que c'est bien List[Tuple[str,float]]
            segments_after_presplit_merged.append(segment_merged)  # type: ignore
        elif segment_merged:  # Si merge_strat retourne List[str] à cause d'un return_score=True mal interprété
            logger.warning(
                "merge_strat a retourné List[str] au lieu de List[Tuple[str,float]], tentative de conversion (simpliste)")
            # Ceci est une rustine, idéalement merge_strat est appelé correctement
            segments_after_presplit_merged.append([(word, 0.1) for word in " ".join(segment_merged).split()])

    # Étape 3: Découpe récursive des segments fusionnés
    # `double_line` contiendra des segments (List[Tuple[str, float]]) prêts à être formatés en 1 ou 2 lignes.
    intermediate_segments_for_formatting: List[List[Tuple[str, float]]] = []
    for i, segment_data in enumerate(segments_after_presplit_merged):
        logger.debug(
            f"\n  Traitement du segment fusionné {i + 1}/{len(segments_after_presplit_merged)} "
            f"(longueur {get_segment_length(segment_data)} chars) pour découpe récursive"
        )
        if segment_data:
            # max_len pour recursive_split est ~1.9x max_chars_by_line pour permettre de former 2 lignes ensuite.
            sub_segments = recursive_split(segment_data, min_chars_by_line, int(max_chars_by_line * 1.9),
                                           return_score=True)
            intermediate_segments_for_formatting.extend(sub_segments)  # type: ignore

    # Étape 4: Formatage final en une ou deux lignes
    final_two_line_subtitles: List[List[str]] = []
    for segment_to_format in intermediate_segments_for_formatting:  # segment_to_format est List[Tuple[str, float]]
        current_length = get_segment_length(segment_to_format)

        if not segment_to_format:
            continue

        if current_length <= max_chars_by_line:
            # Assez court pour une seule ligne
            final_two_line_subtitles.append([" ".join(el[0] for el in segment_to_format)])
            logger.debug(
                f"Formaté en une ligne (longueur {current_length}): {' '.join(el[0] for el in segment_to_format)}")
        else:
            # Trop long pour une ligne (mais <= max_chars_by_line * 1.9), essayer de diviser en deux.
            possible_splits = []
            # k_split est l'index du dernier élément de la première ligne potentielle
            for k_split in range(len(segment_to_format) - 1):
                first_line_elements = segment_to_format[:k_split + 1]
                second_line_elements = segment_to_format[k_split + 1:]

                len_l1 = get_segment_length(first_line_elements)
                len_l2 = get_segment_length(second_line_elements)

                # Vérifier si les deux lignes candidates respectent les contraintes de longueur
                if (min_chars_by_line <= len_l1 <= max_chars_by_line and
                        min_chars_by_line <= len_l2 <= max_chars_by_line):
                    score_of_split_element = segment_to_format[k_split][1]  # Score de l'élément avant la césure
                    balance = -abs(len_l1 - len_l2)  # Métrique d'équilibre (plus proche de 0 est mieux)
                    possible_splits.append({
                        'index': k_split,
                        'score': score_of_split_element,
                        'balance': balance,
                        'l1_elements': first_line_elements,
                        'l2_elements': second_line_elements,
                        'len_l1': len_l1,
                        'len_l2': len_l2
                    })

            if possible_splits:
                # Trier par score (décroissant) puis par équilibre (décroissant, i.e. moins négatif)
                possible_splits.sort(key=lambda x: (x['score'], x['balance']), reverse=True)
                best_split = possible_splits[0]

                line1_text = " ".join(el[0] for el in best_split['l1_elements'])
                line2_text = " ".join(el[0] for el in best_split['l2_elements'])
                final_two_line_subtitles.append([line1_text, line2_text])
                logger.debug(
                    f"Segment (long. {current_length}) divisé en deux lignes: ['{line1_text}' (long. {best_split['len_l1']}), '{line2_text}' (long. {best_split['len_l2']})] à l'index {best_split['index']}")
            else:
                # Fallback: Pas de division "parfaite" trouvée.
                # Tenter une division basée sur le meilleur score, même si les contraintes de longueur par ligne ne sont pas idéales.
                # Cela garantit une tentative de "couper en 2" si le segment est trop long pour une ligne.
                fallback_options = []
                for k_fallback in range(len(segment_to_format) - 1):
                    l1_elems = segment_to_format[:k_fallback + 1]
                    l2_elems = segment_to_format[k_fallback + 1:]
                    if l1_elems and l2_elems:  # S'assurer que les deux parties existent
                        fallback_options.append({
                            'index': k_fallback,
                            'score': segment_to_format[k_fallback][1],
                            'l1_elements': l1_elems,
                            'l2_elements': l2_elems
                        })

                if fallback_options:
                    fallback_options.sort(key=lambda x: x['score'], reverse=True)  # Trier par score
                    best_fallback_split = fallback_options[0]

                    line1_text = " ".join(el[0] for el in best_fallback_split['l1_elements'])
                    line2_text = " ".join(el[0] for el in best_fallback_split['l2_elements'])
                    final_two_line_subtitles.append([line1_text, line2_text])
                    len_fb_l1 = get_segment_length(best_fallback_split['l1_elements'])
                    len_fb_l2 = get_segment_length(best_fallback_split['l2_elements'])
                    logger.debug(
                        f"Fallback pour segment (long. {current_length}). Divisé en deux lignes (peuvent être hors limites): "
                        f"['{line1_text}' (long. {len_fb_l1}), '{line2_text}' (long. {len_fb_l2})]"
                    )
                else:
                    # Cas très improbable si len(segment_to_format) > 1:
                    # e.g., un seul mot très long qui a passé recursive_split.
                    # Dans ce cas, on le garde sur une seule ligne (qui sera trop longue).
                    single_line_text = " ".join(el[0] for el in segment_to_format)
                    final_two_line_subtitles.append([single_line_text])
                    logger.error(
                        f"Segment (long. {current_length}) n'a pas pu être divisé par fallback (e.g. mot unique trop long). "
                        f"Conservé en une ligne: '{single_line_text}'"
                    )
    return final_two_line_subtitles





