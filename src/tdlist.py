import os,json,time,sys
from pathlib import Path
from colorama import Fore, Back, Style, init
init()

class TDL:
    
    class Dados:
        def pegar_dados():
            try:
                with open(str(Path.home()).replace("\\","/")+'/TDList/data.json','r') as f:
                    return json.load(f)
            except FileNotFoundError:
                with open(str(Path.home()).replace("\\","/")+'/TDList/data.json','w+') as f:
                    f.write('{\n}')
                    return json.load(f)
        def salvar_dados(dados:dict):
            with open(str(Path.home()).replace("\\","/")+'/TDList/data.json','w') as f:
                json.dump(dados,f,indent=4)    
    def ligar():
        if os.path.exists(str(Path.home())+'\TDList' if os.name == 'nt' else '~/TDList') == False:
            os.mkdir(str(Path.home())+'\TDList' if os.name == 'nt' else '~/TDList')       
        os.system('cls' if os.name  == 'nt' else 'clear') 
        d = dict(TDL.Dados.pegar_dados())
        print("[New/Open]\n.......................\n")
        var = input("New/Open:\t")
        var = var.lower().replace(" ","")
        if var == 'new':
            novo=(
                input("Digite o nome do novo projeto: "),
                input("Digite uma descrição para o projeto: "),
                input("Senha (Se não quiser não digite nada): ")
            )
            ver = input(f"\nNome: {novo[0]}\nDescrição: {novo[1]}\nSenha: ***{novo[2][len(novo[2])-2:]}\nVocê tem certeza? [S/N]")
            if ver.lower() == 's':
                d[novo[0]] = {"Nome":novo[0],"Descrição":novo[1],"Senha":novo[2] if novo[2] != "" else 0,"Andamento":{},"Concluidos":{},"Ideias":{},'Não Começado':{}}
                TDL.Dados.salvar_dados(d)
                proj = d[novo[0]]
                TDL.ReadMode(proj)
            else:
                TDL.ligar()
        elif var == 'open':
            print(Style.BRIGHT)
            os.system('cls' if os.name  == 'nt' else 'clear')
            for k in d:
                print(Fore.GREEN+Back.BLACK+k)
            try:
                print(Style.RESET_ALL)    
                proj = d[input("\nDigite qual projeto você quer acessar:\t")]
            except KeyError:
                os.system('cls' if os.name  == 'nt' else 'clear')
                print("Projeto invalido")
                cont=0
                msg='Projeto invalido'
                final=''
                msg = list(msg)                
                while True:
                    cont +=1
                    time.sleep(1)
                    msg.append(".")
                    for i in msg:
                        final = final + i
                    os.system('cls' if os.name  == 'nt' else 'clear')
                    print(final)
                    final = ''
                    if cont == 5:
                        TDL.ligar()
                        break
            os.system('cls' if os.name  == 'nt' else 'clear')
        if proj['Senha'] == 0:
            TDL.ReadMode(proj)
        else:
            senha = input(f'Digite a senha do projeto {proj["Nome"]}\t')
            if senha == proj['Senha']:
                os.system('cls' if os.name  == 'nt' else 'clear')
                TDL.ReadMode(proj)
            else:
                print("\nSenha invalida")
                time.sleep(2) 
                TDL.ligar()
    def ReadMode(proj: dict):
        level={
        "1":"Normal",
        "2":"Razoalmente Importante",
        "3":"Importante"
        }
        Tp=["bug","feature","update","tasks","issues"]
        v = {
            "em":"Andamento",
            "id":"Ideias",
            "nc":"Não Começado",
            "cl":"Concluidos"
        }
        os.system('cls' if os.name  == 'nt' else 'clear')
        print('[ NOME  :  DESCRIÇÃO ]\n\n')
        print(Back.RESET + Fore.MAGENTA + 'Em Andamento\n')        
        for i in proj['Andamento']:
            print(Fore.YELLOW + f'{i}: ' + f'{Fore.GREEN} [ {proj["Andamento"][i]["Tipo"]} ] {Fore.RED} [ {proj["Andamento"][i]["Grav"]} ]')
        print(Back.RESET + Fore.MAGENTA + '\nNão Começado\n')        
        for i in proj['Não Começado']:
            print(Fore.YELLOW + f'{i}: ' + f'{Fore.GREEN} [ {proj["Não Começado"][i]["Tipo"]} ] {Fore.RED} [ {proj["Não Começado"][i]["Grav"]} ]')
        print(Back.RESET + Fore.MAGENTA + '\nIdeias\n') 
        for i in proj['Ideias']:
            print(Fore.YELLOW + f'{i}: ' + f'{Fore.GREEN} [ {proj["Ideias"][i]["Tipo"]} ] {Fore.RED} [ {proj["Ideias"][i]["Grav"]} ]')
        print(Back.RESET + Fore.MAGENTA + '\nConcluidos\n')        
        for i in proj['Concluidos']:
            print(Fore.YELLOW + f'{i}: ' + f'{Fore.GREEN} [ {proj["Concluidos"][i]["Tipo"]} ]{Fore.RED} [ {proj["Concluidos"][i]["Grav"]} ]')
               
        print(Fore.CYAN)
        ver = input("\n\nNEW | EDIT | INFO | WHERE: ")        
        if ver.lower() == 'new':
            inp = (
                input("Digite o nome: "),
                input("Digite a descrição: "),
                input("Qual é a categoria? [EM = Em andamento | ID = Ideias]: "),
                input("Qual é o tipo? [Bug/Feature/Update/Tasks/Issues]: "),
                input("Qual o nivel de gravidade? [1 = Normal / 2 = Razoavelmente Importante / 3 = Importante]: "),
                input("Digite uma Nota: "),
                input("Digite o nome do arquivo [Se tiver]: ")
            )
            veri = input("Você tem certeza? [S/N]: ")
            if veri.lower() == 's':     
                if inp[2] in v:
                    proj[v[inp[2]]][inp[0]] = {
                        "Nome":inp[0],
                        "Descrição":inp[1],
                        "Tipo":inp[3] if inp[3].lower() in Tp else "Comum",
                        "Grav":level[inp[4]] if inp[4].lower() in level else "Normal",
                        "Nota":inp[5],
                        "Local":inp[6] 
                    } 
                    d = TDL.Dados.pegar_dados()
                    d[proj['Nome']] = proj
                    TDL.Dados.salvar_dados(d)
                    TDL.ReadMode(proj)
                else:
                    TDL.ReadMode(proj) 

        elif ver.lower() == 'edit':
            inp = (
                input("Qual é o tipo? [EM = Em andamento / ID = Ideias / NC = Não começados / CL = Concluidos OU Nada]: "),
                input("Qual o nome?: "),
                print('\n\n'),
                input("Digite o nome [Caso não queria mudar deixe vazio]: "),
                input("Digite a descrição [Caso não queria mudar deixe vazio]: "),
                input("Quer mover para uma categoria? [EM = Em andamento / ID = Ideias / NC = Não começados / CL = Concluidos OU Nada]: ")
            )
            if inp[0].lower() in v:
                inf = proj[v[inp[0].lower()]][inp[1]]
                if inp[5].lower() != '':
                    if inp[5].lower() in v:
                        proj[v[inp[5].lower()]][inf['Nome'] if inp[3] == "" else inp[3]]= {
                            "Nome":inf['Nome'] if inp[3] == "" else inp[3],
                            "Tipo":inf["Tipo"],
                            "Grav":inf["Grav"],
                            "Nota":inf["Nota"],
                            "Local":inf["Local"],
                            "Descrição":inf['Descrição'] if inp[4] == "" else inp[4]
                        }
                        del proj[v[inp[0].lower()]][inp[1]]
                        d = TDL.Dados.pegar_dados()
                        d[proj['Nome']] = proj
                        TDL.Dados.salvar_dados(d)
                    else:
                        print(f"ERROR [ 1 ] | Categoria \"{inp[5]}\" inexistente... ")
                else:
                    proj[v[inp[5]]][inf['Nome'] if inp[3] == "" else inp[3]] = {
                            "Descrição":inf['Descrição'] if inp[4] == "" else inp[4]
                        }
                    d = TDL.Dados.pegar_dados()
                    d[proj['Nome']] = proj
                    TDL.Dados.salvar_dados(d)
                    TDL.ReadMode(proj)
            TDL.ReadMode(proj)

        elif ver.lower() == 'info':
            inp = (
                input("Digite o nome: "),
                input("Digite a categoria [EM = Em andamento / ID = Ideias / NC = Não começados / CL = Concluidos OU Nada]: ")
            )
            os.system('cls' if os.name  == 'nt' else 'clear')
            if inp[1].lower() in v:
                try:
                    lis = proj[v[inp[1].lower()]][inp[0]]
                except KeyError:
                    print("ERROR [ 02 ] - Nome invalido")
                    time.sleep(2)
                    TDL.ReadMode(proj)
                print(
                    f"{Fore.WHITE}###################################\n\n\n{Fore.CYAN}[TAGS] {Fore.WHITE}|  {Fore.GREEN} [ {lis['Tipo']} ] {Fore.RED} [ {lis['Grav']} ]\n{Fore.LIGHTYELLOW_EX}[NOTA] {Fore.WHITE}|  {Fore.CYAN} {lis['Nota']}\n\n\n{Fore.WHITE}###################################")
                os.system("Pause")
                TDL.ReadMode(proj)

        elif ver.lower() == 'where':
            inp = (
                input("Qual o nome?: "),
                input("Qual a categoria? [EM = Em andamento / ID = Ideias / NC = Não começados / CL = Concluidos OU Nada]: ")
            )
            if inp[1].lower() in v:
                if inp[0] in proj[v[inp[1].lower()]]:
                    os.system('cls' if os.name  == 'nt' else 'clear')
                    print(proj[v[inp[1].lower()]][inp[0]]["Local"])
                    os.system('pause')
                    TDL.ReadMode(proj)
            TDL.ReadMode(proj)
TDL.ligar()