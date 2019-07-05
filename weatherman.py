import sys

from datetime import datetime


def pr_red(skk): print("\033[91m {}\033[00m".format(skk), end='')


def pr_cyan(skk): print("\033[96m {}\033[00m".format(skk), end='')


def mk_int(s):
    s = s.strip()
    return int(s) if s else None


def mk_double(s):
    s = s.strip()
    return float(s) if s else None


class WeatherReading:
    def __init__(self, record):
        # print(record)
        if record != '':
            self.pkt, self.maxTempC, self.meanTempC, self.minTempC, self.dewPointC, self.meanDewPointC,\
                self.minDewPointC, self.maxHumidity, self.meanHumidity, self.minHumidity, self.maxSeaLevelPressure,\
                self.meanSeaLevelPressure, self.minSeaLevelPressure, self.maxVisibility, self.meanVisibility,\
                self.minVisibility, self.maxWindSpeed, self.meanWindSpeed, self.maxGustSpeed, self.precipitation,\
                self.cloudClover, self.event, self.windDirDegrees = record.split(',')

            self.pkt = datetime.strptime(self.pkt, '%Y-%m-%d')
            self.maxTempC = mk_int(self.maxTempC)
            self.minTempC = mk_int(self.minTempC)
            self.meanTempC = mk_int(self.meanTempC)
            self.meanHumidity = mk_int(self.meanHumidity)
            self.maxHumidity = mk_int(self.maxHumidity)
            self.minHumidity = mk_int(self.minHumidity)
            self.dewPointC = mk_int(self.dewPointC)
            self.meanDewPointC = mk_int(self.meanDewPointC)
            self.minDewPointC = mk_int(self.minDewPointC)
            self.minSeaLevelPressure = mk_double(self.minSeaLevelPressure)
            self.meanSeaLevelPressure = mk_double(self.meanSeaLevelPressure)
            self.maxSeaLevelPressure = mk_double(self.maxSeaLevelPressure)
            self.maxVisibility = mk_double(self.maxVisibility)
            self.minVisibility = mk_double(self.minVisibility)
            self.meanVisibility = mk_double(self.meanVisibility)
            self.maxWindSpeed = mk_double(self.maxWindSpeed)
            self.meanWindSpeed = mk_double(self.meanWindSpeed)
            self.maxGustSpeed = mk_double(self.maxGustSpeed)
            self.precipitation = mk_double(self.precipitation)
            self.cloudClover = mk_double(self.cloudClover)


months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# filePath = "/home/alii/PycharmProjects/WeatherMan/weatherfiles/Murree_weather_{0}_{1}.txt"
filePath = "{0}/Murree_weather_{1}_{2}.txt"
# days_in_a_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class AnnualReport:
    def __init__(self):
        self.maxTemp = None
        self.maxDate = None
        self.minTemp = None
        self.minDate = None
        self.mostHumid = None
        self.humidDate = None
        self.report = "Highest: {0}C on {1} {2}\n" \
                      "Lowest: {3}C on {4} {5}\n" \
                      "Humidity: {6}% on {7} {8}"

    def display(self):
        self.report = self.report.format(self.maxTemp, months[self.maxDate.month], self.maxDate.day,
                                         self.minTemp, months[self.minDate.month], self.minDate.day,
                                         self.mostHumid, months[self.humidDate.month], self.humidDate.day)
        print(self.report)


class MonthlyReport:
    def __init__(self):
        self.report = "Highest Average: {0}C\nLowest Average: {1}C\nAverage Mean Humidity: {2}%"
        self.maxMeanTemp = None
        self.minMeanTemp = None
        self.meanHumid = None

    def display(self):
        self.report = self.report.format(self.maxMeanTemp, self.minMeanTemp, round(self.meanHumid))
        print(self.report)


