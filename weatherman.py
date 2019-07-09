import argparse
import csv


from datetime import datetime


def print_red(skk): print("\033[91m {}\033[00m".format(skk), end='')


def print_cyan(skk): print("\033[96m {}\033[00m".format(skk), end='')


def make_int(s):
    s = s.strip()
    return int(s) if s else None


def make_double(s):
    s = s.strip()
    return float(s) if s else None


class WeatherReading:
    def __init__(self, record):
        if record != '':
            self.pkt, self.max_temp, self.mean_temp, self.min_temp, self.dew_point, self.mean_dew_point, \
            self.minDewPointC, self.maxHumidity, self.meanHumidity, self.minHumidity, self.maxSeaLevelPressure, \
            self.meanSeaLevelPressure, self.minSeaLevelPressure, self.maxVisibility, self.meanVisibility, \
            self.minVisibility, self.maxWindSpeed, self.meanWindSpeed, self.maxGustSpeed, self.precipitation, \
            self.cloudClover, self.event, self.windDirDegrees = record[0], record[1], record[2], record[3]\
                , record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11], record[12]\
                , record[13], record[14], record[15], record[16], record[17], record[18], record[19], record[20]\
                , record[21], record[22]

            self.pkt = datetime.strptime(self.pkt, '%Y-%m-%d')
            self.max_temp = make_int(self.max_temp)
            self.min_temp = make_int(self.min_temp)
            self.mean_temp = make_int(self.mean_temp)
            self.meanHumidity = make_int(self.meanHumidity)
            self.maxHumidity = make_int(self.maxHumidity)
            self.minHumidity = make_int(self.minHumidity)
            self.dew_point = make_int(self.dew_point)
            self.mean_dew_point = make_int(self.mean_dew_point)
            self.minDewPointC = make_int(self.minDewPointC)
            self.minSeaLevelPressure = make_double(self.minSeaLevelPressure)
            self.meanSeaLevelPressure = make_double(self.meanSeaLevelPressure)
            self.maxSeaLevelPressure = make_double(self.maxSeaLevelPressure)
            self.maxVisibility = make_double(self.maxVisibility)
            self.minVisibility = make_double(self.minVisibility)
            self.meanVisibility = make_double(self.meanVisibility)
            self.maxWindSpeed = make_double(self.maxWindSpeed)
            self.meanWindSpeed = make_double(self.meanWindSpeed)
            self.maxGustSpeed = make_double(self.maxGustSpeed)
            self.precipitation = make_double(self.precipitation)
            self.cloudClover = make_double(self.cloudClover)


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
filePath = "{0}/Murree_weather_{1}_{2}.txt"


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
        self.report = self.report.format(self.maxTemp, months[self.maxDate.month - 1], self.maxDate.day,
                                         self.minTemp, months[self.minDate.month - 1], self.minDate.day,
                                         self.mostHumid, months[self.humidDate.month - 1], self.humidDate.day)
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

    def __init__(self):
        self.directory = None
        self.year = None
        self.month = None

    def calculate_annual_report(self, directory, year):
        print("\n\n\n~~~TASK 1~~~")
        self.directory = directory
        self.year = year
        annual_report = AnnualReport()
        for month in months:
            try:
                with open(filePath.format(directory, year, month)) as file:
                    row_count = 0
                    file = csv.reader(file)

                    for row in file:

                        if row_count == 0:
                            row_count += 1
                            continue
                        weather_reading = WeatherReading(row)
                        if row_count == 1:
                            annual_report.maxTemp = weather_reading.max_temp
                            annual_report.maxDate = weather_reading.pkt
                            annual_report.minTemp = weather_reading.min_temp
                            annual_report.minDate = weather_reading.pkt
                            annual_report.mostHumid = weather_reading.maxHumidity
                            annual_report.humidDate = weather_reading.pkt
                            row_count += 1
                        else:
                            if weather_reading.max_temp is not None and annual_report.maxTemp < weather_reading.max_temp:
                                annual_report.maxTemp = weather_reading.max_temp
                                annual_report.maxDate = weather_reading.pkt
                            if weather_reading.min_temp is not None and annual_report.minTemp > weather_reading.min_temp:
                                annual_report.minTemp = weather_reading.min_temp
                                annual_report.minDate = weather_reading.pkt
                            if weather_reading.maxHumidity is not None and annual_report.mostHumid < weather_reading.maxHumidity:
                                annual_report.mostHumid = weather_reading.maxHumidity
                                annual_report.humidDate = weather_reading.pkt
            except FileNotFoundError:
                continue
        return annual_report

    def calculate_monthly_report(self, directory, year, month):
        print("\n\n\n~~~TASK 2~~~")

        self.directory = directory
        self.year = year
        self.month = month

        try:
            with open(filePath.format(directory, year, months[month - 1])) as file:
                row_count = 0
                file = csv.reader(file)
                monthly_report = MonthlyReport()

                for row in file:
                    if row_count == 0:
                        row_count += 1
                        continue
                    weather_reading = WeatherReading(row)
                    if row_count == 1:
                        monthly_report.maxMeanTemp = weather_reading.mean_temp
                        monthly_report.minMeanTemp = weather_reading.mean_temp
                        monthly_report.meanHumid = weather_reading.meanHumidity
                        row_count += 1
                    if weather_reading.max_temp is not None and weather_reading.min_temp is not None:
                        if weather_reading.mean_temp is None:
                            weather_reading.mean_temp = (weather_reading.max_temp + weather_reading.min_temp) / 2
                        if monthly_report.maxMeanTemp < weather_reading.mean_temp:
                            monthly_report.maxMeanTemp = weather_reading.mean_temp
                        if monthly_report.minMeanTemp > weather_reading.mean_temp:
                            monthly_report.minMeanTemp = weather_reading.mean_temp
                        monthly_report.meanHumid += weather_reading.meanHumidity
                        row_count += 1
                monthly_report.meanHumid /= row_count

            return monthly_report

        except FileNotFoundError:
            print("File not found")

    def display_bars(self, bars):
        try:
            with open(filePath.format(self.directory, self.year, months[self.month - 1])) as file:
                row_count = 0
                file = csv.reader(file)
                day = 1
                for row in file:
                    if row_count == 0:
                        row_count += 1
                        continue
                    weather_reading = WeatherReading(row)
                    if weather_reading.max_temp is not None and weather_reading.max_temp is not None:
                        if bars == 1:
                            str1 = ("+" * weather_reading.min_temp)
                            str2 = ("+" * weather_reading.max_temp) + " "
                            print("{:02d} ".format(day), end='')

                            print_cyan(str1)
                            print_red(str2)
                            print(weather_reading.min_temp, "C - ", weather_reading.max_temp, "C")
                        if bars == 2:
                            str1 = ("+" * weather_reading.max_temp) + " " + str(weather_reading.max_temp) + "\n"
                            str2 = ("+" * weather_reading.min_temp) + " " + str(weather_reading.min_temp) + "\n"

                            print("{:02d} ".format(day), end='')
                            print_red(str1)
                            print("{:02d} ".format(day), end='')
                            print_cyan(str2)
                        day += 1
        except FileNotFoundError:
            print("file not found")

    def two_horizontal(self, directory, year, month):

        print("\n\n\n~~~TASK 3~~~")
        self.directory = directory
        self.year = year
        self.month = month
        self.display_bars(2)

    def one_horizontal(self, directory, year, month):

        print("\n\n\n~~~BONUS TASK~~~")
        self.directory = directory
        self.year = year
        self.month = month
        self.display_bars(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--year", required=False, help="Annual Report")
    ap.add_argument("-a", "--month", required=False, help="Monthly Report")
    ap.add_argument("-c", "--horizontal", required=False, help="draw horizontal chart")
    ap.add_argument("-f", "--file", required=False, help="file(s) path")

    args = vars(ap.parse_args())

    calculator = CalculateResults()
    if args["year"] is not None:
        annual_report = calculator.calculate_annual_report(args["file"], args["year"])
        if annual_report is not None:
            annual_report.display()
    if args["month"] is not None:
        year, month = args["month"].split('/')
        monthly_report = calculator.calculate_monthly_report(args["file"], year, int(month))
        monthly_report.display()
    if args["horizontal"] is not None:
        year, month = args["horizontal"].split('/')
        calculator.two_horizontal(args["file"], year, int(month))
        calculator.one_horizontal(args["file"], year, int(month))


if __name__ == "__main__":
    main()
