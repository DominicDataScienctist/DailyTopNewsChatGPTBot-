1. Introduction
   Given that ChatGPT was trained with data from a cut-off date, with ChatGPT 4 at April, 2023 and ChatGPT 3.5 at Sept, 2021. To allow ChatGPT to talk about news. This repo is provides:

   i. A BeautifulSoup4 powered web scraper to get real time news articles from https://www.npr.org

   ii. ChatGPT bot that utilizes Langchain and ChatCompletion model that is back with updated knowledge acquired in i.
  
3. Set up the tool:
   i. git clone
   ii. cd ./DailyTopNewsChatGPTBot-
   iii. source venv/bin/activate

4. Collect new knowledge and run the chatbot:
   python daily_top_new_bot.py -p

5. To run the chatbot (without getting updated knowledge):
   ython daily_top_new_bot.py
   
6. Here is a quick demo of the chatbot, notice that the demo was recorded on Dec 1st of 2023 as of the date the Chatbot replied when asked about when its knowledge was based on:
   

https://github.com/DominicDataScienctist/DailyTopNewsChatGPTBot-/assets/8252308/06ad3f25-825e-4a2b-8981-eb2a80138ab6

