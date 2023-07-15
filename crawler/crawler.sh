themeID=675
startPage=2 # should be greater than 1
endPage=101
# dir path not file name
output_path='/home/ryanzhang/crawler'
python  crawler.py \
    	      --themeID ${themeID} \
	      --startPage ${startPage} \
              --endPage ${endPage} \
              --output_path ${output_path}
