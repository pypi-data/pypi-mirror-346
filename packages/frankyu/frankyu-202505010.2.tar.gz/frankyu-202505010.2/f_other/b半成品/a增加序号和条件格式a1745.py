import f_excel.bcp半成品.run_excel_conditional_formatting_Copy1 as ru

app,bo,sh = ru.initialize_excel()

bo.Name

sh.Name

rng = sh.Range("A1:Z999")



 
def ruset_cell_value_and_select(sheet, value_cell="N12", value_to_set=0, select_cell="K7"):
    """
    設定指定儲存格的值，並選取另一個儲存格。
    """
    try:
        sheet.Range(value_cell).Value = value_to_set
        print(f"已將儲存格 {value_cell} 的值設定為 {value_to_set}。")
        #sheet.Range(select_cell).Select()
        print(f"已選取儲存格 {select_cell}。")
    except Exception as e:
        print(f"設定儲存格值或選取儲存格時發生錯誤: {e}")
        #traceback.print_exc()

ru.clear_conditional_formatting(sh)

ru.apply_border_conditional_formatting(rng)

ru.apply_font_conditional_formatting(rng)


#ru.run_excel_conditional_formatting()

bbb = 200
for i in   list( zip( range(1,bbb),   range(1,bbb),  range(1,bbb))):
    print(i)
    
    ruset_cell_value_and_select(sh,f"{"A"}{i[1]}",i[2],"A1")

sh.Range("A1").Select()

import frankyu.frankyu as fr

fr.dao_ji_shi(10)