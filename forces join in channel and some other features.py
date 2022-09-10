from telethon import TelegramClient , events , Button , functions , errors
from specs import id , hash , token , channel
import asyncio
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test_bot"]
Accounts_col = db["UserAccounts"]


class Loggerbot :
    
    def __init__(self, api_id : int , api_hash : str , token : str) :
        self.bot = TelegramClient('bot' , api_id , api_hash)
        self.token = token
        self.bot.add_event_handler(self.main , events.NewMessage)
        self.bot.add_event_handler(self.inline_handler, events.CallbackQuery)        
        
    async def asyncInit(self) :
        await self.bot.start(bot_token = self.token)
        
            
    async def main(self , event : events.NewMessage) : 
        
        try :  
            sender_id = event.from_id.user_id
            group_id = event.message.peer_id.channel_id

            
            if event.text == '/sign_up@mosiyo_test_bot' :
                
                if Accounts_col.find_one({'sender_id' : sender_id}) == None :    
                        
                    sign_info = {'sender_id' : sender_id ,'Access level' : 0 , 'is in group' : True , 'group id' : group_id }
                    Accounts_col.insert_one(sign_info)
                    Buttons = [
                        [Button.text('button1' , resize = True , single_use = True , selective = True ) , Button.text('button2')],
                        [Button.text('help')]
                        ]     
                    await self.bot.send_message(entity = event.chat_id , message= '.انجام شد!حالا دكمه ي مدنظر را انتخاب كنيد' , reply_to = event , buttons = Buttons ) 
                                                
                else :
                    await self.bot.send_message(entity = event.chat_id , message= 'شما قبلا حساب كاربري ايجاد كرده ايد' , reply_to = event ) 
            elif event.text == '/status@mosiyo_test_bot' :
                await self.bot.send_message(entity = event.chat_id , message= 'براي استفاده از اين دستور بطور شخصي به ربات پيام دهيد' , reply_to = event ) 
                
               
        except AttributeError :
            sender_id = int(event.peer_id.user_id)
            
            try :
                await self.bot(functions.channels.GetParticipantRequest(channel = channel , participant = sender_id))
                        
                if event.text == '/start' :
                    await self.bot.send_message(entity = event.chat_id , message = 'سلام!،يه كامند رو انتخاب كن' , reply_to = event ) 

                elif event.text == '/sign_up' :
                    
                    if Accounts_col.find_one({'sender_id' : sender_id}) == None :  
                                    
                        sign_info = {'sender_id' : sender_id ,'Access level' : 0 , 'is in group' : False , 'group id' : None }
                        Accounts_col.insert_one(sign_info)
                    
                        Buttons = [
                        [Button.text('button1' , resize = True , single_use = True , selective = True ) , Button.text('button2')],
                        [Button.text('help')]
                        ]     
                        await self.bot.send_message(entity = event.chat_id , message= '.انجام شد!حالا دكمه ي مدنظر را انتخاب كنيد' , reply_to = event , buttons = Buttons ) 
                    
                    else :
                        await self.bot.send_message(entity = event.chat_id , message= 'شما قبلا حساب كاربري ايجاد كرده ايد' , reply_to = event ) 


                elif event.text == '/status' :
                    Buttons = [
                        [Button.text('استعلام وضعيت' , resize = True)] ,
                        [Button.text('خريد اشتراك سطح 1' , single_use = True) , Button.text('خريد اشتراك سطح 2' , single_use = True)\
                            , Button.text('خريد اشتراك سطح 3' , single_use = True)]
                        ]       
                    await self.bot.send_message(entity = event.chat_id , message = 'انتخاب كنيد' , reply_to = event , buttons = Buttons ) 
                
                elif event.text == 'استعلام وضعيت' :  
                    access_level = Accounts_col.find_one({'sender_id' : sender_id})['Access level']          
                    await self.bot.send_message(entity = event.chat_id , message = f'شما داراي سطح {access_level} اشتراك هستيد' , reply_to = event ) 
                
                elif event.text == 'خريد اشتراك سطح 1' :
                    await self.bot.send_message(entity = event.chat_id , message = '1' , reply_to = event ) 
                    
                elif event.text == 'خريد اشتراك سطح 2' :
                    await self.bot.send_message(entity = event.chat_id , message = '2' , reply_to = event ) 
                    
                elif event.text == 'خريد اشتراك سطح 3' :
                    await self.bot.send_message(entity = event.chat_id , message = '3' , reply_to = event )                
            
            
            except errors.rpcerrorlist.UserNotParticipantError :
                Buttons = [
                    [Button.url('عضويت در كانال','t.me/test')],
                    [Button.inline('عضو شدم',data = '1')]
                ]
                await self.bot.send_message(entity = event.chat_id , message= ' براي ادامه ي كار با ربات بايد حتما در كانال زير عضو شويد \
                    \n  \n  وقتي عضو شديد ، روي دكمه\n "عضو شدم" كليك كنيد ', reply_to = event , buttons = Buttons )  
                    

    async def inline_handler(self , event : events.CallbackQuery) : 
        if event.data.decode() == '1' :
                sender_id = int(event.sender_id)
                
                try :
                    await self.bot(functions.channels.GetParticipantRequest(channel = channel , participant = sender_id))
                    await event.answer('عضويت شما تاييد شد') 
                    await self.bot.delete_messages(entity = event.original_update.user_id , message_ids = event.original_update.msg_id ) 
                    await self.bot.send_message(entity = event.chat_id , message= 'يه كامند رو انتخاب كن' ) 
                
                except errors.rpcerrorlist.UserNotParticipantError :
                    await event.answer('عضو نشدي كه !') 
 
 
async def run():
    bot = Loggerbot(id , hash , token)
    await bot.asyncInit()
    
    
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()
loop.create_task(run())
loop.run_forever()    