# LLM-on-Custom-Fashion-Data


## Installation and Usage

1. Clone the repository to the local machine:
```
git clone https://github.com/aryankasat/LLM-on-Custom-Fashion-Data.git
```
2. Navigate to the project directory:
```
cd LLM-on-Custom_Fashion-Data
```
3. Install the required dependencies using pip:
```
pip install -r requirements.txt 
```
4. Acquire an api key through makersuite.google.com and put in .env file
```
GOOGLE_API_KEY = "your_api_key"
```
5. For Database setup, run the commands in .sql file.
6. Run the application
```
streamlit run main.py
```

## Project Outcomes

* As the app starts running, you will be directed to the main page, from where you can toggle to the page of your choice for either RAG based query or Database querying.
* Once you navigate to the Database UI page, you will just have to input your question in plain english and it will give the output along with query used in the database.
* If you navigate to the Internet RAG UI page, you will have to input the URLs you want to fetch information from and to the question to query, after which the model will generate the required output after taking reference from the web-pages whose URLs have been provided.

## File Structure

* data_storage.sql - Building of a schema and tables in a SQL database
* database_query.py - Code to generate query and use to query the database
* few_shots.py - Consists of list of few shot prompts to enhance the LLM models
* internet_query.py - Used to the generate the answer for the question asked from the web-page URLs provided
* main.py - used to generate the main page of the UI from where we can navigate to other pages as well
* pages - Contains the UI for other two pages
    * database_ui.py - Contains the UI for the querying of database in plain english
    * internet_rag_ui.py - Contains the  UI for the RAG based outputs as well as used for chunking of data from the urls

## Output Demo
https://github.com/aryankasat/LLM-on-Custom-Fashion-Data/assets/33005008/2712f021-6505-4fe3-a891-55ca45a4390b
