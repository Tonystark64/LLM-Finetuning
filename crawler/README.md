## Web Crawler based on Requests and Beautiful Soup  
### Usage  
>1. Open the [baby-kingdom](https://www.baby-kingdom.com/forum_home.php) page   
>2. Select the forum theme and note down the theme ID  
>3. Modify crawler.sh  
>4. Set theme ID, start page and end page (end page should not be larger than the final page of the theme!)  
>5. Set the folder path (not file name) where you want to save the results   
### Suggestion
>1. It is suggested to create tmux session to run the code, in case you need to terminate them   
>2. You may concurrently run two sessions using the same IP to increase the efficiency   
### Feature
>1. The result file will be updated every topic. So an exception would not cause a complete data loss
>2. If you want to know the entry number and time cost of each task, check result.csv
>3. Regular expression and Xpath is being used to accurately select and clean the collected data    
