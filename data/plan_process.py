import openpyexcel


class DataProcess:

    def __init__(self, file):
        self.file = file
        self.read = openpyexcel.load_workbook(file)

    def processing(self, key_row):
        sheet = self.read.worksheets[0]
        w_sheet = self.read.worksheets[1]
        majors = set()
        for row in range(1, sheet.max_row + 1):
            w_sheet.cell(row=row, column=1, value=sheet.cell(row, key_row).value)
            majors.add(sheet.cell(row, key_row).value)
            temp = ""
            for col in range(1, sheet.max_column + 1):
                if col == key_row or sheet.cell(row, col).value is None:
                    continue
                temp += sheet.cell(row, col).value + "-"
                print(sheet.cell(row=row, column=col).value)
            if temp[-1] == "-":
                temp = temp[:-1]
            w_sheet.cell(row, 2, temp)
        # self.combine(majors)
        self.read.save(self.file.split('/')[-1])
        self.read.close()

    def combine(self, majors):
        sheet = self.read.worksheets[1]
        w_sheet = self.read.worksheets[2]
        temp = ""
        index = 1
        for name in majors:
            if name == "专业名称":
                continue
            for row in range(1, sheet.max_row + 1):
                if sheet.cell(row, 1).value == name:
                    temp += sheet.cell(row, 2).value + ", "
            temp = temp[:-2]
            w_sheet.cell(index, 1, value=name)
            w_sheet.cell(index, 2, value=temp)
            temp = ""
            index += 1


if __name__ == "__main__":
    handle = DataProcess("../crwal/data/plan.xlsx")
    handle.processing(5)
