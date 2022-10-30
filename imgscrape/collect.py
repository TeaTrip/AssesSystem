import re
import os
if __name__ == '__main__':
    # Using readline()
    file1 = open('html.txt', 'r')
    count = 0
    
    while True:
        count += 1
    
        # Get next line from file
        line = file1.readline()
    
        # if line is empty
        # end of file is reached
        if not line:
            break
        if '<span title="' in line:
            result = re.findall(r'".*"', line)
            result = result[0].replace("\"", "", 2)
            os.system('scrapy crawl img -a category={} -s GLOBAL_CATEGORY={}'.format(result, result))
            print("Line{}: {}".format(count, result))
        
    
    file1.close()
    