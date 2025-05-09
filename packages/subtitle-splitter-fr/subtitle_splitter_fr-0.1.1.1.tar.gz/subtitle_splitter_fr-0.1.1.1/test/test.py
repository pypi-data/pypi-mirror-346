import unittest
from unittest.mock import patch, MagicMock, call
import numpy as np

from subtitle_splitter_fr.splitter import Splitter, preprocess_inference, find_zero_score_series


# Assuming your Splitter class and other functions are in a module named 'splitter_module'
# Adjust the import path according to your project structure.
# For this example, let's assume the Splitter code is in 'splitter_module.py'
# and the helper functions are also accessible or will be mocked

# We will also need to be able to mock these if they are not part of splitter_module
# or if we want to test functions in isolation.
# For now, let's assume they are imported by splitter_module or we mock their calls.
# from subtitle_splitter_fr.models.preprocessing_utils import split_text_into_elements
# from subtitle_splitter_fr.splitting_strategies import merge, split_subtitles_recursive


class TestSplitter(unittest.TestCase):

    @patch('splitter_module.nltk.download')
    @patch('splitter_module.nltk.data.find')
    @patch('splitter_module.files')
    @patch('splitter_module.ort.InferenceSession')
    @patch('splitter_module.AutoTokenizer.from_pretrained')
    def setUp(self, mock_from_pretrained, mock_inference_session, mock_files, mock_nltk_find, mock_nltk_download):
        # Configure mocks for successful initialization
        mock_nltk_find.side_effect = LookupError  # Simulate NLTK resource not found initially

        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = True
        mock_path_obj.is_dir.return_value = True  # For tokenizer path
        mock_files.return_value.joinpath.return_value = mock_path_obj

        mock_tokenizer_instance = MagicMock()
        mock_tokenizer_instance.convert_tokens_to_ids.return_value = 12345  # Dummy SEP_TOKEN_ID
        mock_tokenizer_instance.unk_token_id = 0
        mock_tokenizer_instance.cls_token_id = 101
        mock_tokenizer_instance.sep_token_id = 102  # Model's own SEP, not custom
        mock_tokenizer_instance.pad_token_id = 0
        mock_from_pretrained.return_value = mock_tokenizer_instance

        mock_session_instance = MagicMock()
        mock_inference_session.return_value = mock_session_instance

        self.splitter = Splitter()
        self.splitter.tokenizer = mock_tokenizer_instance  # Ensure the mock is used
        self.splitter.session = mock_session_instance  # Ensure the mock is used

    def test_splitter_initialization_nltk_download_called(self):
        # Check if nltk.download was called during setUp
        # setUp already creates a splitter instance
        # The mock for nltk.data.find is set to raise LookupError, so download should be called.
        self.splitter.nltk.download.assert_called_once_with('punkt_tab', quiet=True)

    @patch('splitter_module.files')
    def test_splitter_initialization_file_not_found(self, mock_files):
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = False  # Simulate model file not found
        mock_files.return_value.joinpath.return_value = mock_path_obj
        with self.assertRaises(FileNotFoundError):
            Splitter()

    def test_split_empty_text(self):
        self.assertEqual(self.splitter.split(""), [])
        self.assertEqual(self.splitter.split("   "), [])

    @patch('splitter_module.Splitter._predict_scores')
    @patch('splitter_module.merge')  # Assuming 'merge' is importable/patchable this way
    def test_split_merge_method(self, mock_merge, mock_predict_scores):
        mock_predict_scores.return_value = [("element1", 0.8), ("element2", 0.7)]
        mock_merge.return_value = ["merged subtitle"]

        result = self.splitter.split("some text", method="MERGE")

        mock_predict_scores.assert_called_once_with("some text")
        mock_merge.assert_called_once_with(
            [("element1", 0.8), ("element2", 0.7)],
            min_chars=10,  # 15 * 2/3
            max_chars=20  # 10 * 2
        )
        self.assertEqual(result, ["merged subtitle"])

    @patch('splitter_module.Splitter._predict_scores')
    @patch('splitter_module.split_subtitles_recursive')  # Assuming importable/patchable
    def test_split_split_method(self, mock_split_recursive, mock_predict_scores):
        mock_predict_scores.return_value = [("element1", 0.8), ("element2", 0.7)]
        mock_split_recursive.return_value = ["split subtitle"]

        result = self.splitter.split("some text", length=21, method="SPLIT")  # length=21 -> min=14, max=28

        mock_predict_scores.assert_called_once_with("some text")
        mock_split_recursive.assert_called_once_with(
            [("element1", 0.8), ("element2", 0.7)],
            min_chars=14,
            max_chars=28
        )
        self.assertEqual(result, ["split subtitle"])

    def test_split_unknown_method(self):
        with patch.object(self.splitter.logger, 'error') as mock_log_error:
            result = self.splitter.split("some text", method="UNKNOWN")
            self.assertEqual(result, ["some text"])  # Returns original text
            mock_log_error.assert_called_with("Unknown splitting method: UNKNOWN. Returning original text.")

    def test_split_predict_scores_fails(self):
        with patch.object(self.splitter, '_predict_scores', side_effect=Exception("Predict error")):
            with patch.object(self.splitter.logger, 'error') as mock_log_error:
                result = self.splitter.split("some text")
                self.assertEqual(result, ["some text"])
                mock_log_error.assert_called_once()
                self.assertIn("Error predicting scores for text", mock_log_error.call_args[0][0])

    @patch('splitter_module.preprocess_inference')
    def test_predict_scores_empty_proprocesses(self, mock_preprocess_inference):
        mock_preprocess_inference.return_value = []
        result = self.splitter._predict_scores("text")
        self.assertEqual(result, [])

    @patch('splitter_module.preprocess_inference')
    def test_predict_scores_successful_inference(self, mock_preprocess_inference):
        # Mock tokenizer and session are already set up in self.splitter
        mock_inputs = {"input_ids": np.array([[101, 678, 12345, 679, 12345, 102]]),
                       "attention_mask": np.array([[1, 1, 1, 1, 1, 1]])}
        mock_elements = ["word1", "word2"]
        mock_sep_indices = [2, 4]  # Indices of SEP_TOKEN_ID
        mock_preprocess_inference.return_value = [(mock_inputs, mock_elements, mock_sep_indices)]

        # Mock ONNX session output
        # Logits for 6 tokens, scores for SEP tokens at index 2 and 4 will be extracted
        mock_logits = np.array([[-0.5, 0.5, 1.38, 0.0, 0.84, -0.2]])  # (batch_size, seq_len)
        self.splitter.session.run.return_value = [mock_logits]

        expected_scores = [1 / (1 + np.exp(-1.38)), 1 / (1 + np.exp(-0.84))]  # Sigmoid of logits at sep_indices

        result = self.splitter._predict_scores("text")

        self.splitter.session.run.assert_called_once_with(["logits"], mock_inputs)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "word1")
        self.assertAlmostEqual(result[0][1], expected_scores[0])
        self.assertEqual(result[1][0], "word2")
        self.assertAlmostEqual(result[1][1], expected_scores[1])

    @patch('splitter_module.preprocess_inference')
    def test_predict_scores_onnx_error(self, mock_preprocess_inference):
        mock_inputs = {"input_ids": np.array([[1, 2, 3]]), "attention_mask": np.array([[1, 1, 1]])}
        mock_preprocess_inference.return_value = [(mock_inputs, ["elem"], [1])]
        self.splitter.session.run.side_effect = Exception("ONNX Error")

        with patch.object(self.splitter.logger, 'error') as mock_log_error:
            result = self.splitter._predict_scores("text")
            self.assertEqual(result, [])  # Should return empty if all inferences fail
            mock_log_error.assert_called_with("Error during ONNX inference: ONNX Error")


