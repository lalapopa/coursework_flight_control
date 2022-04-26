import pandas as pd
import config

mach_area = pd.read_csv(config.PATH_DATA + config.FILE_MACH_AREA, header=None) 
height_area = pd.read_csv(config.PATH_DATA+config.FILE_H, header=None)
height_area = height_area.rename(columns={0: '$H$'})

flight_area = height_area.join(mach_area)
styler = flight_area.style.format(precision=3).hide()
print(styler.to_latex())

