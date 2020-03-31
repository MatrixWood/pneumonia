import json
import datetime
from pyecharts.charts import Pie
from pyecharts import options as opts

today = datetime.date.today().strftime('%Y%m%d')   #20200315
datafile = 'data/'+ today + '.json'
with open(datafile, 'r', encoding='UTF-8') as file:
    json_array = json.loads(file.read())

china_data = []
for province in json_array:
    china_data.append((province['provinceShortName'], province['confirmedCount']))
china_data = sorted(china_data, key=lambda x: x[1], reverse=True)

print(china_data)

labels = [data[0] for data in china_data]
counts = [data[1] for data in china_data]

m = {
    Pie()
    .add("累计确诊", [list(z) for z in zip(labels, counts)], center=["50%", "80%"],radius="40%")
    .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
    .set_series_opts(label_opts=opts.LabelOpts(
        font_size=12,
        formatter="{b}: {c}",
        ),
        is_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title='全国实时确诊数据',
                                            subtitle='数据来源：丁香园',
                                            pos_left="15%"))
    .render(path='./全国实时确诊数据pie.html')
}