import openpyxl as op 

#기존 파일을 로딩 
wb = op.load_workbook("test.xlsx")

#새로운 시트 추가 
ws = wb.create_sheet("직원명부")

wb.save("test2.xlsx")

