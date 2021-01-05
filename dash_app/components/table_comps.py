import dash_html_components as html
from dash_bootstrap_components import Table
def sort_areas(frame_dic):
    """returns a list of tuples
    0: image_name
    1: area size
    2: area x
    3: area y"""
    area_ls = []
    for image in frame_dic["image_data_ls"]:
        #print("ty:",type(image),image)
        if(image != 'EMPTY_IMAGE_LS'):
            for entry in image["img_largest_areas"]:
                val = (entry[0],int(entry[1]),entry[2],entry[3],entry[4],entry[5])
                area_ls.append(val)

    area_ls = sorted(area_ls,key = lambda tup: int(tup[1]))
    #print("sorted areas:",area_ls)
    area_ls.reverse()
    return area_ls




def create_area_table(frame_dic):
    area_ls = sort_areas(frame_dic)
    table_header = [
        html.Thead(html.Tr([html.Th("Pore Size"),
                            html.Th("Image Name"),
                            html.Th("(x,y)"),
                            html.Th("Diameter of Largest Circle"),
                            html.Th("center")]
                           ))
    ]
    rows = []
    print(type(area_ls),"area_ls")
    #print(area_ls)
    if(len(area_ls)==0):
        return []
    for area in area_ls:
        px_str = ' (' + str(area[5]) + 'pixels' + ')'
        row = html.Tr([html.Td(int(area[1])),
            html.Td(area[0]),
            html.Td("(" + str(area[2])+ "," + str(area[3]) +")"),
            html.Td(str(area[5]*float(frame_dic["scale"])) +px_str),
            html.Td(str(area[4]))
            #html.Td(area[4]),
            #html.Td(area[5])
            ])
        rows.append(row)

    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= True,
        dark = True,
        striped = True)
    return table


def create_pore_table(frame_dic):
    pore_ls = []
    name_ls = []
    for image in frame_dic["image_data_ls"]:
        if(image!="EMPTY_IMAGE_LS"):
            pore_ls.append(image["pores"])
            name_ls.append(image["img_name"])
    table_header = [
        html.Thead(html.Tr([
                            html.Th("Image Name"),
                            html.Th("Porosity"),]
                           ))
    ]
    rows = []
    if(len(pore_ls)==0):
        return []
    i =0
    while i< len(pore_ls):
        row = html.Tr([
            html.Td(name_ls[i]),
            html.Td(pore_ls[i]),
            ])
        rows.append(row)
        i=i+1

    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= True,
        dark = True,
        striped = True)
    return table
