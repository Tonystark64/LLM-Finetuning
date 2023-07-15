themeID=675
startPage=2
endPage=101
# dir path not file path
output_path='/home/ryanzhang/crawler'
python  crawler.py \
    	      --themeID ${themeID} \
	      --startPage ${startPage} \
              --endPage ${endPage} \
              --output_path ${output_path}
