from typing import List, Literal, Tuple, Any

import nltk
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from importlib_resources import files
from transformers import AutoTokenizer

from subtitle_splitter_fr.preprocessing_utils import split_text_into_elements
from subtitle_splitter_fr.splitting_strategies import merge_strat, split_rec_strat, hybride_strat, cutting_into_2_line

import logging

logger = logging.getLogger(__name__)

# --- Configuration Hugging Face ---
HF_REPO_ID = "JulesGo/subtitle-splitter-fr"
HF_MODEL_FILENAME = "camembert_regression.onnx"

def get_onnx_model_path():
    """
    Downloads the ONNX model from Hugging Face Hub if it's not already cached locally.
    Returns the local path to the model file.
    """
    try:
        # hf_hub_download handles downloading and caching
        model_path = hf_hub_download(repo_id=HF_REPO_ID, filename=HF_MODEL_FILENAME)
        print(f"ONNX model available locally at: {model_path}")
        return model_path
    except Exception as e:
        print(f"Error downloading model from Hugging Face Hub: {e}")
        raise # Re-raise the exception if the download fails


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
            model_local_path = get_onnx_model_path()

            try:
                self.session = ort.InferenceSession(str(model_local_path), providers=providers)
            except Exception as e:
                raise RuntimeError(f"Erreur lors du chargement du modèle ONNX depuis {model_local_path}: {e}") from e
            tokenizer_path_obj = files("subtitle_splitter_fr").joinpath(self._TOKENIZER_SUBPATH)

            if not tokenizer_path_obj.is_dir():
                logger.error(f"Tokenizer directory not found or invalid: {tokenizer_path_obj}")
                raise FileNotFoundError(f"Tokenizer directory not found or invalid: {tokenizer_path_obj}")

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

    def split(self, text: str, length: int = 15, method: Literal["MERGE", "SPLIT", "HYBRIDE"] = "MERGE") -> List[str]:
        if not text or text.isspace():
            return []

        try:
            elements_scores_predicts = self._predict_scores(text)
        except Exception as e:
            logger.error(f"Error predicting scores for text: '{text[:50]}...'. Error: {e}")
            return [text]

        if not elements_scores_predicts:
            return [text] if text.strip() else []

        min_chars = max(7, int(length * 2 / 3))
        max_chars = 2 * min_chars

        try:
            if method == "MERGE":
                sub_titles = merge_strat(
                    elements_scores_predicts,
                    min_chars=min_chars,
                    max_chars=max_chars,
                )
            elif method == "SPLIT":
                sub_titles = split_rec_strat(
                    elements_scores_predicts,
                    min_chars=min_chars,
                    max_chars=max_chars,
                )
            elif method == "HYBRIDE":
                sub_titles = hybride_strat(
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
    def split_two_line(self, text: str, length: int = 15) -> list[str] | list[Any] | list[list[str]]:
        if not text or text.isspace():
            return []

        try:
            elements_scores_predicts = self._predict_scores(text)
        except Exception as e:
            logger.error(f"Error predicting scores for text: '{text[:50]}...'. Error: {e}")
            return [text]

        if not elements_scores_predicts:
            return [text] if text.strip() else []

        min_chars = max(7, int(length * 2 / 3))
        max_chars = 2 * min_chars

        sub_titles = cutting_into_2_line(
            elements_scores_predicts,
            min_chars_by_line=min_chars,
            max_chars_by_line=max_chars,
        )

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

if __name__ == "__main__":
    splitter = Splitter()
    texte_exemple = "Le château se dressait sur une colline escarpée, dominant la vallée sinueuse où la rivière serpentait lentement, reflétant les rayons du soleil couchant. À l'intérieur, de vastes salles résonnaient du silence des siècles passés, tandis que des tapisseriesComplexes ornaient les murs de pierre froide, racontant des histoires oubliées de chevaliers et de dames. Dehors, le vent murmurait à travers les arbres centenaires, emportant avec lui les échos d'un temps révolu."
    sous_titres = splitter.split_two_line(texte_exemple, length=10)

    print("\nSous-titres générés :")
    for i, subs in enumerate(sous_titres):
        f=", ".join([str(len(s)) for s in subs])

        print(f"{i + 1}: {subs} ({f} chars)")