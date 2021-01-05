import tkinter as tk
import requests as rq
from PIL import ImageTk, Image
root = tk.Tk()
root.config(bg='#ffffff')
root.title('Google-AD')
root.wm_minsize(700,400)
root.wm_maxsize(700,400)

def clear_placeholder(e):
    en.delete("0", "end")
    en.configure(fg='black')
    
def get_info(place):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {'input': f'{place}',
          'inputtype': 'textquery',
          'fields': 'place_id,photos,formatted_address,name,rating,opening_hours,geometry',
          'key': 'AIzaSyAtzvDoPkWFu8g6urdrhaManQq-zccP9RM',
          'photoreference':'CmRaAAAAK9eay-SzysPwoyqs2MC113XeQmdMvxXXaJSND8TwSbhwRFUgN5x5E4hkvtJTQ75uPWQQ8IgqGu9N5-78T8Vms5M_O2xk_CyWnXm3eSg-1tDeSINvfTvDuDkVkqgsphf9EhAyoyHyOnG0qqm8TQOrOCOfGhTNnECx7B_1RUv16V3qDuv9MnfxKw'
         }
    photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=640&maxheight=480&photoreference={}&key=AIzaSyAtzvDoPkWFu8g6urdrhaManQq-zccP9RM"
    
    info_response = rq.get(url,params=params)
    if info_response.headers['Content-type']=='application/json; charset=UTF-8':
        info = info_response.json()
        #print(info)
        if info['status']=='OK':
            data =  'Place Name'.ljust(10)      + ' : ' + info['candidates'][0]['name'] +'\n'
            data += 'Address'.ljust(10)   +' : ' + info['candidates'][0]['formatted_address'] + '\n'
            data += 'Latitude'.ljust(10)  +' : ' + str(info['candidates'][0]['geometry']['location']['lat']) + '\n'
            data += 'Longitude'.ljust(10) +' : ' + str(info['candidates'][0]['geometry']['location']['lng']) + '\n'
            
            img_ref = info['candidates'][0]['photos'][0]['photo_reference']
            img_response = rq.get(photo_url.format(img_ref))
            if img_response.headers['Content-type'] == 'image/jpeg':
                with open('api_image.jpeg','wb') as fp:
                    fp.write(img_response.content)
                    fp.close
                #img = plt.imread('api_image.jpeg')
                return data,True
    
            else:
                return data,False
            
        else:
            return 'Data Not Found !',False
    
    else:
        return 'Data Not Found !',False
    
def home():
    global img
    global icon
    global en
    global se
    img = ImageTk.PhotoImage(Image.open("google.png")) 
    icon=tk.Label(root,image=img,bg='#ffffff')
    icon.pack(pady=40)
    en = tk.Entry(root,width=30,font=('Times',15),fg='#bbbbbb')
    en.insert(0, 'Search Place Here...')
    en.bind('<Return>',search)
    en.pack()
    en.bind("<FocusIn>", clear_placeholder)
    se = tk.Button(root,text='Search',width=10,font=('Times',13,),fg='#777777')
    se.bind("<ButtonRelease-1>",search)
    se.pack(pady=50)
    
def clear_data(e):
    data_label.destroy()
    image_label.destroy()
    bk.destroy()
    home()

def clear_home():
     icon.destroy()
     se.destroy()
     en.destroy()

def back_button():
    global bk
    bk = tk.Button(root,text='Back',font=('Times',10),width=15)
    bk.bind('<ButtonRelease-1>',clear_data)
    bk.pack()
    return None

#def loading():
#   place = en.get()
#    clear_home()
#    global load
#    load = tk.Label(text='Loading...',font=('Times',20))
#    load.config(anchor='center')
#    load.pack()
#    return place
    
def search(e):
    place = en.get()
    clear_home()
    #place=loading()
    #print(en.get())
    data,img = get_info(place)
    #load.destroy()
    global data_label
    global image_label
    global place_img
    data_label = tk.Label(root,text=data,font=('Courier',12),bg='#ffffff')
    data_label.config(justify=tk.LEFT)
    data_label.pack()
    image_label = tk.Label(root,width=300,height=200,bg='#ffffff')
    image_label.pack(pady=20)
    if img:
        place_img = ImageTk.PhotoImage(Image.open('api_image.jpeg'))
        image_label.config(image=place_img)
    else:
        place_img = ImageTk.PhotoImage(Image.open('api_image.jpeg'))
        image_label.config(text='Image Not Found !',width=15,height=7)
    back_button()
    
home()
root.mainloop()
