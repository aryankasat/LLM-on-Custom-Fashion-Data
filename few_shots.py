few_shots = [
    {'Question' : "How many t-shirts do we have left for Max in S size and grey color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE company = 'Max' AND color = 'Grey' AND size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "74"},
    {'Question': "How much is the total price of the inventory for all M-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'M'",
     'SQLResult': "Result of the SQL query",
     'Answer': "19015"},
    {'Question': "If we have to sell all the Wrogen’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where company = 'Wrogen'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': "17591.8"} ,
     {'Question' : "If we have to sell all the Shoppers Stop’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE company = 'Shoppers Stop'",
      'SQLResult': "Result of the SQL query",
      'Answer' : "19356"},
    {'Question': "How many orange color United Colors of Benetton's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE company = 'United Colors of Benetton' AND color = 'Orange'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "130"
     },
    {'Question': "how much sales amount will be generated if we sell all large size t shirts today in United Colors of Benetton brand after discounts?",
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where company = 'United Colors of Benetton' and size="L"
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer' : "6699.6"
    }
]