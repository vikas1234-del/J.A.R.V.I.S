import mysql.connector
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import mysql
#import psutil


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


con=mysql.connector.connect(host="localhost",user="root",password="vikas",database="jarvisai")
cur=con.cursor()
# cur.execute("show tables;")
# res=cur.fetchall()
# print(res)

def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()


def time() -> None:
    """Tells the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    """Tells the current date."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme() -> None:
    """Greets the user based on the time of day."""
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    #current_time = datetime.now().strftime("%H:%M:%S")


# Print the current time
   # print("Current time:", current_time)

    #a_p=cur.strftime("%p")

    
    #if 4 <= hour < 12:
        #if (a_p=="PM"):
             #speak("Good evening!")
             #print("Good evening!") 
        #else:
            
        #     speak("Good morning!")
        #     print("Good morning!")
    #elif 1 <= hour < 5:
     #   if (a_p=="PM"):
    #         speak("Good afternoon!")
    #         print("Good afternoon!")
     #   else:
    #         speak("Good evening!")
     #        print("Good evening!")
    #else:
     #    speak("Good night, see you tomorrow.")


    current_time = datetime.datetime.now()
    hour = current_time.hour

# Check the time of day and print the appropriate greeting
    if 5 <= hour < 12:
        speak("Good morning! Sir")
        print("Good Morning")
    elif 12 <= hour < 18:
        speak("Good evening! Sir")
        print("Good Evening")
    else:
        speak("Good night")
        print("Good Night Sir ")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")


def screenshot() -> None:
    """Takes a screenshot and saves it."""
    try:
        # Take the screenshot
        img = pyautogui.screenshot()
        
        # Get the path to the user's images directory
        img_path = os.path.join(os.getcwd(), "Images\\one.png")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        
        # Save the image
        img.save(img_path)
        
        # Announce the file path and print it
        speak(f"Screenshot saved as {img_path}.")
        print(f"Screenshot saved as {img_path}.")
    except Exception as e:
        # Handle any errors during the process
        speak(f"Failed to take a screenshot. Error: {str(e)}")
        print(f"Failed to take a screenshot. Error: {str(e)}")

def takecommand() -> str:
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)  # Listen with a timeout
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
        return None

def play_music(song_name=None) -> None:
    """Plays music from the user's Music directory."""
    song_dir = os.path.expanduser("~\\Music") #~\\Music
    songs = os.listdir(song_dir)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}.")
        print(f"Playing {song}.")
    else:
        speak("No song found.")
        print("No song found.")

def set_name() -> None:
    """Sets a new name for the assistant."""
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

def load_name() -> str:
    """Loads the assistant's name from a file, or uses a default name."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"  # Default name


def search_wikipedia(query):
    """Searches Wikipedia and returns a summary."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def google_translater(query):
    """Translate something and returns a summary."""
    try:
        speak("Google Translater...")
        result= google_translater.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "date" in query:
            date()
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "wikipedia" in query:
            wb.open("wikipedia.org")
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "google translater" in query:
            wb.open("https://translate.google.com/?sl=auto&tl=en&op=translate")
            query = query.replace("wikipedia", "").strip()
            google_translater(query)
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()    
        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            play_music(song_name)
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "open youtube" in query:
            wb.open("youtube.com")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "what is your name" in query:
            speak("hey user my name vikas")
            print("hey user my name vikas")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "open google" in query:
            wb.open("google.com")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "change your name" in query:
            set_name()
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "screenshot" in query:
            screenshot()
            speak("I've taken screenshot, please check it")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "tell me a joke" in query :
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "shutdown" in query:
            speak("Shutting down the system, goodbye!")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
            con.close()
            os.system("shutdown /s /f /t 1")
            break
            
        elif "restart" in query:
            speak("Restarting the system, please wait!")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
            con.commit()
            con.close()
            os.system("shutdown /r /f /t 1")
            break
            
        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
            
            con.close()
            break
        
        elif "internet speed" in query:
            wb.open("fast.com")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()
        elif "wish me" in query:
            wishme()
        elif "what functions can you do" in query or "what function you do" in query or "function" in query:
            speak("I can do 25+ fuctions in this project those fuction are as listed below")
            print("I can do 25+ fuctions in this project those fuction are as listed below")
            speak("1st one is I giving wishesh to you ")
            print("1st one is I giving wishesh to you ")
            speak("set my name as your wish")
            print("set my name as your wish")
            speak("then Saying the current time")
            print("then Saying the current time")
            speak("show the current date")
            print("show the current date")
            speak("open the wikipwdia and then search as your wish")
            print("open the wikipwdia and then search as your wish")
            speak("open the youtube application and  search as you wont")
            print("open the youtube application and  search as you wont")
            speak("controll the play music on youtube")
            print("controll the play music on youtube")
            speak("open the Google")
            print("open the Google")
            speak("open the Google translater")
            print("open the Google translater")
            speak("change your name function")
            print("change your name function")
            speak("get the screenshot of the screen")
            print("get the screenshot of the screen")
            speak("i say the one joke for you as a entertainment")
            print("i say the one joke for you as a entertainment")
            speak("shutdown the system")
            print("shutdown the system")
            speak("restarting the system")
            print("restarting the system")
            speak("going offline as per your wish")
            print("going offline as per your wish")
            speak("check the current internet speed")
            print("check the current internet speed")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()

        elif "what is your name " in query:
            speak("Hey! user My name is vikas and please tell me what can i help you")
            print("Hey! user My name is vikas and please tell me what can i help you")
            q=f"insert into queries (query)values('{query}');"
            print(q)
            cur.execute(q)
            con.commit()

        #cpu_percent = psutil.cpu_percent(interval=1)  # CPU usage in percentage
        #cpu_count = psutil.cpu_count(logical=False)  # Physical cores
        #cpu_count_logical = psutil.cpu_count(logical=True)  # Logical cores

        # Memory info
        #memory = psutil.virtual_memory()  # Virtual memory info
        #total_memory = memory.total
        #used_memory = memory.used
        #memory_percent = memory.percent

        # Disk info
        #disk = psutil.disk_usage('/')
        #total_disk = disk.total
        #used_disk = disk.used
        #disk_percent = disk.percent

        # Network info
        #network = psutil.net_if_addrs()  # Get network interfaces and addresses
        #bytes_sent = psutil.net_io_counters().bytes_sent
        #bytes_recv = psutil.net_io_counters().bytes_recv

        # Output system status
        #print("CPU Usage: {}%".format(cpu_percent))
        #print("CPU Physical Cores: {}".format(cpu_count))
        #print("CPU Logical Cores: {}".format(cpu_count_logical))

        #print("Total Memory: {} GB".format(total_memory / (1024 ** 3)))
        #print("Used Memory: {} GB".format(used_memory / (1024 ** 3)))
        #print("Free Memory: {} GB".format(free_memory / (1024 ** 3)))
        #print("Memory Usage: {}%".format(memory_percent))

        #print("Total Disk Space: {} GB".format(total_disk / (1024 ** 3)))
        #print("Used Disk Space: {} GB".format(used_disk / (1024 ** 3)))
        #print("Free Disk Space: {} GB".format(free_disk / (1024 ** 3)))
        #print("Disk Usage: {}%".format(disk_percent))

        #print("Network Sent: {} bytes".format(bytes_sent))
        #print("Network Received: {} bytes".format(bytes_recv))  