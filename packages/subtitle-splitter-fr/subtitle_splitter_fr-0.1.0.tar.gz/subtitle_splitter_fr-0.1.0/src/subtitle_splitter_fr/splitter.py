from typing import List, Literal, Tuple

import nltk
import numpy as np
import onnxruntime as ort
from importlib_resources import files
from transformers import AutoTokenizer

from subtitle_splitter_fr.preprocessing_utils import split_text_into_elements
from subtitle_splitter_fr.splitting_strategies import merge, split_subtitles_recursive

import logging

logger = logging.getLogger(__name__)


class Splitter:
    _MODEL_SUBPATH = "models/camembert_regression.onnx"
    _TOKENIZER_SUBPATH = "models/tokenizer"
    SEP_TOKEN_NAME = "<sep_secable>"
    MAX_LENGTH = 512

    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except (nltk.downloader.DownloadError, LookupError):
            logger.info("NLTK 'punkt_tab' resource not found, attempting to download.")
            try:
                nltk.download('punkt_tab', quiet=True)
            except Exception as e:
                logger.error(f"Failed to download 'punkt_tab': {e}. Sentence tokenization might be affected.")

        providers = ['CPUExecutionProvider']

        try:
            model_path_obj = files("subtitle_splitter_fr").joinpath(self._MODEL_SUBPATH)
            tokenizer_path_obj = files("subtitle_splitter_fr").joinpath(self._TOKENIZER_SUBPATH)

            if not model_path_obj.exists():
                logger.error(f"ONNX model file not found: {model_path_obj}")
                raise FileNotFoundError(f"ONNX model file not found: {model_path_obj}")
            if not tokenizer_path_obj.is_dir():
                logger.error(f"Tokenizer directory not found or invalid: {tokenizer_path_obj}")
                raise FileNotFoundError(f"Tokenizer directory not found or invalid: {tokenizer_path_obj}")

            self.session = ort.InferenceSession(str(model_path_obj), providers=providers)
            self.tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path_obj))
            self.SEP_TOKEN_ID = self.tokenizer.convert_tokens_to_ids(self.SEP_TOKEN_NAME)

            if self.SEP_TOKEN_ID == self.tokenizer.unk_token_id:
                logger.warning(
                    f"Separator token '{self.SEP_TOKEN_NAME}' is unknown to the tokenizer. "
                    "This might lead to unexpected behavior."
                )

        except FileNotFoundError as e:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during model or tokenizer loading: {e}")
            raise

    def split(self, text: str, length: int = 15, method: Literal["MERGE", "SPLIT"] = "MERGE") -> List[str]:
        if not text or text.isspace():
            return []

        try:
            elements_scores_predicts = self._predict_scores(text)
        except Exception as e:
            logger.error(f"Error predicting scores for text: '{text[:50]}...'. Error: {e}")
            return [text]

        if not elements_scores_predicts:
            return [text] if text.strip() else []

        min_chars = max(10, int(length * 2 / 3))
        max_chars = 2 * min_chars

        sub_titles = []
        try:
            if method == "MERGE":
                sub_titles = merge(
                    elements_scores_predicts,
                    min_chars=min_chars,
                    max_chars=max_chars,
                )
            elif method == "SPLIT":
                sub_titles = split_subtitles_recursive(
                    elements_scores_predicts,
                    min_chars=min_chars,
                    max_chars=max_chars,
                )
            else:
                logger.error(f"Unknown splitting method: {method}. Returning original text.")
                return [text]
        except Exception as e:
            logger.error(f"Error during splitting method '{method}': {e}. Returning original text.")
            return [text]

        return sub_titles

    def _predict_scores(self, text: str) -> List[Tuple[str, float]]:
        try:
            sentences_proprocesses = preprocess_inference(text, self.tokenizer, self.MAX_LENGTH, self.SEP_TOKEN_ID,
                                                          split_text_into_elements)
        except Exception as e:
            logger.error(f"Error during preprocessing in _predict_scores for text: '{text[:50]}...'. Error: {e}")
            return []

        elements_with_scores_tot: List[Tuple[str, float]] = []

        if not sentences_proprocesses:
            return []

        for inputs, elements, sep_indices in sentences_proprocesses:
            if inputs is None or not elements:
                continue

            try:
                ort_outputs = self.session.run(["logits"], inputs)
                logits = ort_outputs[0]
            except Exception as e:
                logger.error(f"Error during ONNX inference: {e}")
                continue

            scores_numpy = 1 / (1 + np.exp(-logits))
            all_token_scores = scores_numpy.squeeze()

            if all_token_scores.ndim == 0:
                all_token_scores = np.array([all_token_scores.item()])
            elif all_token_scores.ndim > 1:
                logger.error(f"Unexpected shape for all_token_scores: {all_token_scores.shape}. Expected 1D or 0D.")
                continue

            predicted_scores = []
            if len(all_token_scores) > 0:
                for index in sep_indices:
                    if index < len(all_token_scores):
                        predicted_scores.append(all_token_scores[index])
                    else:
                        pass

            num_scores = len(predicted_scores)
            elements_with_scores_tot.extend(list(zip(elements[:num_scores], predicted_scores)))

        return elements_with_scores_tot


