import xlsxwriter

workbook = xlsxwriter.Workbook("tests.xlsx")


def run_multiple_tests(number_apk):
    vars = ["#", "MD5", "Start Time", "End Time", "Duration", "Name", "Package", "Downloads", "APK Size", "Version Name", "Version Code"]
    sheet = workbook.add_worksheet("Results - Multiple (" + str(number_apk) + ")")


def run_sequence_tests():
    vars = ["#", "MD5", "Start Time", "End Time", "Duration", "Name", "Package", "Downloads", "APK Size", "Version Name", "Version Code"]
    sheet = workbook.add_worksheet("Results - Sequence")
    bold = workbook.add_format({'bold': True})
    # write the header
    cols = 0
    for var in vars:
        sheet.write(0, cols, var, bold)
        cols = cols + 1


if __name__=="__main__":
    run_sequence_tests()
    run_multiple_tests(10)
    workbook.close()
