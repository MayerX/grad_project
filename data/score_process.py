import openpyexcel


class DataProcess:

    def __init__(self, file):
        self.file = file
        self.read = openpyexcel.load_workbook(file)

    def processing(self, major, year):
        sheet = self.read.worksheets[0]
        w_sheet = self.read.worksheets[1]
        majors = set()
        for row in range(1, sheet.max_row + 1):
            w_sheet.cell(row=row, column=1, value=sheet.cell(row, major).value)
            w_sheet.cell(row, 2, value=sheet.cell(row, year).value)
            majors.add(sheet.cell(row, major).value)
            temp = ""
            for col in range(1, sheet.max_column + 1):
                if col == major or col == year or sheet.cell(row, col).value is None:
                    continue
                temp += sheet.cell(row, col).value + "-"
                print(sheet.cell(row=row, column=col).value)
            if temp[-1] == "-":
                temp = temp[:-1]
            w_sheet.cell(row, 3, temp)
        self.insert_major(majors)
        self.read.save(self.file.split('/')[-1].split('.')[0] + "_data.xlsx")
        self.read.close()

    def insert_major(self, majors):
        w_sheet = self.read.worksheets[2]
        for index, value in enumerate(majors):
            w_sheet.cell(index+1, 1, value)
        # w_sheet.cell(1, 1, majors)
        # sheet = self.read.worksheets[1]
        # w_sheet = self.read.worksheets[2]
        # temp = ""
        # index = 1
        # for name in majors:
        #     if name == "专业名称":
        #         continue
        #     for row in range(1, sheet.max_row + 1):
        #         if sheet.cell(row, 1).value == name:
        #             temp += sheet.cell(row, 2).value + ", "
        #     temp = temp[:-2]
        #     w_sheet.cell(index, 1, value=name)
        #     w_sheet.cell(index, 2, value=temp)
        #     temp = ""
        #     index += 1


if __name__ == "__main__":
    handle = DataProcess("../crwal/data/score.xlsx")
    handle.processing(5, 1)
