import unittest
from string_repetition import StringRepetitionDetector

class TestStringRepetitionDetector(unittest.TestCase):
    def setUp(self):
        self.detector = StringRepetitionDetector(
            min_length=3,  # 使用较小的值便于测试
            min_repeats=2
        )

    def test_simple_repetition(self):
        text = "abcabcabc"
        result = self.detector.detect(text)
        self.assertTrue(result.has_repetition)
        self.assertEqual(result.substring, "abc")
        self.assertEqual(result.repetition_count, 3)
        self.assertEqual(result.sequence_length, 3)

    def test_no_repetition(self):
        text = "abcdef"
        result = self.detector.detect(text)
        self.assertFalse(result.has_repetition)

    def test_overlapping_repetition(self):
        text = "aaaaa"
        result = self.detector.detect(text)
        self.assertTrue(result.has_repetition)
        self.assertEqual(result.substring, "aaa")

    def test_batch_detection(self):
        texts = ["abcabc", "def", "xyzxyzxyz"]
        results = [self.detector.detect(text) for text in texts]
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].has_repetition)
        self.assertFalse(results[1].has_repetition)
        self.assertTrue(results[2].has_repetition)

    def test_empty_string(self):
        text = ""
        result = self.detector.detect(text)
        self.assertFalse(result.has_repetition)

    def test_long_string_parallel(self):
        # 创建一个较长的重复字符串
        text = "abc" * 1000000
        result = self.detector.detect(text)
        self.assertTrue(result.has_repetition)
        self.assertEqual(result.substring, "abc")
    
    def test_prefix(self):
        # 前缀加上
        text= "qwertyuiopabcabcabcabc"
        result = self.detector.detect(text)
        self.assertTrue(result.has_repetition)
        self.assertEqual(result.substring, "abc")
        self.assertEqual(result.repetition_count, 4)
        self.assertEqual(result.sequence_length, 3)
        self.assertEqual(result.start_pos, 10)

if __name__ == '__main__':
    unittest.main()