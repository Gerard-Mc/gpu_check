import re

#Check if the string starts with "The" and ends with "Spain":

steam = "<strong>Минимальные:</strong><br><ul class=><li>Требуются 64-разрядные процессор и операционная система<br></li><li><strong>ОС:</strong> Windows 7 or 10<br></li><li><strong>Процессор:</strong> Intel Core i5-3570K or AMD FX-8310<br></li><li><strong>Оперативная память:</strong> 8 GB ОЗУ<br></li><li><strong>Видеокарта:</strong> NVIDIA GeForce GTX 780 or AMD Radeon RX 470<br></li><li><strong>DirectX:</strong> Версии 12<br></li><li><strong>Место на диске:</strong> 70 GB<br></li><li><strong>Дополнительно:</strong> In this game you will encounter a variety of visual effects that may provide seizures or loss of consciousness in a minority of people. If you or someone you know experiences any of the above symptoms while playing, stop and seek medical attention immediately.</li></ul>"


find_title_is_graphics = re.search("(?<=Graphics:).+", steam)
find_title_is_video = re.search("(?<=Video:).+", steam)
find_title_is_russian = re.search("(?<=Видеокарта:).+", steam)
long_requirements = []

if find_title_is_graphics:
	long_requirements = re.findall("(?<=Graphics:).+", steam)
elif find_title_is_video:
	long_requirements = re.findall("(?<=Video:).+", steam)
elif find_title_is_russian:
	long_requirements = re.findall("(?<=Видеокарта:).+", steam)  
else:
	print("We don't have this game on our database.")
# Tidy Steam requirements input    
shorten_requirements = re.findall("(.*?)<\/li>",long_requirements[0])  
remove_words = re.sub("(?i)nvidia\s?|amd\s?|series\s?|or\s", "", shorten_requirements[0])
gpu_requirements = remove_words

# Find old gpus under 1GB
old_gpu = re.search("\d+MB|\d+\sMB", gpu_requirements)
# Find old Geforce and ATI/Radeon GPUs
old_geforce_radeon_gpu = re.findall('(\s[A-Za-z]+\s\d{2,5}\s?[A-Za-z]{0,2}\s)', gpu_requirements)
# Find intel integrated graphics
intel_gpu = re.findall('(?i)intel\shd\s\d+[A-Za-z]{0,2}', gpu_requirements)
# Find radeon hd 
radeon_hd = re.findall('(?i)radeon?\s?hd+\s\d+[A-Za-z]{0,1}\s', gpu_requirements)
# Find geforce gtx
gtx_gpu = re.findall('(?i)geforce\s[A-Za-z]+\s\d+\s?[A-Za-z]{0,3}\s', gpu_requirements)
print(old_gpu)
print(old_geforce_radeon_gpu)
print(radeon_hd)
print(intel_gpu)
print(gtx_gpu)



# Fix Steam AMD/ATI naming inconsistencies to align with the app's database
    # Eg. ATI Radeon X1900 -> Radeon X1900 
    find_number_gtx =re.findall('(?i)(?:mobility|ati)\s?radeon?\s?[A-za-z]\d+', gpu_requirements)
    for i in find_number_gtx:
            i = re.sub("(?i)ATI", "", i) 
            i = re.sub("^\s",  "", i)
            i = re.sub("\s\s$",  "", i)
            i = re.sub("\s$",  "", i)
            i = re.sub("  ",  " ", i)
            number_gtx.append(i)