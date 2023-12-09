import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="python"
)

database = mydb.cursor()

database.execute("SELECT * FROM processor_amd")
list_processor_amd = database.fetchall()

database.execute("SELECT * FROM processor_intel")
list_processor_intel = database.fetchall()

database.execute("SELECT * FROM processor_igpu")
list_processor_igpu = database.fetchall()

database.execute("SELECT * FROM motherboard_amd")
list_motherboard_amd = database.fetchall()

database.execute("SELECT * FROM motherboard_intel")
list_motherboard_intel = database.fetchall()

database.execute("SELECT * FROM vga_amd")
list_vga_amd = database.fetchall()

database.execute("SELECT * FROM vga_nvidia")
list_vga_nvidia = database.fetchall()

database.execute("SELECT * FROM ram")
list_ram = database.fetchall()

database.execute("SELECT * FROM ssd")
list_ssd = database.fetchall()

database.execute("SELECT * FROM psu")
list_psu = database.fetchall()

database.execute("SELECT * FROM casing")
list_casing = database.fetchall()

harga = int(input("Masukkan Harga : "))
harga_baru = harga-1250000 #250 ram, 150 ssd, 500 psu, 350 casing
processor = harga_baru*0.3
motherboard = harga_baru*0.3
vga = harga_baru*0.4

# mencari nilai tertinggi
#lamun mencari nilai max float meh gampang make sintax phpna <= %s (place holder) diganti sama nilai proci
database.execute("SELECT MAX(Score_Produktivitas) AS Max_Score FROM processor_amd WHERE Harga <= %s", (processor,))
max_score_produktivitas = database.fetchone()[0]

database.execute("SELECT MAX(Score_Produktivitas) AS Max_Score FROM processor_intel WHERE Harga <= %s", (processor,))
max_score_produktivitas1 = database.fetchone()[0]


#(nama kolom) AS variabel from tabel
database.execute("SELECT MAX(Score_Game) AS Max_Score FROM processor_amd WHERE Harga <= %s", (processor,))
max_score_game= database.fetchone()[0]

database.execute("SELECT MAX(Score_Game) AS Max_Score FROM processor_intel WHERE Harga <= %s", (processor,))
max_score_game1 = database.fetchone()[0]




