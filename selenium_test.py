from unittest import TestCase
from unit_test import add_test_data_to_db

from selenium.webdriver.common.by import By
from selenium import webdriver
import multiprocessing
import time

from app import create_app, db
from app.config import SeleniumTestConfig



localHost = "http://localhost:5000"

def run_test_server():
    testApp = create_app(SeleniumTestConfig)
    testApp.run(use_reloader=False)

class seleniumTests(TestCase):
    def setUp(self):
        self.testApp = create_app(SeleniumTestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()

        db.create_all()
        add_test_data_to_db()

        self.server_thread = multiprocessing.Process(target=run_test_server)
        self.server_thread.start()

        #disable password saving prompts
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(localHost)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class TestIndex(seleniumTests):
#-----------index.html -----------------
    def test_index_add_delete_task(self):
        self.driver.get(localHost + "/login")

        self.driver.find_element(By.ID, "email").send_keys("A123@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password1")
        self.driver.find_element(By.ID, "login-submit-btn").click()

        time.sleep(2)  # Wait for the page to load

        task_text = "Selenium Task"
        
        # Add Task----------------------------
        task_input = self.driver.find_element(By.ID, "task-input")
        task_input.clear()
        task_input.send_keys(task_text)
        
        time.sleep(2)  # Wait for the page to update

        add_button = self.driver.find_element(By.ID, "add-task-btn")
        self.driver.execute_script("arguments[0].click();", add_button) 

        time.sleep(2)  # Wait for the page to update

        self.assertIn(task_text, self.driver.page_source)

        # Toggle Status----------------------------
        task_span = self.driver.find_element(By.XPATH, f"//span[text()='{task_text}']")
        task_item = task_span.find_element(By.XPATH, "./ancestor::li")

        status_box = task_item.find_element(By.CLASS_NAME, "statusbox")
        self.driver.execute_script("arguments[0].click();", status_box)

        time.sleep(2)  # Wait for the page to update

        task_span = self.driver.find_element(By.XPATH, f"//span[text()='{task_text}']")
        task_item = task_span.find_element(By.XPATH, "./ancestor::li")

        self.assertIn("completed", task_item.get_attribute("class"))

        # Delete Task----------------------------
        delete_button = self.driver.find_element(By.ID, "delete-task-btn")
        self.driver.execute_script("arguments[0].click();", delete_button)

        time.sleep(2)  
        
        # Find the task span by path
        task_span = self.driver.find_element(By.XPATH, f"//span[text()='{task_text}']")
        task_item = task_span.find_element(By.XPATH, "./ancestor::li")

        delete_button = task_item.find_element(By.CLASS_NAME, "delete-btn")
        self.driver.execute_script("arguments[0].click();", delete_button)

        time.sleep(2)  # Wait for the page to update

        self.assertNotIn(task_text, self.driver.page_source)

    def test_index_timer(self):
        self.driver.get(localHost + "/login")

        self.driver.find_element(By.ID, "email").send_keys("A123@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password1")
        self.driver.find_element(By.ID, "login-submit-btn").click()

        time.sleep(2)  # Wait for the page to load

        self.driver.find_element(By.ID, "lbreak_length").click()
        time.sleep(1)  # Wait for the page to update

        self.assertEqual(
            self.driver.find_element(By.ID, "simple-timer").text,
            "15:00"
        )

        self.driver.find_element(By.ID, "sbreak_length").click()
        time.sleep(1)  # Wait for the page to update

        self.assertEqual(
            self.driver.find_element(By.ID, "simple-timer").text,
            "05:00"
        )

        self.driver.find_element(By.ID, "start-btn").click()
        time.sleep(2)  # Wait for the timer to start

        self.assertEqual(
            self.driver.find_element(By.ID, "start-btn").text,
            "Pause"
        )

        self.driver.find_element(By.ID, "start-btn").click()
        time.sleep(2)  # Wait for the timer to pause

        self.assertEqual(
            self.driver.find_element(By.ID, "start-btn").text,
            "Resume"
        )

        self.driver.find_element(By.ID, "reset-btn").click()
        time.sleep(2)  # Wait for the timer to reset  

        self.assertEqual(
            self.driver.find_element(By.ID, "start-btn").text,
            "Start"
        )

    def test_toggle_mode_choose_tasks(self):
        self.driver.get(localHost + "/login")

        self.driver.find_element(By.ID, "email").send_keys("A123@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password1")
        self.driver.find_element(By.ID, "login-submit-btn").click()

        time.sleep(2)  # Wait for the page to load

        # Add Task----------------------------
        task_text = "Selenium Task2"

        task_input = self.driver.find_element(By.ID, "task-input")
        task_input.clear()
        task_input.send_keys(task_text)
        
        add_button = self.driver.find_element(By.ID, "add-task-btn")
        self.driver.execute_script("arguments[0].click();", add_button) 

        time.sleep(2)  # Wait for the page to update

        self.assertIn(task_text, self.driver.page_source)
        task_span = self.driver.find_element(By.XPATH, f"//span[text()='{task_text}']")
        task_item = task_span.find_element(By.XPATH, "./ancestor::li")
        self.driver.execute_script("arguments[0].click();", task_item)

        time.sleep(2)  # Wait for the page to update

        # Check if the task item has the "selected" class
        self.assertIn("selected", task_item.get_attribute("class"))

        # Check if the task item is in the selected tasks list
        self.assertIn(
            "active",
            self.driver.find_element(By.ID, "mode-flow").get_attribute("class")
        )

        self.assertEqual(
            self.driver.find_element(By.ID, "flow-task-name").text,
            f"Task: {task_text}"
        )

        self.assertIsNone(
            self.driver.find_element(By.ID, "flow-start-btn").get_attribute("disabled")
        )

#---------Settings Change, Affects Timer Logic--------------------
def test_settings_change_affects_timer(self):
        self.driver.get(localHost + "/login")

        self.driver.find_element(By.ID, "email").send_keys("A123@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password1")
        self.driver.find_element(By.ID, "login-submit-btn").click()

        time.sleep(2)  # Wait for the page to load

        self.driver.find_element(By.ID, "settings-btn").click()
        time.sleep(2)  # Wait for the page to update

        self.driver.find_element(By.ID, "flow-rest-ratio").send_keys("2")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(2)  # Wait for the page to update
        self.driver.find_element(By.ID, "menusidebar").click()
        self.driver.find_element(By.ID, "urlfortimers").click()
        self.assertEqual(
            self.driver.find_element(By.ID, "flow-rest-ratio").text,
            "2"
        )
        self.driver.find_element(By.ID, "settings-btn").click()
        time.sleep(2)  # Wait for the page to update
        self.driver_find_element(By.ID, "pom_worklength").send_keys("30")
        self.driver_find_element(By.ID, "pom_short_break").send_keys("10")
        self.driver_find_element(By.ID, "pom_long_break").send_keys("20")
        self.driver_find_element(By.ID, "submit").click()
        time.sleep(2)  # Wait for the page to update
        self.driver.find_element(By.ID, "menusidebar").click()
        self.driver.find_element(By.ID, "urlfortimers").click()
        time.sleep(2)  # Wait for the page to update
        self.assertEqual(
            self.driver.find_element(By.ID, "pom-worklength").text,
            "30"
        )
        self.assertEqual(
            self.driver.find_element(By.ID, "pom-short-break").text,
            "10"
        )
        self.assertEqual(
            self.driver.find_element(By.ID, "pom-long-break").text,
            "20"
        )

#-----------Timer session start and end updates dashboard graph--------------------
def test_timer_session_start_and_end_updates_chart_data(self):
    self.driver.get(localHost + "/login")

    self.driver.find_element(By.ID, "email").send_keys("E123@example.com")
    self.driver.find_element(By.ID, "password").send_keys("password5")
    self.driver.find_element(By.ID, "login-submit-btn").click()

    time.sleep(2)  # Wait for the page to load

    self.driver.find_element(By.ID, "menusidebar").click()
    self.driver.find_element(By.ID, "urlfortimers").click()
    time.sleep(2)  # Wait for the page to update
    task_input = self.driver.find_element(By.ID, "task-input")
    task_input.clear()
    task_input.send_keys("CITS3403 project")
    time.sleep(1)  # Wait for the page to update
    self.driver.find_element(By.ID, "add-task-btn").click()
    time.sleep(2)  # Wait for the page to update
    self.driver.find_element(By.ID, "flow-start-btn").click()
    time.sleep(2)  # Wait for the page to update
    self.driver.find_element(By.ID, "flow-end-btn").click()
    time.sleep(2)  # Wait for the page to update
    self.driver.find_element(By.ID, "urlfordashboard").click()
    time.sleep(2)  # Wait for the page to update
    # Build a {task_name: hours} dictionary from the chart
    task_hours = self.driver.execute_script("""
        const chart = Chart.getChart("analyticsChart");
        const labels = chart.data.labels;
        const values = chart.data.datasets[0].data;

        const result = {};
        for (let i = 0; i < labels.length; i++) {
            result[labels[i]] = values[i];
        }
        return result;
    """)

    self.assertIn("CITS3403 project", task_hours.keys())
    self.assertGreater(task_hours["CITS3403 project"], 0)

def test_pomodoro_session_start_and_end_updates_chart_data(self):
    self.driver.get(localHost + "/login")

    self.driver.find_element(By.ID, "email").send_keys("E123@example.com")
    self.driver.find_element(By.ID, "password").send_keys("password5")
    self.driver.find_element(By.ID, "login-submit-btn").click()

    time.sleep(2)  # Wait for the page to load

    self.driver.find_element(By.ID, "menusidebar").click()
    self.driver.find_element(By.ID, "urlfortimers").click()
    time.sleep(2)  # Wait for the page to update
    task_input = self.driver.find_element(By.ID, "task-input")
    task_input.clear()
    task_input.send_keys("CITS3403 project")
    time.sleep(1)  # Wait for the page to update
    self.driver.find_element(By.ID, "add-task-btn").click()
    time.sleep(2)  # Wait for the page to update
    self.driver.find_element(By.ID, "start-btn").click()
    time.sleep(2)  # Wait for the page to update
    self.driver.find_element(By.ID, "start-btn").click()
    time.sleep(2)  # Wait for the page to update
    self.driver.find_element(By.ID, "urlfordashboard").click()
    time.sleep(2)  # Wait for the page to update
    # Build a {task_name: hours} dictionary from the chart
    task_hours = self.driver.execute_script("""
        const chart = Chart.getChart("analyticsChart");
        const labels = chart.data.labels;
        const values = chart.data.datasets[0].data;

        const result = {};
        for (let i = 0; i < labels.length; i++) {
            result[labels[i]] = values[i];
        }
        return result;
    """)

    self.assertIn("CITS3403 project", task_hours.keys())
    self.assertGreater(task_hours["CITS3403 project"], 0)
