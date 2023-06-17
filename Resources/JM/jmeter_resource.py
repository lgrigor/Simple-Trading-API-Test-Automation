import os
import subprocess
import threading
import time
import xml.etree.ElementTree as ET

from Data.main import Main


class JmeterResource(Main):

    def run_jmeter_in_thread(self, arguments: tuple) -> None:
        t1 = threading.Thread(target=self.run_jmeter, args=arguments)
        t1.start()

    def run_jmeter(self, jmx_file: str, jmeter_log: str, output_xml: str) -> None:
        root = os.getenv("root")

        jmx = rf"{root}\Resources\JM\{jmx_file}"

        try:
            print('\nINFO: Jmeter run Started')
            subprocess.run([self.JMETER, "-j", jmeter_log, "-n", "-t", jmx, "-l", output_xml,
                            "-Jjmeter.save.saveservice.output_format=xml",
                            "-Jjmeter.save.saveservice.response_data=true"
                            ])
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def wait_until_files_are_created(files: tuple, timeout=10) -> None:
        for each_file in files:
            for i in range(timeout):
                time.sleep(timeout/10)
                if os.path.exists(each_file):
                    break
            else:
                raise Exception("Output files wasn't created!")

    @staticmethod
    def check_response_content(xml: str, expected_response_structure: dict, expected_status_code: int) -> bool:
        tree = ET.parse(xml)
        root = tree.getroot()
        http_samples = root.findall('.//httpSample')

        for http_sample in http_samples:
            response_data = http_sample.find('responseData').text
            response_status_code = int(http_sample.get("rc"))
            response_body = eval(response_data)
            response_body: dict

            if response_status_code != expected_status_code:
                return False

            if response_body.keys() != expected_response_structure.keys():
                return False
            else:
                for __key in response_body:
                    if expected_response_structure[__key] == "random":
                        continue
                    elif expected_response_structure[__key] != response_body[__key]:
                        print(f"Expected value of the key '{__key}' is '{expected_response_structure[__key]}'")
                        print(f"Got '{response_body[__key]}' instead!")
                        return False

                return True

    @staticmethod
    def calculate_average_execution_delay(execution_times: dict) -> int:
        """Calculate the average order execution delay:
            1. Sum up all the order execution delay values
            2. Divide the sum by the total number of data points"""

        return round(sum(execution_times.values()) / len(execution_times.values()), 3)

    @staticmethod
    def calculate_standard_deviation(execution_times: dict, average: int) -> float:
        """Calculate the standard deviation of the order execution delays:
            1. Calculate the difference between each data point and the average order execution delay
            2. Square each difference
            3. Sum up all the squared differences
            4. Divide the sum by the total number of data points
            5. Take the square root of the result"""

        difference = set()
        for each_exec_time in execution_times.values():
            difference.add((each_exec_time - average) ** 2)

        return round((sum(difference) / len(difference)) ** 0.5, 3)