class TestPreprocessInference(unittest.TestCase):

    def setUp(self):
        self.mock_tokenizer = MagicMock()
        self.mock_tokenizer.cls_token_id = 101
        self.mock_tokenizer.sep_token_id = 102  # This is the model's general SEP, not custom
        self.mock_tokenizer.pad_token_id = 0
        self.mock_tokenizer.encode.side_effect = lambda x, add_special_tokens: [len(c) for c in x]  # Dummy encode

        self.sep_token_id = 12345  # Custom SEP

    @patch('splitter_module.nltk.sent_tokenize')
    def test_preprocess_empty_text(self, mock_sent_tokenize):
        mock_sent_tokenize.return_value = []
        result = preprocess_inference("", self.mock_tokenizer, 512, self.sep_token_id, lambda x: [])
        self.assertEqual(result, [])

        result = preprocess_inference("   ", self.mock_tokenizer, 512, self.sep_token_id, lambda x: [])
        self.assertEqual(result, [])

    @patch('splitter_module.nltk.sent_tokenize')
    def test_preprocess_simple_sentence(self, mock_sent_tokenize):
        mock_sent_tokenize.return_value = ["Hello world."]
        mock_split_elements = MagicMock(return_value=["Hello", "world."])

        # Simplified tokenizer.encode mock for this test
        def simple_encode(text, add_special_tokens=False):
            if text == "Hello": return [11]
            if text == "world.": return [22, 23]
            return []

        self.mock_tokenizer.encode = simple_encode

        result = preprocess_inference("Hello world.", self.mock_tokenizer, 10, self.sep_token_id, mock_split_elements)

        self.assertEqual(len(result), 1)
        batch_info = result[0]
        inputs, elements, sep_indices = batch_info

        # Expected: [CLS, Hello_ids, SEP_CUSTOM, world._ids, SEP_CUSTOM, SEP_MODEL]
        # [101, 11, 12345, 22, 23, 12345, 102]
        expected_input_ids = [101, 11, 12345, 22, 23, 12345, 102]
        padding_needed = 10 - len(expected_input_ids)
        expected_input_ids += [0] * padding_needed

        np.testing.assert_array_equal(inputs["input_ids"], np.array([expected_input_ids], dtype=np.int64))
        self.assertEqual(elements, ["Hello", "world."])
        self.assertEqual(sep_indices, [2, 5, 6])  # Indices of *any* sep_token_id (custom and model's)

    @patch('splitter_module.nltk.sent_tokenize')
    def test_preprocess_long_sentence_chunking(self, mock_sent_tokenize):
        # Test that a long sentence is broken into chunks by preprocess_inference's first loop
        mock_sent_tokenize.return_value = ["one two three four five six."]
        # Each "word" + sep_token_id will be 2 tokens long by this mock
        self.mock_tokenizer.encode.side_effect = lambda x, add_special_tokens: [1]  # each element is 1 token

        # max_length for chunking is max_length - 2 (for CLS and final SEP of batch)
        # If max_length (for model) is 10, then chunk max_length is 8.
        # Each element + custom_sep = 1 + 1 = 2 tokens.
        # So, a chunk can hold 8 / 2 = 4 elements.
        # "one two three four" (4 elements, 8 tokens) -> chunk 1
        # "five six." (2 elements, 4 tokens) -> chunk 2

        mock_split_elements = MagicMock(return_value=["one", "two", "three", "four", "five", "six."])

        # This test primarily checks the sentences_elements creation part
        # The actual batching part is more complex to assert fully without replicating logic
        # We'll focus on the number of batches if possible, or the intermediate sentences_elements

        # To properly test sentences_elements we'd need to extract it or modify preprocess_inference
        # For now, let's check the final output structure based on this.
        # With max_length = 10 for the final batch:
        # Batch 1: [CLS, one,S,two,S,three,S,four,S, SEP_MODEL, PAD] (1+2+2+2+2+1 = 10)
        # Batch 2: [CLS, five,S,six.,S, SEP_MODEL, PAD,PAD,PAD,PAD] (1+2+2+1 = 6 tokens + 4 pads)

        result = preprocess_inference("long sentence", self.mock_tokenizer, 10, self.sep_token_id, mock_split_elements)
        self.assertEqual(len(result), 2)  # Expect two batches due to chunking and then batching

        # Batch 1
        inputs1, elements1, sep_indices1 = result[0]
        self.assertEqual(elements1, ["one", "two", "three", "four"])
        # [CLS, 1,S, 1,S, 1,S, 1,S, SEP_MODEL] -> [101, 1,12345, 1,12345, 1,12345, 1,12345, 102]
        np.testing.assert_array_equal(inputs1["input_ids"],
                                      np.array([[101, 1, 12345, 1, 12345, 1, 12345, 1, 12345, 102]], dtype=np.int64))

        # Batch 2
        inputs2, elements2, sep_indices2 = result[1]
        self.assertEqual(elements2, ["five", "six."])
        # [CLS, 1,S, 1,S, SEP_MODEL, PAD, PAD, PAD, PAD] -> [101, 1,12345,1,12345, 102, 0,0,0,0]
        np.testing.assert_array_equal(inputs2["input_ids"],
                                      np.array([[101, 1, 12345, 1, 12345, 102, 0, 0, 0, 0]], dtype=np.int64))


