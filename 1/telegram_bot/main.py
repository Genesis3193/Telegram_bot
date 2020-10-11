import telebot
import mysql.connector
TOKEN='1223802619:AAGQYp3gAqpj87r6liiXAXGD6tAyIXWQTJc'
bot=telebot.TeleBot(TOKEN)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="кщще",
  port="3306",
  database="telegram"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE  telegram") # при многократном запуске программы , все действия направленные на создание структуры бд следует закомментировать , после первного запуска
mycursor.execute("SHOW DATABASES")
mycursor.execute("CREATE TABLE general (task_name VARCHAR(255))")
mycursor.execute("ALTER TABLE general ADD COLUMN (user_id INT ,description VARCHAR(255))")
mycursor.execute("ALTER TABLE general ADD COLUMN (number INT AUTO_INCREMENT PRIMARY KEY )")



@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, "Привет, пользователь!")
    ident=int(message.from_user.id)



@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, "Я знаю следующие команды :\n/start-чтобы начать знакомство\n/new_item <Название задачи>\n/all-чтобы вывести все задачи\n/delete <Номер задачи>-чтобь удалить выбранную задачу\n/add <Название задачи> <Описание задачи>-чтобы добавить описание к выбранной задаче")

@bot.message_handler(commands=['new_item','...'])
def add_handler(message):
    strin=message.text
    ident = int(message.from_user.id)
    mes=strin[9:len(strin)-1]
    sql = "INSERT INTO general (task_name,user_id,description) VALUES (%s,%s,%s)"
    val = (mes,ident,"empty")
    mycursor.execute(sql, val)
    mydb.commit()
    bot.send_message(message.from_user.id,"Задание добавлено")

@bot.message_handler(commands=['all'])
def print_handler(message):
    ident = str(message.from_user.id)
    print(ident)
    sql="SELECT * FROM general WHERE user_id=%s"
    numb=(ident, )
    mycursor.execute(sql, numb)
    myresult=mycursor.fetchall()
    for x in myresult :
        bot.send_message(message.from_user.id,x[0]+','+x[2])




@bot.message_handler(commands=['delete','...'])
def delete_hadler(message):
    strin =message.text
    print(strin)
    ident = str(message.from_user.id)
    mes =str(strin[8:len(strin)] )
    print(mes)
    sql = "DELETE FROM general WHERE number = %s"
    val = (mes, )
    mycursor.execute(sql,val)
    mydb.commit()

    print(mycursor.rowcount, "record(s) deleted")
    bot.send_message(message.from_user.id, "Задание удалено")




@bot.message_handler(commands=['add','...','...'])
def adder_hadler(message):
    strin =str( message.text )
    print(strin)
    mes=strin.split()
    print(mes[2])
    print(mes[1])
    sql = "UPDATE general SET description = %s WHERE task_name = %s"
    val = (str(mes[2]), str(mes[1]))
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")
    bot.send_message(message.from_user.id, "Описание добавлено")



bot.polling()

