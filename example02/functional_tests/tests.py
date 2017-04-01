# coding: utf-8

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from contextlib import contextmanager


class NewVisitorTest(LiveServerTestCase):

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield WebDriverWait(self.browser, timeout).until(
                staleness_of(old_page)
                )

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                '작업 아이템 입력'
                )

        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)
        
#        edith_list_url = self.browser.current_url
#        self.assertRegex(edith_list_url, '/lists/.+')

        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: 공작깃털 사기')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table(
                '2: 공작깃털을 이용해서 그물 만들기')
            self.check_for_row_in_list_table('1: 공작깃털 사기')

        ## 새로운 사용자인 프란시스가 사이트에 접속한다.

        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가
        ## 쿠키를 통해 유입되는 것을 방지한다. 

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)


        """
        새로운 창을 띄웟을 때 이전에 입력한 값이 없어야 하지만 
        계속해서 값이 존재함.. 

        URL 매칭도 이상 
        """
#        francis_list_url = self.browser.current_url
#        self.assertRegex(francis_list_url, '/lists/.+')
#        self.assertNotEqual(francis_list_url, edith_list_url)

        with self.wait_for_page_load(timeout=10):
            page_text = self.browser.find_element_by_tag_name('body').text
#            self.assertNotIn('공작깃털 사기', page_text)
            self.assertIn('우유 사기', page_text)


        self.fail('Finish the test!')



