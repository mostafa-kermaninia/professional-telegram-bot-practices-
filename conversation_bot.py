from telethon import TelegramClient , events , Button
from specs import id,hash,token
import asyncio


class Loggerbot:
    
    def __init__(self, api_id : int , api_hash : str , token : str):
        self.bot = TelegramClient('bot' , api_id , api_hash)
        self.token = token
        self.bot.add_event_handler(self.main , events.NewMessage)
        self.bot.add_event_handler(self.inline_handler, events.CallbackQuery)
        
        
    async def asyncInit(self):
        await self.bot.start(bot_token = self.token)
        
    async def main(self , event : events.NewMessage): 
        
        if event.text == '/start' :
            await self.bot.send_message(entity = event.chat_id , message= 'سلام!،يه كامند رو انتخاب كن' , reply_to = event ) 
         
        elif event.text == '/joke' :
            Buttons = [
                [Button.text('جوك بلند اول(اينو بزن)' , resize = True , single_use = True) , Button.text('جوك بلند دوم')],
                [Button.text('جوك كوتاه اول')]
                ]
                   
            await self.bot.send_message(entity = event.chat_id , message= 'آفرين،حالا يه مدل جوك انتخاب كن' , reply_to = event , buttons = Buttons ) 
               
        elif event.text == '/greeting' :
            Buttons = [
                Button.text('حال خودم',resize =True),
                Button.text('حال خانواده(اينو بزن)' , single_use = True)
                ]       
            await self.bot.send_message(entity = event.chat_id , message= 'خب حال كيو بپرسم؟' , reply_to = event , buttons = Buttons ) 
        
        elif event.text == 'جوك بلند اول(اينو بزن)' :
            url = 'https://vaghayerooz.com/fa/news/11765/%D8%AC%D9%88%DA%A9-%D8%AE%D9%86%D8%AF%D9%87-%D8%AF%D8%A7%D8%B1-%DA%A9%D8%B1%D9%88%D9%86%D8%A7-%D8%AF%D8%B1-%D8%AA%D9%84%DA%AF%D8%B1%D8%A7%D9%85-%D9%88-%D8%A7%DB%8C%D9%86%D8%B3%D8%AA%D8%A7%DA%AF%D8%B1%D8%A7%D9%85-%D9%88-%D9%88%D8%A7%D8%AA%D8%B3%D8%A7%D9%BE-%D9%88-%D8%AC%D8%AF%DB%8C%D8%AF%D8%AA%D8%B1%DB%8C%D9%86-%D8%AC%DA%A9-%D9%87%D8%A7%DB%8C-%D8%A8%D8%A7-%D9%85%D8%B2%D9%87-%D9%88-%D8%AC%D8%B0%D8%A7%D8%A8-%D9%81%D8%B6%D8%A7%DB%8C-%D9%85%D8%AC%D8%A7%D8%B2%DB%8C'
            Buttons = [
                [Button.url('سايت جوك',url),Button.url('site2','https://google.com')],
                [Button.url('site3','https://google.com') , Button.url('site4','https://google.com')],
                [Button.inline('بازم بگو',data = '1') , Button.inline('دوباره،يبار فايده نداره',data = '2')]
            ]    
            await self.bot.send_message(entity = event.chat_id , message= 'جووووووووووووووووووووووووووووك' , reply_to = event , buttons = Buttons ) 
        
        elif event.text == 'حال خانواده(اينو بزن)' :
            url = 'https://vaghayerooz.com/fa/news/11765/%D8%AC%D9%88%DA%A9-%D8%AE%D9%86%D8%AF%D9%87-%D8%AF%D8%A7%D8%B1-%DA%A9%D8%B1%D9%88%D9%86%D8%A7-%D8%AF%D8%B1-%D8%AA%D9%84%DA%AF%D8%B1%D8%A7%D9%85-%D9%88-%D8%A7%DB%8C%D9%86%D8%B3%D8%AA%D8%A7%DA%AF%D8%B1%D8%A7%D9%85-%D9%88-%D9%88%D8%A7%D8%AA%D8%B3%D8%A7%D9%BE-%D9%88-%D8%AC%D8%AF%DB%8C%D8%AF%D8%AA%D8%B1%DB%8C%D9%86-%D8%AC%DA%A9-%D9%87%D8%A7%DB%8C-%D8%A8%D8%A7-%D9%85%D8%B2%D9%87-%D9%88-%D8%AC%D8%B0%D8%A7%D8%A8-%D9%81%D8%B6%D8%A7%DB%8C-%D9%85%D8%AC%D8%A7%D8%B2%DB%8C'
            Buttons = [
                [Button.inline('باز بپرس',data = '1') , Button.inline('دوباره،يبار فايده نداره',data = '2')]
            ]    
            await self.bot.send_message(entity = event.chat_id , message= 'حال خانوادت چطوره داوش؟همه خوبن؟ :/' , reply_to = event , buttons = Buttons ) 
                
     
        
    async def inline_handler (self , event : events.CallbackQuery) :
        if event.data.decode() == '1' :
            Buttons = [
                [Button.url('site6','https://google.com') , Button.url('site7','https://google.com')],
                [Button.url('site8','https://google.com')],
                [Button.inline('اينم بزن،جالبه',data = '3') , Button.inline('inlinebutton1.2',data = '4')]
            ]
            await self.bot.edit_message(entity = event.original_update.user_id , message = event.original_update.msg_id ,text= 'بسه ديگه داوش،بيا از گوگل پيدا كن' , buttons=Buttons) 

        elif event.data.decode() == '2' :
            Buttons = [
                [Button.url('site6','https://google.com')],
                [Button.url('site8','https://google.com')],
                [Button.inline('اينم بزن ،جالبه',data = '5') , Button.inline('inlinebutton2.2',data = '6')]
            ]
            await self.bot.edit_message(entity = event.original_update.user_id , message = event.original_update.msg_id , text= 'بسه باو خسته شدم،بيا از گوگل پيدا كن' , buttons=Buttons) 
        elif event.data.decode() == '3' or event.data.decode() == '5' : 
            await event.answer('هاهاها اسكلت كردم' , alert = True )               
                

    
    
async def run():
    bot = Loggerbot(id, hash, token)
    await bot.asyncInit()
    
    
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()
loop.create_task(run())
loop.run_forever()    