class CalculateResults:
    @staticmethod
    def calculate_annual_report(directory, year):
        print("\n\n\n~~~TASK 1~~~")
        flag = False
        annual_report = AnnualReport()
        for month in months:
            try:
                file = open(filePath.format(directory, year, month))
            except FileNotFoundError:
                continue
            file.readline()
            weather_reading = WeatherReading(file.readline())
            if flag is False:
                annual_report.maxTemp = weather_reading.maxTempC
                annual_report.maxDate = weather_reading.pkt
                annual_report.minTemp = weather_reading.minTempC
                annual_report.minDate = weather_reading.pkt
                annual_report.mostHumid = weather_reading.maxHumidity
                annual_report.humidDate = weather_reading.pkt
                weather_reading = WeatherReading(file.readline())
                flag = True

            while weather_reading is not None:
                if weather_reading.maxTempC is not None and annual_report.maxTemp < weather_reading.maxTempC:
                    annual_report.maxTemp = weather_reading.maxTempC
                    annual_report.maxDate = weather_reading.pkt
                if weather_reading.minTempC is not None and annual_report.minTemp > weather_reading.minTempC:
                    annual_report.minTemp = weather_reading.minTempC
                    annual_report.minDate = weather_reading.pkt
                if weather_reading.maxHumidity is not None and annual_report.mostHumid < weather_reading.maxHumidity:
                    annual_report.mostHumid = weather_reading.maxHumidity
                    annual_report.humidDate = weather_reading.pkt
                record = file.readline()
                if record != '':
                    weather_reading = WeatherReading(record)
                else:
                    weather_reading = None

            file.close()
        if flag is True:
            return annual_report
        else:
            print("File(s) not found!")

    @staticmethod
    def calculate_monthly_report(directory, year, month):
        print("\n\n\n~~~TASK 2~~~")

        flag = False
        try:
            file = open(filePath.format(directory, year, months[month]))
            file.readline()
            weather_reading = WeatherReading(file.readline())
            monthly_report = MonthlyReport()
            if flag is False:
                monthly_report.maxMeanTemp = weather_reading.meanTempC
                monthly_report.minMeanTemp = weather_reading.meanTempC
                monthly_report.meanHumid = weather_reading.meanHumidity
                weather_reading = WeatherReading(file.readline())
                days = 1

            while weather_reading is not None:
                if weather_reading.maxTempC is not None and weather_reading.minTempC is not None:
                    if weather_reading.meanTempC is None:
                        weather_reading.meanTempC = (weather_reading.maxTempC + weather_reading.minTempC) / 2
                    if monthly_report.maxMeanTemp < weather_reading.meanTempC:
                        monthly_report.maxMeanTemp = weather_reading.meanTempC
                    if monthly_report.minMeanTemp > weather_reading.meanTempC:
                        monthly_report.minMeanTemp = weather_reading.meanTempC
                    monthly_report.meanHumid += weather_reading.meanHumidity
                record = file.readline()
                if record != '':
                    weather_reading = WeatherReading(record)
                    days += 1
                else:
                    weather_reading = None

            file.close()
            monthly_report.meanHumid /= days

            return monthly_report

        except FileNotFoundError:
            print("File not found")

    @staticmethod
    def draw_bar_chart_for_a_month(directory, year, month):

        print("\n\n\n~~~TASK 3~~~")
        try:
            file = open(filePath.format(directory, year, months[month]))
            file.readline()
            weather_reading = WeatherReading(file.readline())
            day = 1
            while weather_reading is not None:
                if weather_reading.maxTempC is not None and weather_reading.maxTempC is not None:
                    str1 = ("+" * weather_reading.maxTempC) + " " + str(weather_reading.maxTempC) + "\n"
                    str2 = ("+" * weather_reading.minTempC) + " " + str(weather_reading.minTempC) + "\n"

                    print("{:02d} ".format(day), end='')
                    pr_red(str1)
                    print("{:02d} ".format(day), end='')
                    pr_cyan(str2)
                record = file.readline()
                if record != '':
                    weather_reading = WeatherReading(record)
                    day += 1
                else:
                    weather_reading = None

            file.close()

        except FileNotFoundError:
            print("file not found")

    @staticmethod
    def draw_bar_chart_for_a_month2(directory, year, month):

        print("\n\n\n~~~BONUS TASK~~~")
        try:
            file = open(filePath.format(directory, year, months[month]))
            file.readline()
            weather_reading = WeatherReading(file.readline())
            day = 1
            while weather_reading is not None:
                if weather_reading.maxTempC is not None and weather_reading.maxTempC is not None:
                    str1 = ("+" * weather_reading.minTempC)
                    str2 = ("+" * weather_reading.maxTempC) + " "
                    print("{:02d} ".format(day), end='')

                    pr_cyan(str1)
                    pr_red(str2)
                    print(weather_reading.minTempC, "C - ", weather_reading.maxTempC, "C")
                record = file.readline()
                if record != '':
                    weather_reading = WeatherReading(record)
                    day += 1
                else:
                    weather_reading = None

            file.close()

        except FileNotFoundError:
            print("file not found")


print(sys.argv)

directory = sys.argv[1]
i = 2
while i < len(sys.argv):
    argument = sys.argv[i]
    if i % 2 == 0:
        choice = argument
    else:
        if choice == "-e":
            annualReport = CalculateResults.calculate_annual_report(directory, argument)
            if annualReport is not None:
                annualReport.display()
        if choice == "-a":
            year, month = argument.split('/')
            monthlyReport = CalculateResults.calculate_monthly_report(directory, year, int(month))
            monthlyReport.display()
        if choice == "-c":
            year, month = argument.split('/')
            CalculateResults.draw_bar_chart_for_a_month(directory, year, int(month))
            CalculateResults.draw_bar_chart_for_a_month2(directory, year, int(month))
    i += 1