kebutuhan = input("1. Produktivitas \t 2. Game : ")
jenis_processor = input("Mau Processor Apa ? \n1. AMD \t 2. Intel \t 3. Tidak: ")
if(jenis_processor == "3" or jenis_processor == "tidak"):
  if kebutuhan == "1" or kebutuhan=="produktivitas":
  # ==============================================================AMD Proci + VGA AMD ===============================================================================
    # variabel kajeng nentuken procina kapanggih hantena
    found_processor = False
    found_motherboard = False
    found_vga = False

    #===================================================== Cari Proci ================================================================================
    for list_amd in list_processor_amd:
      #cari proci berdasarkan harga
      if processor >= list_amd[7]:
        
        #cari proci berdasarkan score
        score_proci = float(list_amd[4])

        if score_proci >= max_score_produktivitas:
          print(f"Processor \t : {list_amd[1]} - {list_amd[7]}")
          # lamun kapanggih set ka true
          found_processor = True

          #============================================================= Cari Mobo ===================================================================
          #Harga tambahan untuk sisa proci ditambahin ke motherboard
          harga_tambahan = processor - list_amd[7]
          harga_motherboard = motherboard + harga_tambahan
          
          for motherboard_amd in list_motherboard_amd:
              # cari soket yang sama
              if list_amd[2] == motherboard_amd[2]:
                  #filter berdasarkan harga
                  if harga_motherboard >= motherboard_amd[5]:
                    # filter dengan harga tertinggi dan soket yang sesuai
                    database.execute("SELECT * FROM motherboard_amd WHERE Soket = %s AND Harga <= %s", (list_amd[2], harga_motherboard))
                    list_motherboard = database.fetchall()
                    
                    # masukkan harga tertinggi ke dalam variabel
                    max_harga_motherboard = max([mb[5] for mb in list_motherboard], default=0)

                    # lalu cari harga tertingginya
                    if max_harga_motherboard == motherboard_amd[5]:             
                      print(f"Motherboard \t : {motherboard_amd[1]} - {motherboard_amd[5]}")
                      found_motherboard = True

                      #============================================================= Cari VGA ===================================================================
                      #harga tambahan dari sisa mobo untuk vga
                      harga_tambahan_1 = harga_motherboard - motherboard_amd[5]
                      harga_vga = vga + harga_tambahan_1

                      for list_amd_vga in list_vga_amd:
                        if harga_vga >= list_amd_vga[3]:

                            database.execute("SELECT MAX(Harga) AS Max_Harga FROM vga_amd WHERE Harga <= %s", (harga_vga,))
                            max_harga_vga = database.fetchone()[0]

                            if max_harga_vga == list_amd_vga[3]:             
                              print(f"VGA \t\t : {list_amd_vga[1]} - {list_amd_vga[3]}")
                              found_vga = True

                              #================================================= Cari sisa komponen =============================================================
                              #RAM
                              for ram in list_ram:
                                if motherboard_amd[3] == ram[2]:
                                    if ram[5] == 250000:
                                      print(f"RAM \t\t : {ram[1]} - {ram[5]}")
                              #SSD
                              for ssd in list_ssd:
                                if ssd[4] == 150000:
                                  print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                              #PSU
                              for psu in list_psu:
                                if psu[4] == 500000:
                                  print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                              #Casing
                              for casing in list_casing:
                                if casing[3] == 350000:
                                  print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")
                                
                              harga_sisa = harga_baru - list_amd[7] - motherboard_amd[5] - list_amd_vga[3]
                              print(f"Sisa Uang\t : {harga_sisa}")

                              print(f"Score Produktivitas Processor : {score_proci}")


                              
                      if not found_vga:
                        print("Maaf, data vga tidak ditemukan.")
                            
          if not found_motherboard:
            print("Maaf, data motherboard tidak ditemukan.")

    if not found_processor:
      print("Maaf, data processor tidak ditemukan.")


  # # ========================================================Intel Proci + VGA Nvidia ============================================================================
    #===================================================== Cari Proci ================================================================================
    found_processor = False
    found_motherboard = False            

    for list_intel in list_processor_intel:
      #cari proci berdasarkan harga
      if processor >= list_intel[7]:
        
        #cari proci berdasarkan score
        score_proci = float(list_intel[4])

        if score_proci >= max_score_produktivitas1:
          print(f"\n\nProcessor \t : {list_intel[1]} - {list_intel[7]}")
          found_processor = True

          #============================================================= Cari Mobo ===================================================================
          #Harga tambahan untuk sisa proci ditambahin ke motherboard
          harga_tambahan = processor - list_intel[7]
          harga_motherboard = motherboard + harga_tambahan
          
          for motherboard_intel in list_motherboard_intel:
              # cari soket yang sama
              if list_intel[2] == motherboard_intel[2]:
                  #filter berdasarkan harga
                  if harga_motherboard >= motherboard_intel[5]:
                    # filter dengan harga tertinggi dan soket yang sesuai
                    database.execute("SELECT * FROM motherboard_intel WHERE Soket = %s AND Harga <= %s", (list_intel[2], harga_motherboard))
                    list_motherboard = database.fetchall()

                    # masukkan harga tertinggi ke dalam variabel
                    max_harga_motherboard = max([mb[5] for mb in list_motherboard], default=0)

                    # lalu cari harga tertingginya
                    if max_harga_motherboard == motherboard_intel[5]:             
                      print(f"Motherboard \t : {motherboard_intel[1]} - {motherboard_intel[5]}")
                      found_motherboard = True

                      #============================================================= Cari VGA ===================================================================
                      #harga tambahan dari sisa mobo untuk vga
                      harga_tambahan_1 = harga_motherboard - motherboard_intel[5]
                      harga_vga = vga + harga_tambahan_1

                      for list_nvidia_vga in list_vga_nvidia:
                        if harga_vga >= list_nvidia_vga[3]:

                            database.execute("SELECT MAX(Harga) AS Max_Harga FROM vga_nvidia WHERE Harga <= %s", (harga_vga,))
                            max_harga_vga = database.fetchone()[0]

                            if max_harga_vga == list_nvidia_vga[3]:             
                              print(f"VGA \t\t : {list_nvidia_vga[1]} - {list_nvidia_vga[3]}")
                              found_vga = True

                              #================================================= Cari sisa komponen =============================================================
                              #RAM
                              for ram in list_ram:
                                if motherboard_intel[3] == ram[2]:
                                    if ram[5] == 250000:
                                      print(f"RAM \t\t : {ram[1]} - {ram[5]}")
                              #SSD
                              for ssd in list_ssd:
                                if ssd[4] == 150000:
                                  print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                              #PSU
                              for psu in list_psu:
                                if psu[4] == 500000:
                                  print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                              #Casing
                              for casing in list_casing:
                                if casing[3] == 350000:
                                  print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")
                                
                              harga_sisa = harga_baru - list_intel[7] - motherboard_intel[5] - list_nvidia_vga[3]
                              print(f"Sisa Uang\t : {harga_sisa}")

                              print(f"Score Produktivitas Processor : {score_proci}")
    
                      if not found_vga:
                        print("Maaf, data vga tidak ditemukan.")
          if not found_motherboard:
            print("Maaf, data motherboard tidak ditemukan.")
    if not found_processor:
      print("\n\nMaaf, data processor tidak ditemukan.")

  # ========================================================Proci + IGPU ============================================================================
    #===================================================== Cari Proci ================================================================================
    processor = harga_baru*0.5
    motherboard = harga_baru*0.5

    found_processor = False
    found_motherboard = False           

    database.execute("SELECT MAX(Score_Produktivitas) AS Max_Score FROM processor_igpu WHERE Harga <= %s", (processor,))
    max_score_produktivitas2 = database.fetchone()[0] 

    for list_igpu in list_processor_igpu:
      #cari proci berdasarkan harga
      if processor >= list_igpu[9]:
        
        #cari proci berdasarkan score
        score_proci = float(list_igpu[5])
        score_igpu = list_igpu[7]

        #cari dulu score gpunya (logika salah)
        if score_proci >= max_score_produktivitas2:      
          print(f"\n\nProcessor \t : {list_igpu[1]} - {list_igpu[9]}")
          found_processor = True

          #===================================================== Cari Mobo ================================================================================
          #Harga tambahan untuk sisa proci ditambahin ke motherboard
          harga_tambahan = processor - list_igpu[9]
          harga_motherboard = motherboard + harga_tambahan

          for motherboard_amd in list_motherboard_amd:
            # cari soket yang sama
            if list_igpu[2] == motherboard_amd[2]:
              #filter berdasarkan harga
              if harga_motherboard >= motherboard_amd[5] :
                # filter dengan harga tertinggi dan soket yang sesuai
                database.execute("SELECT * FROM motherboard_amd WHERE Soket = %s AND Harga <= %s", (list_igpu[2], harga_motherboard))
                list_motherboard_amd = database.fetchall()
                    
                # masukkan harga tertinggi ke dalam variabel
                max_harga_motherboard_amd = max([mb[5] for mb in list_motherboard_amd], default=0)
                      
                # lalu cari harga tertingginya
                if max_harga_motherboard_amd == motherboard_amd[5]:              
                  print(f"Motherboard \t : {motherboard_amd[1]} - {motherboard_amd[5]}")
                  found_motherboard = True

          #================================================= Cari sisa komponen =============================================================
                  for ram in list_ram:
                    if motherboard_amd[3] == ram[2]:
                      if ram[5] == 250000:
                        print(f"RAM \t\t : {ram[1]} - {ram[5]}")

                  #SSD
                  for ssd in list_ssd:
                    if ssd[4] == 150000:
                      print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                  #PSU
                  for psu in list_psu:
                    if psu[4] == 500000:
                      print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                  #Casing
                  for casing in list_casing:
                    if casing[3] == 350000:
                      print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")
                  
                  harga_sisa = harga_baru - list_igpu[9] - motherboard_amd[5]
                  print(f"Sisa Uang\t : {harga_sisa}")

                      
          for motherboard_intel in list_motherboard_intel:
            if list_igpu[2] == motherboard_intel[2] :
              #filter berdasarkan harga
              if harga_motherboard >= motherboard_intel[5] :
                # filter dengan harga tertinggi dan soket yang sesuai
                database.execute("SELECT * FROM motherboard_intel WHERE Soket = %s AND Harga <= %s", (list_igpu[2], harga_motherboard))
                list_motherboard_intel = database.fetchall()

                # masukkan harga tertinggi ke dalam variabel
                max_harga_motherboard_intel = max([mb[5] for mb in list_motherboard_intel], default=0)

                # lalu cari harga tertingginya
                if max_harga_motherboard_intel == motherboard_intel[5]:
                  print(f"Motherboard \t : {motherboard_intel[1]} - {motherboard_intel[5]}")
                  found_motherboard = True

                  
          #================================================= Cari sisa komponen =============================================================
                  #RAM
                  for ram in list_ram:
                    if motherboard_intel[3] == ram[2]:
                      if ram[5] == 250000:
                        print(f"RAM \t\t : {ram[1]} - {ram[5]}")
                  #SSD
                  for ssd in list_ssd:
                    if ssd[4] == 150000:
                      print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                  #PSU
                  for psu in list_psu:
                    if psu[4] == 500000:
                      print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                  #Casing
                  for casing in list_casing:
                    if casing[3] == 350000:
                      print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")

                  harga_sisa = harga_baru - list_igpu[9] - motherboard_intel[5]
                  print(f"Sisa Uang \t: {harga_sisa}")

          print(f"Score Produktivitas Processor + IGPU : {score_proci}")

          if not found_motherboard:
            print("Maaf, data motherboard tidak ditemukan.")
    if not found_processor:
      print("\n\nMaaf, data processor tidak ditemukan.")


