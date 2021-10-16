from selenium import webdriver
from selenium.webdriver.support.ui import Select


class GymReservation:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def init_driver(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')

    def next_date(self):
        change_url = self.driver.get(
            "http://applications.ucy.ac.cy/pub_sportscenter/online_reservations_pck2.insert_reservation?p_lang=")
        terms_accepted = self.driver.find_element_by_name(
            'terms_accepted')
        terms_accepted.click()
        select_gym = Select(self.driver.find_element_by_name('p_sport'))
        select_gym.select_by_visible_text("Γυμναστήριο")
        sumbit_new_reserv = self.driver.find_element_by_css_selector(
            "div > button")
        sumbit_new_reserv.submit()
        select_weights = Select(
            self.driver.find_element_by_name("p_class_code"))
        select_weights.select_by_visible_text("ΑΙΘΟΥΣΑ ΒΑΡΩΝ (ΕΠΙΠΕΔΟ -1)")

        present = self.driver.find_element_by_css_selector(
            "form > h5 > input[type=submit]:nth-child(18)")
        present.submit()

    def next_month(self):
        next_m = self.driver.find_element_by_css_selector(
            'table:nth-child(4) > tbody > tr > td:nth-child(19) > div > button')
        next_m.click()

    def login(self):
        agree_terms_checkbox = self.driver.find_element_by_id("tpe")
        agree_terms_checkbox.click()

        with_grad_password_button = self.driver.find_element_by_xpath(
            '//*[@id="doing"]/div/article/button[2]')
        with_grad_password_button.click()

        username = self.driver.find_element_by_xpath(
            '//*[@id="contentRow"]/div[2]/div/article/form/div[1]/div/input')
        username.click()
        username.send_keys(self.username)

        password = self.driver.find_element_by_xpath(
            '//*[@id="contentRow"]/div[2]/div/article/form/div[2]/div/input')
        password.send_keys(self.password)

        login_submit = self.driver.find_element_by_xpath(
            '//*[@id="contentRow"]/div[2]/div/article/form/div[3]/button')
        login_submit.submit()

    def choose_sport(self):
        terms_accepted = self.driver.find_element_by_name('terms_accepted')
        terms_accepted.click()

        select_gym = Select(self.driver.find_element_by_name('p_sport'))
        select_gym.select_by_visible_text("Γυμναστήριο")

        sumbit_new_reserv = self.driver.find_element_by_css_selector(
            "div > button")
        sumbit_new_reserv.submit()

        select_weights = Select(
            self.driver.find_element_by_name("p_class_code"))
        select_weights.select_by_visible_text("ΑΙΘΟΥΣΑ ΒΑΡΩΝ (ΕΠΙΠΕΔΟ -1)")

        present = self.driver.find_element_by_css_selector(
            "form > h5 > input[type=submit]:nth-child(18)")
        present.submit()

    def prepare_for_reservation(self):
        self.init_driver()
        self.driver.get("http://applications.ucy.ac.cy/pub_sportscenter/main")

        self.login()

        change_url = self.driver.get(
            "http://applications.ucy.ac.cy/pub_sportscenter/online_reservations_pck2.insert_reservation?p_lang=")

        self.choose_sport()

    def close_driver(self):
        self.driver.quit()

    def make_reservation(self, gym_dates):

        mytable = self.driver.find_element_by_css_selector(
            '#contentRow > center > table.table.table-bordered ')

        temp = mytable.find_elements_by_tag_name('tr')
        rows_n = len(temp)
        cells_temp = temp[-2].find_elements_by_css_selector('td')
        cells_n = len(cells_temp)

        for i in range(1, rows_n+1):
            for j in range(1, cells_n+1):
                try:
                    day_btn = self.driver.find_element_by_css_selector(
                        'tr:nth-child('+str(i)+') > td:nth-child('+str(j)+') > form > div > button')
                    day_btn.click()

                    if j == 2:
                        select_time = Select(self.driver.find_element_by_name(
                            "p_sttime")).select_by_visible_text(gym_dates['Monday'])
                        print("\n**Monday**")
                    elif j == 3:
                        select_time = Select(self.driver.find_element_by_name(
                            "p_sttime")).select_by_visible_text(gym_dates['Tuesday'])
                        print("\n**Tuesday**")
                    elif j == 4:
                        select_time = Select(self.driver.find_element_by_name(
                            "p_sttime")).select_by_visible_text(gym_dates['Wednesday'])
                        print("\n**Wednesday**")
                    elif j == 5:
                        select_time = Select(self.driver.find_element_by_name(
                            "p_sttime")).select_by_visible_text(gym_dates['Thursday'])
                        print("\n**Thursday**")
                    elif j == 6:
                        select_time = Select(self.driver.find_element_by_name(
                            "p_sttime")).select_by_visible_text(gym_dates['Friday'])
                        print("\n**Friday**")
                    elif j == 7:
                        select_time = Select(self.driver.find_element_by_name(
                            "p_sttime")).select_by_visible_text(gym_dates['Saturday'])
                        print("\n**Saturday**")

                    reservation_purpose = self.driver.find_element_by_name(
                        'p_skopos')
                    reservation_purpose.send_keys("q")

                    submit_details = self.driver.find_element_by_css_selector(
                        'td > div > button')
                    submit_details.submit()

                    final_submit = self.driver.find_element_by_css_selector(
                        'td > div.form-group > button')
                    final_submit.submit()



                    try:
                        p_date = self.driver.find_element_by_name(
                        "p_reservation_date")
                        print(p_date.text)
                        reasons = self.driver.find_elements_by_css_selector('li')
                        for k in reasons:
                            print(k.text)
                    except:
                        successfull_reservation = self.driver.find_elements_by_css_selector('#contentRow > p')
                        print(successfull_reservation[0].text)
                    self.next_date()
                    
                except Exception as e: 
                    # print(e)
                    pass


if __name__ == "__main__":

    # CHOOSE YOUR TIMES
    reservation_dates = {'Monday': '18:00',     'Tuesday': '18:00',     'Wednesday': '18:00',
                         'Thursday': '18:00',      'Friday': '16:00',    'Saturday': '08:30'}
    gym = GymReservation("ADD YOUR EMAIL", "ADD YOUR PASSWORD")
    gym.prepare_for_reservation()
    gym.make_reservation(reservation_dates)
    gym.next_month()
    gym.make_reservation(reservation_dates)
    print('**FINISHED**')
    gym.close_driver()
