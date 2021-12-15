import psycopg2
# TEST
# conn = psycopg2.connect(host="cobra.cvc6fic9cofz.us-east-1.rds.amazonaws.com",
#                          database="cobra",
#                          user="postgres",
#                          password="cobra2021*")

# PROD
conn = psycopg2.connect(host="cobra.cvc6fic9cofz.us-east-1.rds.amazonaws.com",
                         database="cobra-prod",
                         user="postgres",
                         password="cobra2021*")

#DEV
# conn = psycopg2.connect(host="localhost",
#                          database="cobra",
#                          user="postgres",
#                          password="jacm1212")