def preprocess_inference(text: str, tokenizer, max_length: int, sep_token_id: int, split_text_into_elements_func) -> \
List[Tuple[dict, List[str], List[int]]]:
    if not text or text.isspace():
        return []

    try:
        sentences = nltk.sent_tokenize(text)
    except Exception as e:
        logger.error(f"Error tokenizing sentences with NLTK for text: '{text[:50]}...'. Error: {e}")
        return []

    sentences_preprocess: List[Tuple[dict, List[str], List[int]]] = []
    sentences_elements: List[Tuple[List[int], List[str]]] = []

    for sentence in sentences:
        try:
            elements = split_text_into_elements_func(sentence)
        except Exception as e:
            logger.error(f"Error splitting elements for sentence: '{sentence[:50]}...'. Error: {e}")
            continue

        input_ids_sentence: List[int] = []
        elements_sentence: List[str] = []

        for element in elements:
            try:
                element_ids = tokenizer.encode(element, add_special_tokens=False)
            except Exception as e:
                logger.error(f"Error encoding element: '{element}'. Error: {e}")
                continue

            if input_ids_sentence and (len(input_ids_sentence) + len(element_ids) + 1 > max_length - 2):
                if input_ids_sentence:
                    sentences_elements.append((input_ids_sentence, elements_sentence))

                input_ids_sentence = []
                elements_sentence = []

            input_ids_sentence.extend(element_ids + [sep_token_id])
            elements_sentence.append(element)

        if input_ids_sentence:
            sentences_elements.append((input_ids_sentence, elements_sentence))

    if not sentences_elements:
        return []

    input_ids_current: List[int] = [tokenizer.cls_token_id]
    elements_currents: List[str] = []

    for input_ids_chunk, elements_chunk in sentences_elements:
        if input_ids_current and (len(input_ids_current) + len(input_ids_chunk) + 1 > max_length):
            if len(input_ids_current) > 1:
                input_ids_current.append(tokenizer.sep_token_id)

                padding_length = max_length - len(input_ids_current)
                attention_mask = [1] * len(input_ids_current)
                if padding_length < 0:
                    logger.error(
                        f"Negative padding calculated ({padding_length}) for batch. Current length: {len(input_ids_current)}, max_length: {max_length}")
                    padding_length = 0

                if padding_length > 0:
                    input_ids_current.extend([tokenizer.pad_token_id] * padding_length)
                    attention_mask.extend([0] * padding_length)

                input_ids_current = input_ids_current[:max_length]
                attention_mask = attention_mask[:max_length]

                if elements_currents or len(input_ids_current) > 2:
                    sentences_preprocess.append((
                        {
                            "input_ids": np.array([input_ids_current], dtype=np.int64),
                            "attention_mask": np.array([attention_mask], dtype=np.int64),
                        },
                        elements_currents,
                        [i for i, x in enumerate(input_ids_current) if x == sep_token_id],
                    ))

            input_ids_current = [tokenizer.cls_token_id] + input_ids_chunk
            elements_currents = elements_chunk
        else:
            input_ids_current.extend(input_ids_chunk)
            elements_currents.extend(elements_chunk)

    if len(input_ids_current) > 1:
        input_ids_current.append(tokenizer.sep_token_id)

        padding_length = max_length - len(input_ids_current)
        attention_mask = [1] * len(input_ids_current)
        if padding_length < 0:
            logger.error(
                f"Negative padding calculated ({padding_length}) for the last batch. Length: {len(input_ids_current)}, max_length: {max_length}")
            padding_length = 0

        if padding_length > 0:
            input_ids_current.extend([tokenizer.pad_token_id] * padding_length)
            attention_mask.extend([0] * padding_length)

        input_ids_current = input_ids_current[:max_length]
        attention_mask = attention_mask[:max_length]

        if elements_currents or len(input_ids_current) > 2:
            sentences_preprocess.append((
                {
                    "input_ids": np.array([input_ids_current], dtype=np.int64),
                    "attention_mask": np.array([attention_mask], dtype=np.int64)
                },
                elements_currents,
                [i for i, x in enumerate(input_ids_current) if x == sep_token_id],
            ))

    return sentences_preprocess


def find_zero_score_series(elements_with_scores: List[Tuple[str, float]], zero_threshold: float = 0.2) -> List[
    Tuple[int, int, int]]:
    zero_series: List[Tuple[int, int, int]] = []
    current_series_start = -1
    current_series_chars = 0

    for i, (element, score) in enumerate(elements_with_scores):
        is_zero = score < zero_threshold

        if is_zero and current_series_start == -1:
            current_series_start = i
            current_series_chars = len(element)
        elif is_zero and current_series_start != -1:
            current_series_chars += len(element) + 1
        elif not is_zero and current_series_start != -1:
            zero_series.append((current_series_start, i - 1, current_series_chars))
            current_series_start = -1
            current_series_chars = 0

    if current_series_start != -1:
        zero_series.append((current_series_start, len(elements_with_scores) - 1, current_series_chars))

    return zero_series
