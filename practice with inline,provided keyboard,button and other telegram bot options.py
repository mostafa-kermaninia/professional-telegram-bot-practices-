from enum import Enum , auto
from telethon import TelegramClient , events , Button
from specs import id , hash , token 
import asyncio
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["telegram"]
names = db["users name"]
ages = db['users ages']

class State(Enum):
    state1 = 'name'
    state2 = 'age'
    
conversation_state = {}

class Loggerbot :
    
    def __init__(self, api_id : int , api_hash : str , token : str) :
        self.bot = TelegramClient('bot' , api_id , api_hash)
        self.token = token
        self.bot.add_event_handler(self.message_handler , events.NewMessage)
        self.bot.add_event_handler(self.query_handler , events.CallbackQuery)

    async def asyncInit(self) :
        await self.bot.start(bot_token = self.token)
        
    async def message_handler(self , event : events.NewMessage) :
        
        who = event.chat_id
        state = conversation_state.get(who)
         
        if event.text == '/start' :
            Buttons = [
                [Button.text('ثبت نام' , resize = True)] ,
                [Button.text('مشخصات من' , single_use = True) , Button.text('نوموخوام' , single_use = True)]
            ]       
            await self.bot.send_message(entity = event.chat_id , message = 'سلام !يه دكمه انتخاب كن' , reply_to = event , buttons = Buttons ) 
        #sign in function----------------------------------------------------------------------------
        elif event.text == 'ثبت نام' or event.text == '/sign_up_again' :
            if names.find_one({'user_id' : who}) != None and ages.find_one({'user_id' : who})['age'] != None :
                Buttons = [
                    [Button.inline(' پاكسازي اطلاعات قبلي',data = '1')]
                ]    
                await self.bot.send_message(entity = event.chat_id , message = 'قبلا ثبت نام كرديا!' , reply_to = event , buttons = Buttons)              
           
            else :    
                if state is None :
                    await self.bot.send_message(entity = event.chat_id , message = 'اسمت  چيه؟' , reply_to = event )              
                    conversation_state[who] = State.state1  
                                
        elif state == State.state1 :
            name = event.text 
            await self.bot.send_message(entity = event.chat_id , message = f'به به به اقا {name} گل !  \n  چن سالته حالا ؟' , reply_to = event )               
            conversation_state[who] = State.state2
            
            my_dict = {'user_id' : who , 'name' : name}
            names.insert_one(my_dict)

        elif state == State.state2:
            age = event.text 
            await self.bot.send_message(entity = event.chat_id , message = f'ثبت نام شما انجام شد،ميتوانيد در بخش \n /my_info \n اطلاعات كاربري خود را ببينيد' , reply_to = event )               
            del conversation_state[who]
            
            my_dict = {'user_id' : who , 'age' : age}
            ages.insert_one(my_dict)

        #-------------------------------------------------------------------------------------------


        elif event.text == 'مشخصات من' or event.text == '/my_info' : 
            name = names.find_one({'user_id' : who})['name']  
            age = ages.find_one({'user_id' : who})['age']  

            if name != None and age != None :
                 await self.bot.send_message(entity = event.chat_id , message = f'اسم : {name} \n سن : {age}' , reply_to = event ) 
            else :
                 await self.bot.send_message(entity = event.chat_id , message = 'لطفا اول ثبت نام كنيد' , reply_to = event ) 
   
    async def query_handler(self , event : events.CallbackQuery) :
        
        if event.data.decode() == '1' :
            await event.answer('چشم،حتما!')
            
            old_name = names.find_one({'user_id' : event.sender_id})
            names.delete_one(old_name)
            old_age = ages.find_one({'user_id' : event.sender_id})
            ages.delete_one(old_age)
           
            await self.bot.send_message(entity = event.chat_id , message = 'اطلاعات قبلي شما با موفقيت پاك شدند، براي ثبت نام مجدد روي \n /sign_up_again \n  كليك كنيد' ) 
            
           

           
async def run():
    bot = Loggerbot(id , hash , token)
    await bot.asyncInit()
    
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()
loop.create_task(run())
loop.run_forever()    