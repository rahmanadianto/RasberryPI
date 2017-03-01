import requests

#ID Barang, Kode Kategori, Kode Permohonan Vendor
url_product = "http://www.nawastratech.com:9002/feed.ashx?data=product&lab=AL"
#ID Penguji
url_tester = "http://www.nawastratech.com:9002/feed.ashx?data=tester&lab=AL"
#Kode Alat Pengujian, Keterangan
url_device = "http://www.nawastratech.com:9002/feed.ashx?data=device&lab=AL"

def download_data():
    product = requests.get(url_product)
    tester = requests.get(url_tester)
    device = requests.get(url_device)
    
    with open("product.txt", "w") as f:
        f.write(product.text)
        
    with open("tester.txt", "w") as f:
        f.write(tester.text)
        
    with open("device.txt", "w") as f:
        f.write(device.text)
        

