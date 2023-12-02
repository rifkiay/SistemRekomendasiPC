import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="python"
)

database = mydb.cursor()
database1 = mydb.cursor()
database2 = mydb.cursor()

database.execute("SELECT * FROM processor_amd")
list_processor = database.fetchall()

database1.execute("SELECT * FROM motherboard_amd")
list_motherboard = database1.fetchall()


harga = int(input("Masukkan Harga : "))
processor=harga*0.3
motherboard=harga*0.3
vga=harga*0.4

kebutuhan = input("1. Produktivitas \t 2. Game : ")
if kebutuhan == "1" or kebutuhan=="produktivitas":
  for list_amd in list_processor:
    if processor >= list_amd[7]:
      print(f"Processor \t : {list_amd[1]} - {list_amd[7]}")

      for list_motherboard_amd in list_motherboard:
          if list_amd[2] == list_motherboard_amd[2]:
              if motherboard >= list_motherboard_amd[5]:
                  print(f"Motherboard \t : {list_motherboard_amd[1]} - {list_motherboard_amd[5]}")
                  break

if kebutuhan == "2" or kebutuhan=="game":
   print("belum ada data")




  



        









