import difflib

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
Window.size= (350, 550)

from chatbot import load_knowledge_base
from chatbot import save_knowledge_base
from chatbot import find_best_match
from chatbot import get_answer_for_question

#* Red neuronal
from pokemon_rn import load_weights
from pokemon_rn import load_bias
from pokemon_rn import test



class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins-SemiBold.ttf"
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins-SemiBold.ttf"
    font_size = 17


class ChatBot(MDApp):
    
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    learn_response= False
    learn= False
    new_question = '' 
    
    #! ======= Propiedad para las palabras baneadas =====    
    active_banned_words = False

    #* ======= Propiedades para la red neuronal ========= 
    active_rn = False
    rn_inputs = {
        "inputAttack": False,
        "inputDeffense": False
    }
    habilities = {
        "attack": 0,
        "deffense": 0
    }

    def change_screen(self, name):
        screen_manager.curent = name

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
        return screen_manager
    
    def bot_name(self):
        if screen_manager.get_screen('main').bot_name.text != "":
            screen_manager.get_screen('chats').bot_name.text = screen_manager.get_screen('main').bot_name.text
            screen_manager.current = "chats"

    def response(self, *args):
        try:
            question= ""
            response= ""
            best_match: str | None = find_best_match(value, [q["question"] for q in self.knowledge_base["question"]])
            
            if self.learn:
                # value
                # Imprimir aprendí algo nuevo
                print('=============')
                question =self.new_question
                print(question)
                print(value)
                self.learn = False
                response = self.learn_answer()

            else: 
                if value.lower() == 'salir':
                    response = "Adios! Que tengas un gran día"

                if best_match:
                    response = get_answer_for_question(best_match, self.knowledge_base)
                    #! Desactivar de palabras baneadas
                    self.active_banned_words = False

                #* ============= Activar red neuronal =============
                elif self.active_rn:
                    print('========  Activar red neuronal ==========')

                    if self.rn_inputs["inputAttack"]:
                        
                        self.habilities["attack"] = int(value)
                        self.rn_inputs["inputAttack"] = False

                    if self.rn_inputs["inputDeffense"]:
                        self.habilities["deffense"] = int(value)
                        self.rn_inputs["inputDeffense"] = False

                    if self.habilities["attack"] == 0:
                        response = "Claro que sí, ingresa el nivel de ataque del 1 al 100."
                        self.rn_inputs["inputAttack"] = True

                    elif self.habilities["deffense"] == 0:
                        response = "Ahora ingresa su nivel de defensa"
                        self.rn_inputs["inputDeffense"] = True

                    elif self.habilities["attack"] != 0 and self.habilities["deffense"] != 0:

                        #TODO Enviar datos
                        weights = load_weights()
                        bias = load_bias()

                        inputs = [self.habilities["attack"] * 0.01, self.habilities["deffense"] * 0.01]
                        print(inputs)
                        predicted_output = test(inputs, weights, bias)
                        if predicted_output < 0.5:
                            response = "Clasificación: Bajo nivel :(" 
                        else:
                            response = "Clasificación: Buen nivel ;)" 
                        print(predicted_output)

                        self.habilities["attack"] = 0
                        self.habilities["deffense"] = 0
                        self.active_rn = False

                #* =============================================

                elif self.active_banned_words is False:
                    response = f"No sé la respuesta. ¿Puede enseñármela?\nSolamente debes de digitar la respuesta debajo {screen_manager.get_screen('chats').text_input.text}"
                    self.learn = True
                    self.new_question = value

            screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x=.75))
        except:
            self.active_rn = False
            self.rn_inputs["inputAttack"] = False
            self.rn_inputs["inputDeffense"] = False
            self.habilities["attack"] = 0
            self.habilities["deffense"] = 0
    

    def send(self):
        global size, halign, value
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
          
            if value.lower() == 'salir':
                response = "Adios! Que tengas un gran dia"
            if len(value) < 6:
                size = .22
                halign = "center"
            elif len(value) < 11:
                size = .32
                halign = "center"
            elif len(value) < 16:
                size = .45
                halign = "center"
            elif len(value) < 21:
                size = .58
                halign = "center"
            elif len(value) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

        # Imprimir imput del usuario
        screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x=size,halign=halign))
        Clock.schedule_once(self.response, 2)

        #* ==== Buscar la palabra pokemon ===========
        key_words = ['pokemons', 'pokemones','pokemon']

        input_arr = value.split()

        for kw in key_words:
            if kw in input_arr:
                print('Si está la palabra: ', kw)
                self.active_rn = True
           
        #! Buscar palabras baneadas
        kb = load_knowledge_base('knowledge_base.json')
        bannedWords = kb["banned_words"]
        hasBannedWords: bool = False
        
        for word in value.split():
            result = difflib.get_close_matches(word, bannedWords, n=1,  cutoff=0.8)
            if result:
                hasBannedWords = True
        
        #! activo
        if hasBannedWords:
            error_message = 'No puedo generar insultos ni contenido ofensivo. ¿En qué más puedo ayudarte?'
            self.active_banned_words = True
            screen_manager.get_screen('chats').chat_list.add_widget(Response(text=error_message, size_hint_x=.75))

        screen_manager.get_screen('chats').text_input.text = ""

    def learn_answer(self):
        question = self.new_question
        response = ''
        if value.lower() != 'omitir':
            #! Buscar palabras baneadas
            kb = load_knowledge_base('knowledge_base.json')
            bannedWords = kb["banned_words"]
            hasBannedWords: bool = False

            for word in value.split():
                result = difflib.get_close_matches(word, bannedWords, n=1,  cutoff=0.8)
                if result:
                    hasBannedWords = True
                    
            if hasBannedWords:
                error_message = 'No puedo generar insultos ni contenido ofensivo. ¿En qué más puedo ayudarte?'
                self.active_banned_words = True
                screen_manager.get_screen('chats').chat_list.add_widget(Response(text=error_message, size_hint_x=.75))
                hasBannedWords = False
                
            else:
                self.knowledge_base["question"].append({"question": question, "answer": value})
                save_knowledge_base('knowledge_base.json', self.knowledge_base)
                response = '¡Gracias! ¡He aprendido algo nuevo!'
                hasBannedWords = False
        
        return response

    
if __name__ == '__main__':
    ChatBot().run()