import AnalizDataClass
import FT
import plotly

My_Data_Base = FT.Data_Base()
adc = AnalizDataClass.ADC()

adc.lineChart(My_Data_Base.Get_Data(), "WouldYouRec").show()
adc.BarChart("Artist Name", My_Data_Base.Get_Data() ).show()
