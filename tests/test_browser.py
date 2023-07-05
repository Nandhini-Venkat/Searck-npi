import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("driver")
class TestSearch:
    npi_number_id = "npiNumber"
    npi_type_id = (By.ID, "enumerationType")  # select drop down
    taxonomy_description_id = (By.ID, "taxonomyDescription")
    provider_first_name_id = (By.ID, "firstName")
    provider_last_name_id = (By.ID, "lastName")
    organization_name_id = (By.ID, "organizationName")
    auth_first_name_id = (By.ID, "aoFirstName")
    auth_last_name_id = (By.ID, "aoLastName")
    city_id = (By.ID, "city")
    state_id = (By.ID, "state")  # select
    country_id = (By.ID, "country")  # select
    postal_code_id = (By.ID, "postalCode")
    address_type_id = (By.ID, "addressType")  # select
    clear_button_name = (By.NAME, "clear")
    search_button_xpath = "//button[text()='Search']"
    search_page_title_xpath = "//td[text()='1801186879']"
    list_of_npi_records_using_fandl_name = "//table//tbody/tr"
    exact_match_id = "exactMatch"

    def wait(self):
        wait = WebDriverWait(self.driver, 10)
        return wait

    def submit_search(self):
        self.driver.find_element(By.XPATH, self.search_button_xpath).submit()

    def select_from_drop_down(self, text):
        select = Select(self.driver.find_element(By.ID, self.npi_type_id))
        select.select_by_visible_text(text)

    @pytest.mark.parametrize("npi_number", ["1801186879"])
    def test_search_using_npi_number(self, npi_number):
        self.driver.find_element(By.ID, self.npi_number_id).send_keys(npi_number)
        self.submit_search()
        nip_element = self.driver.find_element(By.XPATH, self.search_page_title_xpath).text
        assert nip_element == npi_number

    @pytest.mark.parametrize(("first_name", "last_name"), [("CATHERINE", "HAAS")])
    def test_search_using_provider_first_and_last_name(self, first_name, last_name):
        self.driver.find_element(By.ID, self.provider_first_name_id).sendkeys(first_name)
        self.driver.find_element(By.ID, self.provider_last_name_id).sendkeys(last_name)
        self.submit_search()
        list_of_element = self.driver.fid_elements(By.XPATH, self.list_of_npi_records_using_fandl_name).text
        for first in list_of_element:
            if first == "first_name":
                assert first == first_name
                break

    @pytest.mark.parametrize(("first_name", "last_name"), [("CATHERINE", "HAAS")])
    def test_exact_search_using_provider_names(self, first_name, last_name):
        self.driver.find_element(By.ID, self.provider_first_name_id).sendkeys(first_name)
        self.driver.find_element(By.ID, self.provider_last_name_id).sendkeys(last_name)
        self.driver.find_element(By.ID, self.exact_match_id).click()
        self.submit_search()
        list_of_element = self.driver.fid_elements(By.XPATH, self.list_of_npi_records_using_fandl_name).text
        count = 0
        for first in list_of_element:
            if first in list_of_element:
                count = count + 1
        print(count)

    @pytest.mark.parametrize("taxonomy", ["Registered Nurse"])
    def test_search_using_taxonomy(self, primary_taxonomy):
        self.driver.find_element(By.ID, self.taxonomy_description_id).sendkeys(primary_taxonomy)
        self.submit_search()
        list_of_element = self.driver.fid_elements(By.XPATH, self.list_of_npi_records_using_fandl_name).text
        for taxonomy in list_of_element:
            if taxonomy == primary_taxonomy:
                assert taxonomy == primary_taxonomy
                break

    @pytest.mark.parametrize("taxonomy", ["Registered Nurse"])
    def test_exact_search_using_taxonomy(self, primary_taxonomy):
        self.driver.find_element(By.ID, self.taxonomy_description_id).sendkeys(primary_taxonomy)
        self.driver.find_element(By.ID, self.exact_match_id).click()
        self.submit_search()
        list_of_element = self.driver.fid_elements(By.XPATH, self.list_of_npi_records_using_fandl_name).text
        count = 0
        for taxonomy in list_of_element:
            if taxonomy in list_of_element:
                count = count + 1
        print(count)

    @pytest.mark.parametrize("npi_type","taxonomy",(["Any","Individual","Organization"],["Registered Nurse"]))
    def test_search_using_npi_type_and_taxonomy(self,npi_type, taxonomy):
        self.driver.find_element(By.ID, self.taxonomy_description_id).sendkeys(taxonomy)
        self.select_from_drop_down(npi_type)
        self.submit_search()
        list_of_element = self.driver.fid_elements(By.XPATH, self.list_of_npi_records_using_fandl_name).text
        count = 0
        for tax in list_of_element:
            if tax == taxonomy:
                count = count + 1
        print(count)
