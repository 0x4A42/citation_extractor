import unittest
from citation_mining.citation_json_manager import CitationJsonManager


class TestCitationJsonManager(unittest.TestCase):
    manager = CitationJsonManager()
    path_to_json = "../test_documents/test_json.json"
    expected_dict_keys = ['Academic', 'Non-Academic', 'Unassigned']
    loaded_json_list = manager.load_from_file_to_array(path_to_json)
    loaded_json_dict = manager.load_from_file_to_dict(path_to_json)
    academic_title = "2. A. Hottinen O. Tirkkonen R. Wichman Multi-antenna Transceiver Techniques for 3G and Beyond New York:John Wiley and Sons 2003."
    non_academic_title = "Cooperative diversity in wireless networks: Efficient protocols and outage behavior"

    def test_load_from_file_to_array_length(self):
        """Asserts that the correct number of citations have been loaded
        """
        self.assertEqual(len(self.loaded_json_list), 620042)

    def test_load_from_file_to_array_order(self):
        """Asserts that the loading is done in a consistent order
        """
        self.assertEqual(
            self.loaded_json_list[0].get_title(), self.academic_title)

    def test_load_from_file_to_dict_key_length(self):
        """Asserts the correct number of keys have been loaded in the
        dictionary
        """
        self.assertEqual(len(self.loaded_json_dict), 3)

    def test_load_from_file_to_dict_key_names(self):
        """Asserts that the two keys are as expected
        """
        self.assertEqual(list(self.loaded_json_dict), self.expected_dict_keys)

    def testLoadFromFileToDictKeyItemOrderingAcademic(self):
        """Asserts that the items under the first key are in a conistent
        order
        """
        list_of_academic = self.loaded_json_dict[self.expected_dict_keys[0]]
        self.assertEqual(list_of_academic[0].get_title(), self.academic_title)

    def testLoadFromFileToDictKeyItemOrderingNonacademic(self):
        """Asserts that the items under the first key are in a consistent
        order
        """
        list_of_academic = self.loaded_json_dict[self.expected_dict_keys[1]]
        self.assertEqual(
            list_of_academic[0].get_title(), self.non_academic_title)


if __name__ == '__main__':
    unittest.main()
