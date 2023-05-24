import bot
import assistants

if __name__=="__main__":
    try: 
        str_ = ""
        for i, asst in enumerate(assistants.list_of_available_assistants): str_+= f"{i}: {asst.name}, "
        inp = int(input(f"{str_}\n- "))
        assistant = assistants.list_of_available_assistants[inp]
    except Exception as e: print("Failed to load eviorment variables or select assistant. Error:\n", e)
    else: bot.run_discord_bot(assistant) 