class TestFindZeroScoreSeries(unittest.TestCase):

    def test_find_zero_score_series_empty(self):
        self.assertEqual(find_zero_score_series([]), [])

    def test_find_zero_score_series_no_zeros(self):
        elements = [("a", 0.3), ("b", 0.5), ("c", 0.8)]
        self.assertEqual(find_zero_score_series(elements, zero_threshold=0.2), [])

    def test_find_zero_score_series_all_zeros(self):
        elements = [("a", 0.1), ("b", 0.05), ("c", 0.15)]  # lengths 1, 1, 1
        # Chars: len("a") + len("b") + 1 (space) + len("c") + 1 (space) = 1+1+1+1+1 = 5
        expected = [(0, 2, 5)]
        self.assertEqual(find_zero_score_series(elements, zero_threshold=0.2), expected)

    def test_find_zero_score_series_mixed(self):
        elements = [
            ("word1", 0.1), ("word2", 0.05),  # Zero series 1 (idx 0-1) chars: 5+1+5=11
            ("word3", 0.9),  # Not zero
            ("word4", 0.15), ("word5", 0.1),  # Zero series 2 (idx 3-4) chars: 5+1+5=11
            ("word6", 0.7),  # Not zero
            ("word7", 0.01)  # Zero series 3 (idx 6-6) chars: 5
        ]
        expected = [(0, 1, 11), (3, 4, 11), (6, 6, 5)]
        self.assertEqual(find_zero_score_series(elements, zero_threshold=0.2), expected)

    def test_find_zero_score_series_ends_with_zero(self):
        elements = [("word1", 0.5), ("word2", 0.1), ("word3", 0.05)]  # Zero series (idx 1-2) chars: 5+1+5=11
        expected = [(1, 2, 11)]
        self.assertEqual(find_zero_score_series(elements, zero_threshold=0.2), expected)


if __name__ == '__main__':
    # You might need to add the parent directory to sys.path if running this file directly
    # and 'splitter_module' is not in the Python path.
    # import sys
    # import os
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    unittest.main(verbosity=2)
