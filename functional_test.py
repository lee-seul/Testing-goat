# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3) # 암묵적 대기, 페이지 로딩때문


    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To DO', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholde'),
                '작업 아이템 입력'
        
        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: 공작깃털 사기' for row in rows),
            )
        
        self.fail('Finish the test!')


if __name__ == "__main__":
    unittest.main()