#===============================================================GAME===================================================================

  if kebutuhan == "2" or kebutuhan=="game":
    # ==============================================================AMD Proci + VGA AMD ===============================================================================
    # variabel kajeng nentuken procina kapanggih hantena
    found_processor = False
    found_motherboard = False
    found_vga = False

    #===================================================== Cari Proci ================================================================================
    for list_amd in list_processor_amd:
      #cari proci berdasarkan harga
      if processor >= list_amd[7]:
        
        #cari proci berdasarkan score
        score_proci = float(list_amd[5])

        if score_proci >= max_score_game:
          print(f"Processor \t : {list_amd[1]} - {list_amd[7]}")
          # lamun kapanggih set ka true
          found_processor = True

          #============================================================= Cari Mobo ===================================================================
          #Harga tambahan untuk sisa proci ditambahin ke motherboard
          harga_tambahan = processor - list_amd[7]
          harga_motherboard = motherboard + harga_tambahan
          
          for motherboard_amd in list_motherboard_amd:
              # cari soket yang sama
              if list_amd[2] == motherboard_amd[2]:
                  #filter berdasarkan harga
                  if harga_motherboard >= motherboard_amd[5]:
                    # filter dengan harga tertinggi dan soket yang sesuai
                    database.execute("SELECT * FROM motherboard_amd WHERE Soket = %s AND Harga <= %s", (list_amd[2], harga_motherboard))
                    list_motherboard = database.fetchall()
                    
                    # masukkan harga tertinggi ke dalam variabel
                    max_harga_motherboard = max([mb[5] for mb in list_motherboard], default=0)

                    # lalu cari harga tertingginya
                    if max_harga_motherboard == motherboard_amd[5]:             
                      print(f"Motherboard \t : {motherboard_amd[1]} - {motherboard_amd[5]}")
                      found_motherboard = True

                      #============================================================= Cari VGA ===================================================================
                      #harga tambahan dari sisa mobo untuk vga
                      harga_tambahan_1 = harga_motherboard - motherboard_amd[5]
                      harga_vga = vga + harga_tambahan_1

                      for list_amd_vga in list_vga_amd:
                        if harga_vga >= list_amd_vga[3]:

                            database.execute("SELECT MAX(Harga) AS Max_Harga FROM vga_amd WHERE Harga <= %s", (harga_vga,))
                            max_harga_vga = database.fetchone()[0]

                            if max_harga_vga == list_amd_vga[3]:             
                              print(f"VGA \t\t : {list_amd_vga[1]} - {list_amd_vga[3]}")
                              found_vga = True

                              #================================================= Cari sisa komponen =============================================================
                              #RAM
                              for ram in list_ram:
                                if motherboard_amd[3] == ram[2]:
                                    if ram[5] == 250000:
                                      print(f"RAM \t\t : {ram[1]} - {ram[5]}")
                              #SSD
                              for ssd in list_ssd:
                                if ssd[4] == 150000:
                                  print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                              #PSU
                              for psu in list_psu:
                                if psu[4] == 500000:
                                  print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                              #Casing
                              for casing in list_casing:
                                if casing[3] == 350000:
                                  print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")
                                
                              harga_sisa = harga_baru - list_amd[7] - motherboard_amd[5] - list_amd_vga[3]
                              print(f"Sisa Uang\t : {harga_sisa}")

                              print(f"Score Game Processor : {score_proci}")


                              
                      if not found_vga:
                        print("Maaf, data vga tidak ditemukan.")
                            
          if not found_motherboard:
            print("Maaf, data motherboard tidak ditemukan.")

    if not found_processor:
      print("Maaf, data processor tidak ditemukan.")


  # # ========================================================Intel Proci + VGA Nvidia ============================================================================
    #===================================================== Cari Proci ================================================================================
    found_processor = False
    found_motherboard = False            

    for list_intel in list_processor_intel:
      #cari proci berdasarkan harga
      if processor >= list_intel[7]:
        
        #cari proci berdasarkan score
        score_proci = float(list_intel[5])

        if score_proci >= max_score_game1:
          print(f"\n\nProcessor \t : {list_intel[1]} - {list_intel[7]}")
          found_processor = True

          #============================================================= Cari Mobo ===================================================================
          #Harga tambahan untuk sisa proci ditambahin ke motherboard
          harga_tambahan = processor - list_intel[7]
          harga_motherboard = motherboard + harga_tambahan
          
          for motherboard_intel in list_motherboard_intel:
              # cari soket yang sama
              if list_intel[2] == motherboard_intel[2]:
                  #filter berdasarkan harga
                  if harga_motherboard >= motherboard_intel[5]:
                    # filter dengan harga tertinggi dan soket yang sesuai
                    database.execute("SELECT * FROM motherboard_intel WHERE Soket = %s AND Harga <= %s", (list_intel[2], harga_motherboard))
                    list_motherboard = database.fetchall()

                    # masukkan harga tertinggi ke dalam variabel
                    max_harga_motherboard = max([mb[5] for mb in list_motherboard], default=0)

                    # lalu cari harga tertingginya
                    if max_harga_motherboard == motherboard_intel[5]:             
                      print(f"Motherboard \t : {motherboard_intel[1]} - {motherboard_intel[5]}")
                      found_motherboard = True

                      #============================================================= Cari VGA ===================================================================
                      #harga tambahan dari sisa mobo untuk vga
                      harga_tambahan_1 = harga_motherboard - motherboard_intel[5]
                      harga_vga = vga + harga_tambahan_1

                      for list_nvidia_vga in list_vga_nvidia:
                        if harga_vga >= list_nvidia_vga[3]:

                            database.execute("SELECT MAX(Harga) AS Max_Harga FROM vga_nvidia WHERE Harga <= %s", (harga_vga,))
                            max_harga_vga = database.fetchone()[0]

                            if max_harga_vga == list_nvidia_vga[3]:             
                              print(f"VGA \t\t : {list_nvidia_vga[1]} - {list_nvidia_vga[3]}")
                              found_vga = True

                              #================================================= Cari sisa komponen =============================================================
                              #RAM
                              for ram in list_ram:
                                if motherboard_intel[3] == ram[2]:
                                    if ram[5] == 250000:
                                      print(f"RAM \t\t : {ram[1]} - {ram[5]}")
                              #SSD
                              for ssd in list_ssd:
                                if ssd[4] == 150000:
                                  print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                              #PSU
                              for psu in list_psu:
                                if psu[4] == 500000:
                                  print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                              #Casing
                              for casing in list_casing:
                                if casing[3] == 350000:
                                  print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")
                                
                              harga_sisa = harga_baru - list_intel[7] - motherboard_intel[5] - list_nvidia_vga[3]
                              print(f"Sisa Uang\t : {harga_sisa}")

                              print(f"Score Game Processor : {score_proci}")
    
                      if not found_vga:
                        print("Maaf, data vga tidak ditemukan.")
          if not found_motherboard:
            print("Maaf, data motherboard tidak ditemukan.")
    if not found_processor:
      print("\n\nMaaf, data processor tidak ditemukan.")

  # ========================================================Proci + IGPU ============================================================================
    #===================================================== Cari Proci ================================================================================
    processor = harga_baru*0.5
    motherboard = harga_baru*0.5

    found_processor = False
    found_motherboard = False           

    database.execute("SELECT MAX(Score_Game) AS Max_Score FROM processor_igpu WHERE Harga <= %s", (processor,))
    max_score_game2 = database.fetchone()[0] 

    for list_igpu in list_processor_igpu:
      #cari proci berdasarkan harga
      if processor >= list_igpu[9]:
        
        #cari proci berdasarkan score
        score_proci = float(list_igpu[6])
        score_igpu = list_igpu[7]

        #cari dulu score gpunya (logika salah)
        if score_proci >= max_score_game2:      
          print(f"\n\nProcessor \t : {list_igpu[1]} - {list_igpu[9]}")
          found_processor = True

          #===================================================== Cari Mobo ================================================================================
          #Harga tambahan untuk sisa proci ditambahin ke motherboard
          harga_tambahan = processor - list_igpu[9]
          harga_motherboard = motherboard + harga_tambahan

          for motherboard_amd in list_motherboard_amd:
            # cari soket yang sama
            if list_igpu[2] == motherboard_amd[2]:
              #filter berdasarkan harga
              if harga_motherboard >= motherboard_amd[5] :
                # filter dengan harga tertinggi dan soket yang sesuai
                database.execute("SELECT * FROM motherboard_amd WHERE Soket = %s AND Harga <= %s", (list_igpu[2], harga_motherboard))
                list_motherboard_amd = database.fetchall()
                    
                # masukkan harga tertinggi ke dalam variabel
                max_harga_motherboard_amd = max([mb[5] for mb in list_motherboard_amd], default=0)
                      
                # lalu cari harga tertingginya
                if max_harga_motherboard_amd == motherboard_amd[5]:              
                  print(f"Motherboard \t : {motherboard_amd[1]} - {motherboard_amd[5]}")
                  found_motherboard = True

          #================================================= Cari sisa komponen =============================================================
                  for ram in list_ram:
                    if motherboard_amd[3] == ram[2]:
                      if ram[5] == 250000:
                        print(f"RAM \t\t : {ram[1]} - {ram[5]}")

                  #SSD
                  for ssd in list_ssd:
                    if ssd[4] == 150000:
                      print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                  #PSU
                  for psu in list_psu:
                    if psu[4] == 500000:
                      print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                  #Casing
                  for casing in list_casing:
                    if casing[3] == 350000:
                      print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")
                  
                  harga_sisa = harga_baru - list_igpu[9] - motherboard_amd[5]
                  print(f"Sisa Uang\t : {harga_sisa}")

                      
          for motherboard_intel in list_motherboard_intel:
            if list_igpu[2] == motherboard_intel[2] :
              #filter berdasarkan harga
              if harga_motherboard >= motherboard_intel[5] :
                # filter dengan harga tertinggi dan soket yang sesuai
                database.execute("SELECT * FROM motherboard_intel WHERE Soket = %s AND Harga <= %s", (list_igpu[2], harga_motherboard))
                list_motherboard_intel = database.fetchall()

                # masukkan harga tertinggi ke dalam variabel
                max_harga_motherboard_intel = max([mb[5] for mb in list_motherboard_intel], default=0)

                # lalu cari harga tertingginya
                if max_harga_motherboard_intel == motherboard_intel[5]:
                  print(f"Motherboard \t : {motherboard_intel[1]} - {motherboard_intel[5]}")
                  found_motherboard = True

                  
          #================================================= Cari sisa komponen =============================================================
                  #RAM
                  for ram in list_ram:
                    if motherboard_intel[3] == ram[2]:
                      if ram[5] == 250000:
                        print(f"RAM \t\t : {ram[1]} - {ram[5]}")
                  #SSD
                  for ssd in list_ssd:
                    if ssd[4] == 150000:
                      print(f"SSD \t\t : {ssd[1]} - {ssd[4]}")
                  #PSU
                  for psu in list_psu:
                    if psu[4] == 500000:
                      print(f"PSU \t\t : {psu[1]} - {psu[2]} - {psu[4]}")
                  #Casing
                  for casing in list_casing:
                    if casing[3] == 350000:
                      print(f"CASING \t\t : {casing[1]} - {casing[2]} - {casing[3]}")

                  harga_sisa = harga_baru - list_igpu[9] - motherboard_intel[5]
                  print(f"Sisa Uang \t: {harga_sisa}")

          print(f"Score Game Processor + IGPU : {score_proci}")

          if not found_motherboard:
            print("Maaf, data motherboard tidak ditemukan.")
    if not found_processor:
      print("\n\nMaaf, data processor tidak ditemukan.")
   




  



        









