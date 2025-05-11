from llmada import BianXieAdapter

class Meeting():
    def __init__(self,system:str = None, members = None):
        self.system = system or "让我们现在模拟一个开会讨论的过程, 我们会有一个主题以及四个与会者, 我们会通过不断的讨论对齐我们的想法,最终形成一个相对全面完整的共识. 以聊天的形式进行"
        self.aiTeam = BianXieAdapter()
        self.history = [{"role":"system","content":self.system}]
        self.members = members or {
                        "gpt-4o":"gpt-4o",
                        "gemini":"gemini-2.5-pro-exp-03-25",
                        "gpt-4.1":"gpt-4.1",
                        }
        
    def guide(self,user_message:str,model:str = "",):
        self.history.append({'role': 'user', 'content': user_message})
        self.aiTeam.set_model(model)
        result = self.aiTeam.chat(self.history)
        self.history.append({'role':'assistant','content':f'发言者 {model}:\n' + result})
        return result
    
    def start(self):
        for model_id in ["gpt-4o","gemini","gpt-4.1","gpt-4o","gemini","gpt-4.1","gpt-4o","gemini","gpt-4.1",
                          "gpt-4o","gemini","gpt-4.1"]:
            model = self.members.get(model_id)
            print("model: ",model)
            user_message = input()
            result = self.guide(user_message,model)
            print(f'发言者 {model}:\n' + result)

            