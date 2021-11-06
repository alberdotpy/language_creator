from translator import detect_language
from db import update_db, query_table
from replacements import shuffle, permute
import wx
import wx.grid


class Robot(wx.Frame):
    def __init__(self, parent, title):
        super(Robot, self).__init__(parent, title=title, size=(750, 575))
        self.init_ui()
        self.Centre()
        self.SetTitle("Language Creator")
        try:
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(wx.Bitmap("img\\logo.ico", wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
        except Exception as e:
            print("The favicon was not found, please save the favicon in the img directory as icon.png")

    def init_ui(self):
        nb = wx.Notebook(self)
        nb.AddPage(Panel1(nb), "App")
        nb.AddPage(Panel2(nb), "Data")
        self.Show(True)


class Panel1(wx.Panel):
    def __init__(self, parent):
        super(Panel1, self).__init__(parent)
        sizer = wx.GridBagSizer(9, 9)

        # Header
        try:
            imageFile = "img\\logo.png"
            png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            png = scale_bitmap(png, 90, 60)
            logo = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
            sizer.Add(logo, pos=(0, 0), span=(1, 9), flag=wx.BOTTOM | wx.ALIGN_CENTER | wx.TOP, border=10)
        except Exception as e:
            print("The logo file was not found, please save the logo file in the img directory as logo.png")

        lbl_vowels = wx.StaticText(self, label='Vowels : ')
        sizer.Add(lbl_vowels, pos=(1, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        self.input_vowels = wx.TextCtrl(self, value="aeiou")
        sizer.Add(self.input_vowels, pos=(1, 1), span=(1, 2), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)

        lbl_consonants = wx.StaticText(self, label='Consonants : ')
        sizer.Add(lbl_consonants, pos=(2, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        self.input_consonants = wx.TextCtrl(self, value="bcdfghjklmnpqrstvwxyz")
        sizer.Add(self.input_consonants, pos=(2, 1), span=(1, 2), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)

        lbl_vowp = wx.StaticText(self, label='Vowel Permutations : ')
        sizer.Add(lbl_vowp, pos=(1, 3), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        nb_vow = ['0', '1', '2', '3', '4', '5']
        self.vowel_p = wx.ComboBox(self, choices=nb_vow, value='2')
        sizer.Add(self.vowel_p, pos=(1, 4), flag=wx.LEFT, border=15)

        lbl_conp = wx.StaticText(self, label='Consonant Permutations : ')
        sizer.Add(lbl_conp, pos=(2, 3), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        nb_vow = ['0', '2', '4', '6', '8', '10', '12', '14', '16']
        self.consonants_p = wx.ComboBox(self, choices=nb_vow, value='8')
        sizer.Add(self.consonants_p, pos=(2, 4), flag=wx.LEFT, border=15)

        lbl_conf = wx.StaticText(self, label='New Language : ')
        sizer.Add(lbl_conf, pos=(3, 0), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_LEFT, border=15)
        self.input_language = wx.TextCtrl(self, value="")
        sizer.Add(self.input_language, pos=(3, 1), span=(1, 2), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_LEFT, border=15)

        btn_store = wx.Button(self, label="Save")
        sizer.Add(btn_store, pos=(3, 3), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER, border=15)
        self.Bind(wx.EVT_BUTTON, self.onStore, btn_store)

        btn_load = wx.Button(self, label="Load")
        sizer.Add(btn_load, pos=(3, 4), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER, border=15)
        self.Bind(wx.EVT_BUTTON, self.onLoad, btn_load)

        lbl_text1 = wx.StaticText(self, label='Original text : ')
        sizer.Add(lbl_text1, pos=(4, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        self.textBox1 = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer.Add(self.textBox1, pos=(5, 0), span=(3, 9), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)

        btn_execute = wx.Button(self, label="Transform")
        sizer.Add(btn_execute, pos=(8, 0), span=(1, 9), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER, border=15)
        self.Bind(wx.EVT_BUTTON, self.onExecute, btn_execute)

        lbl_text2 = wx.StaticText(self, label='Resulting text : ')
        sizer.Add(lbl_text2, pos=(9, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        self.textBox2 = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        sizer.Add(self.textBox2, pos=(10, 0), span=(3, 9), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)


        # Footer
        line = wx.StaticLine(self)
        sizer.Add(line, pos=(13, 0), span=(1, 9), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        titre = wx.StaticText(self, label="© 2021 - alberdotpy")
        font = wx.Font(7, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        titre.SetFont(font)
        sizer.Add(titre, pos=(14, 0), span=(1, 9), flag=wx.BOTTOM | wx.ALIGN_CENTER | wx.TOP, border=5)

        # Sizer
        sizer.AddGrowableCol(8, 0)
        #sizer.AddGrowableRow(9, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.new_vowels = []
        self.new_consonants = []

    def onExecute(self, event):
        """Method to transform original text into one with the new language"""
        self.new_consonants, self.new_vowels = [], []
        txt_o = self.textBox1.GetValue().lower()
        vowels = 'aeiou'
        self.new_vowels = self.input_vowels.GetValue()
        consonants = 'bcdfghjklmnpqrstvwxyz'
        self.new_consonants = self.input_consonants.GetValue()
        if self.new_vowels == 'aeiou':
            self.new_vowels = shuffle(vowels)
        if self.new_consonants == 'bcdfghjklmnpqrstvwxyz':
            self.new_consonants = shuffle(consonants)
        vow_p = int(self.vowel_p.GetValue())
        con_p = int(self.consonants_p.GetValue())
        txt_r = permute(txt_o, vowels, self.new_vowels, vow_p)
        txt_r = permute(txt_r, consonants, self.new_consonants, con_p)
        self.textBox2.SetValue(txt_r)

    def onStore(self, event):
        """Method to store the created language in the SQL database"""
        txt_o = self.textBox1.GetValue().lower()
        vowels = self.input_vowels.GetValue()
        consonants = self.input_consonants.GetValue()
        vow_p = int(self.vowel_p.GetValue())
        con_p = int(self.consonants_p.GetValue())
        txt_r = permute(txt_o, vowels, self.new_vowels, vow_p)
        txt_r = permute(txt_r, consonants, self.new_consonants, con_p)
        base_lang = detect_language(txt_o)
        language_name = self.input_language.GetValue()
        print(base_lang, vow_p, con_p, self.new_vowels, self.new_consonants, txt_o, txt_r)
        update_db(language_name, base_lang, vow_p, con_p, self.new_vowels, self.new_consonants, txt_o, txt_r)

    def onLoad(self, event):
        """Method to load any stored language in the SQL database"""
        language_name = self.input_language.GetValue()
        dt = query_table(language_name)
        print(dt)
        line = dt[0]
        vowels = line[4][1:-2].replace("'", "").replace(", ", "")
        consonants = line[5][1:-2].replace("'", "").replace(", ", "")
        self.input_vowels.SetValue(vowels)
        self.input_consonants.SetValue(consonants)
        self.vowel_p.SetValue(line[2])
        self.consonants_p.SetValue(line[3])


class Panel2(wx.grid.Grid):
    def __init__(self, parent):
        super(Panel2, self).__init__(parent)
        dt = query_table()
        self.CreateGrid(len(dt), 9)
        grid = wx.grid.Grid(self, -1)
        grid.AutoSizeColumns()
        self.SetColLabelValue(0, "Language Name")
        self.SetColLabelValue(1, "Base Language")
        self.SetColLabelValue(2, "Vowel Permutations")
        self.SetColLabelValue(3, "Consonant Permutations")
        self.SetColLabelValue(4, "Vowels Used")
        self.SetColLabelValue(5, "Consonants Used")
        self.SetColLabelValue(6, "Original Text")
        self.SetColLabelValue(7, "Resulting Text")
        self.SetColLabelValue(8, "Date")
        for x in range(0, len(dt)):
            self.SetCellValue(x, 0, dt[x][0])
            self.SetCellValue(x, 1, dt[x][1])
            self.SetCellValue(x, 2, str(dt[x][2]).split(":")[0])
            self.SetCellValue(x, 3, str(dt[x][3]).split('.')[0])
            self.SetCellValue(x, 4, str(dt[x][4]).split('.')[0])
            self.SetCellValue(x, 5, str(dt[x][5]).split('.')[0])
            self.SetCellValue(x, 6, str(dt[x][6]).split('.')[0])
            self.SetCellValue(x, 7, str(dt[x][7]).split('.')[0])
            self.SetCellValue(x, 8, str(dt[x][8]).split('.')[0])


def main():
    app = wx.App()
    Robot(None, 'Robot').Show()
    app.MainLoop()


def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result


if __name__ == '__main__':
    main()






