import wx
import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class EDictPanel(wx.Panel):    
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}
        self.listbox = wx.ListBox(self)
        smartDict = SmartDict(self.listbox)
        main_sizer.Add(self.listbox,0, wx.ALL | wx.EXPAND, 5)        
        edit_button = wx.Button(self, label='Search')
        edit_button.Bind(wx.EVT_BUTTON, self.on_search)
        main_sizer.Add(edit_button, 0, wx.ALL | wx.CENTER, 5)        
        self.SetSizer(main_sizer)

    def on_search(self, event):
        word = wx.GetTextFromUser('Enter a word to search up', 'Insert dialog')
        if word != '':
            self.listbox.Append(word)

    def update_mp3_listing(self, folder_path):
        print(folder_path)


class EDictFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None,title='Smart Dictionary')
        self.panel = EDictPanel(self)
        self.Show()
class SmartDict:
    def __init__(self, list):
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Dieuestbon1!",
            database="Edictdb"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Fdict")
        self.myresult = mycursor.fetchall()
        for k,v in self.myresult:
            list.Append(k)
            list.Append(v)
            list.Append("-----------------------------------")

    def local_search(self,word):
        for k,v in self.myresult:
            if(k==word) :
                return v
        return None
    def online_search(word):
        url = 'https://www.google.com/search?rlz=1C5CHFA_enUS898US899&sxsrf=ALeKk03NF0lPvS7XRfNDFbHcPiM5kaKXEg:1590181949238&q=Dictionary&stick=H4sIAAAAAAAAAONQesSoyi3w8sc9YSmZSWtOXmMU4-LzL0jNc8lMLsnMz0ssqrRiUWJKzeNZxMqFEAMA7_QXqzcAAAA&zx=1590183723437'
        url += '#dobs='+word
        driver = webdriver.Chrome('/Users/ntt/Desktop/Webscraper/chromedriver')
        driver.get(url)
        driver.implicitly_wait(10)
        try:
            types = driver.find_elements_by_class_name('lW8rQd')
            descriptions = driver.find_elements_by_class_name('eQJLDd')
        except:
            return None
        desc = ""
        for type in types:
            idx = (types.index(type))
            desc +=type.text+"\n"+descriptions[idx].text+"\n"
        if(desc == ""):
            return None
        return desc


if __name__ == '__main__':
    app = wx.App(False)
    frame = EDictFrame()
    app.MainLoop()


