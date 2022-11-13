
import os
   
directory = '/home/murphylab/cellorganizer/local/images/Kush_thresh/oct12/'
# directory = '/home/kushagra/Documents/CMU_Internship/A2k22/Oct7/thresholds/individual_tiffs/'

images = ['p8', 'p24', 'p34', 'p52']

thresh = [['597', '703', '799', '905', '1000', '1096', '1202', '1297'], 
            ['602', '695', '799', '902', '1005', '1098', '1202', '1295'],  
            ['599', '701', '804', '897', '999', '1102', '1204', '1297'], 
            ['596', '703', '799', '896', '1003', '1100', '1197', '1304']]

obj = [[34, 36, 35, 34, 32, 30, 27, 24], [39, 42, 44, 39, 27, 23, 19, 12], 
        [39, 36, 34, 35, 34, 31, 31, 26], [40, 39, 38, 39, 37, 35, 31, 27]]

suffix =  [['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'], 
            ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
            ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
            ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']]

final_vector = []
for i in range(len(images)):
    str1 = images[i]+'/'

    for j in range(len(thresh[i])):
        str2 = images[i]+"_thresh_"+thresh[i][j]+"/"
        for k in range(1, obj[i][j]+1):
            str3 = 'o'+str(k)+"_"+images[i]+"_"+thresh[i][j]+suffix[i][j]+".tif"
            image_path = directory + str1 + str2 + str3
            final_vector.append(image_path)
            # if(os.path.exists(image_path)):
            #     final_vector.append(image_path)
            # else:
            #     print("MISTAKE!!!", image_path)

print(len(final_vector))
print(final_vector)
