#!/usr/bin/env python3
"""v3: refaz os 13 posts (10 carrosseis + 3 fixados) com arte2 (mascote, selos, icones).
Saida: posts-v3/<slug>/slide_N.jpg + legenda.txt"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from refazer_posts import P, S
import arte2
OUT = os.path.join(HERE, "..", "posts-v3")
del P["2026-11-03-quiz-nbr9050-rampa"]   # nunca foi publicado no perfil
FALAS = {
"2026-11-02-pgr-teste": ["Teste rápido: bora?","Já pensou no estresse?","Plano escrito conta!","Quem faz? Até quando?","Conferiu se funciona?","Eu te ajudo a revisar!"],
"2026-11-03-nr35-treinamento": ["A regra mudou!","Presencial é o que vale.","Híbrido: 1 ano p/ adequar.","Escada também entra!","Certificado não basta.","Tudo em dia?","Bora conferir?"],
"2026-11-03-checklist-laudo": ["5 perguntas, 1 minuto!","Confira o CREA!","ART: pergunte antes!","Cadê a vistoria?","Escopo claro evita briga.","Método à vista!","Fala comigo!"],
"2026-11-04-quiz-nr3": ["Cuidado com a interdição!","Não é tudo igual!","Risco grave = atenção.","Não precisa de acidente.","PGR na gaveta não vale.","Confere hoje!","Vistoria independente!"],
"2026-11-04-quiz-nr10": ["Choque? Nem pensar!","Prontuário atualizado?","Habilitado e registrado!","Pensou antes de mexer?","Quando foi a última?","Revise os documentos!","Bora revisar?"],
"2026-11-05-andaime-nr18": ["Prevenir é melhor!","Projeto e responsável!","Piso completo, por favor.","Inspecione antes do turno!","Queda baixa também fere.","Só suba com checklist!","Vistoria técnica!"],
"2026-11-05-nr12-mitos": ["Spoiler: precisa, sim!","Tirar proteção não resolve!","Emergência tem que funcionar!","Desligou? Bloqueie!","Treinamento de verdade!","Como está a sua máquina?","Bora conversar?"],
"2026-11-06-acessibilidade-erros": ["Rampa sozinha não basta!","Norma vigente, sempre!","Piso tátil: outra norma!","Rampa fora do padrão é risco","Rota completa!","Qual você já viu?"],
"2026-11-06-insalubridade-periculosidade": ["Dá pra somar? Calma!","Escolhe o mais favorável.","Confira mudanças recentes.","Depende de perícia!","Checklist na mão!","Já passou por isso?"],
"2026-11-09-aep-nr17": ["Ergonomia vai além!","Vale p/ todas as empresas!","Sem modelo oficial.","Papel assinado não basta.","Checklist rápido!","Qual mito você ouviu?"],
}
def selo(s):
    k, t, ti = s["kicker"].lower(), s["texto"], s["titulo"]
    if t.startswith("MITO"): return ["MITO", "red"]
    if t.startswith("CUIDADO"): return ["ATENÇÃO", "gold"]
    if (k.startswith("mito") and "x verdade" not in k and "ou verdade" not in k) or ti.startswith("Mito:"): return ["MITO", "red"]
    if k == "verdade": return ["VERDADE", "green"]
    if k.startswith("erro"): return ["ERRO COMUM", "red"]
    if k.startswith("checklist"): return ["CHECKLIST", "blue"]
    if k.startswith("atenção"): return ["ATENÇÃO", "gold"]
    return None
POSTS = {}
for slug, p in P.items():
    sl = []
    for s, f in zip(p["slides"], FALAS[slug]):
        s = dict(s); s["fala"] = f
        if not s.get("cta") and selo(s): s["selo"] = selo(s)
        sl.append(s)
    POSTS[slug] = (sl, p["caption"])
def A(k, t, x, ic=None, f=None, cta=False):
    d = {"kicker": k, "titulo": t, "texto": x, "fala": f}
    if ic: d["icone"] = ic
    if cta: d["cta"] = True
    return d
POSTS["fixado-1-quem-sou"] = ([
 A("Quem sou","André Victor","Engenharia, segurança e perícia aplicadas a decisões mais seguras. CREA-RJ 2014128139.","perfil","Prazer, sou o André!"),
 A("Formação","Sou Engenheiro de Produção, Engenheiro de Segurança do Trabalho e tenho formação em Perícia Judicial.","CREA-RJ 2014128139.","perfil","Formação e registro!"),
 A("Experiência","Minha experiência reúne:","Auditorias e sistemas de gestão • Análise e melhoria de processos • Custos e indicadores • Segurança e conformidade • Documentos técnicos.","pgr","Muita coisa na bagagem!"),
 A("Como trabalho","Meu objetivo é traduzir questões técnicas de forma clara, acessível e fundamentada.","Entender o risco • Verificar o que precisa ser analisado • Orientar adequações • Definir próximos passos.","laudo5","Sem “tecniquês”!"),
 A("Vamos conversar","Atuação com base no Rio de Janeiro e possibilidade de atendimento em todo o Brasil, conforme o tipo de serviço.","Direct ou WhatsApp: 21 99419-2878.",None,"Bora conversar?",True)],
 "Prazer, eu sou o André Victor! 👷‍♂️\n\nEngenheiro de Produção, Engenheiro de Segurança do Trabalho e com formação em Perícia Judicial (CREA-RJ 2014128139). Aqui eu uso engenharia, segurança e perícia para ajudar em decisões mais seguras, traduzindo questões técnicas de forma clara, acessível e fundamentada.\n\nMinha experiência reúne auditorias e sistemas de gestão, análise e melhoria de processos, custos e indicadores, segurança e conformidade e documentos técnicos.\n\nAtuação com base no Rio de Janeiro e possibilidade de atendimento em todo o Brasil, conforme o tipo de serviço.\n\n👉 Qual assunto técnico você gostaria de ver aqui? Conta nos comentários!\n\nDirect ou WhatsApp: 21 99419-2878 (link na bio).\n\n#EngenhariaDeSeguranca #Pericia #Laudos #riodejaneiro #rj")
POSTS["fixado-2-laudos-vistorias-pericias"] = ([
 A("Como posso ajudar","Laudos, vistorias, perícias e mais","Uma avaliação técnica pode esclarecer riscos, responsabilidades e próximos passos.","laudo5","Posso te ajudar!"),
 A("Laudos e vistorias","Quando é necessário registrar tecnicamente as condições de uma edificação, ambiente ou sistema.","A vistoria observa. O laudo organiza e fundamenta as conclusões.","predio","Vistoria observa, laudo explica!"),
 A("Perícias e assistência técnica","Em conflitos, processos ou discussões técnicas, a análise deve ser feita com método, documentos e evidências.","A assistência técnica acompanha a parte e contribui para a leitura técnica do caso.","laudo5","Método e evidências!"),
 A("Segurança e acessibilidade","Também posso ajudar na identificação de riscos relacionados a:","Circulação e portas • Rotas e saídas • Manutenção predial • Segurança contra incêndio • Acessibilidade • Uso dos ambientes.","rampa","Olho nos detalhes!"),
 A("Consultoria e conformidade","Para empresas, escolas, condomínios e outros estabelecimentos:","Análise de não conformidades • Orientação para adequações • Organização de documentos • Melhoria de processos • Apoio técnico.","pgr","Para todo tipo de lugar!"),
 A("Cada caso é um caso","Cada situação precisa ser entendida antes de qualquer conclusão.","Não sabe qual serviço precisa? Explique a situação. Eu ajudo a identificar o caminho técnico mais adequado. Direct ou WhatsApp: 21 99419-2878.",None,"Me conta o seu caso!",True)],
 "Laudos, vistorias, perícias e mais. 📋\n\nUma avaliação técnica pode esclarecer riscos, responsabilidades e próximos passos. A vistoria observa; o laudo organiza e fundamenta as conclusões. Em conflitos, processos ou discussões técnicas, a análise deve ser feita com método, documentos e evidências, e a assistência técnica acompanha a parte e contribui para a leitura técnica do caso.\n\nTambém ajudo na identificação de riscos de circulação e portas, rotas e saídas, manutenção predial, segurança contra incêndio, acessibilidade e uso dos ambientes, e em consultoria e conformidade para empresas, escolas, condomínios e outros estabelecimentos.\n\n👉 Qual desses serviços faz sentido para você? Conta nos comentários!\n\nAtendimento remoto ou presencial, conforme a demanda. Direct ou WhatsApp: 21 99419-2878 (link na bio).\n\n#Laudos #Vistoria #Pericia #riodejaneiro #rj")
POSTS["fixado-3-avaliacao-tecnica"] = ([
 A("Fale comigo","Precisa de uma avaliação técnica?","O primeiro passo é explicar o seu caso. WhatsApp 21 99419-2878.","chat","Me conta o seu caso!"),
 A("O que você pode enviar","Para iniciar a conversa, você pode informar:","Qual é o imóvel ou situação • Onde está localizado • Qual problema foi identificado • Se existe prazo ou processo • Fotos, vídeos ou documentos.","chat","Fotos ajudam muito!"),
 A("O que acontece depois","A partir das informações iniciais, é possível entender:","Se a demanda pode ser remota • Se será necessária uma visita • Quais documentos são importantes • Qual serviço faz mais sentido.","laudo5","Depois a gente decide!"),
 A("Atendimento","Direct: para uma primeira conversa pelo Instagram.","WhatsApp: para explicar o caso e enviar arquivos. E-mail: para encaminhar informações e documentos.","chat","Escolha o seu canal!"),
 A("Dados de contato","André Victor","Engenheiro de Produção • Engenheiro de Segurança do Trabalho • Formação em Perícia Judicial • CREA-RJ 2014128139. WhatsApp 21 99419-2878 • engperitoandre@gmail.com.","perfil","Aqui está o meu contato!"),
 A("Vamos entender o seu caso","Atendimento a partir do Rio de Janeiro e avaliação de demandas em todo o Brasil, conforme o serviço.","Envie uma mensagem e conte brevemente o que aconteceu. WhatsApp 21 99419-2878.",None,"Bora conversar?",True)],
 "Precisa de uma avaliação técnica? 🔎\n\nO primeiro passo é explicar o seu caso. Para iniciar a conversa, você pode informar: qual é o imóvel ou situação, onde está localizado, qual problema foi identificado, se existe prazo ou processo, e enviar fotos, vídeos ou documentos.\n\nA partir das informações iniciais, é possível entender se a demanda pode ser remota, se será necessária uma visita, quais documentos são importantes e qual serviço faz mais sentido.\n\nDirect para uma primeira conversa, WhatsApp para explicar o caso e enviar arquivos, e e-mail para encaminhar informações e documentos.\n\n👉 Tem alguma dúvida sobre como funciona? Pergunta nos comentários!\n\nAtendimento a partir do Rio de Janeiro, com avaliação de demandas em todo o Brasil, conforme o serviço. WhatsApp 21 99419-2878 (link na bio).\n\n#AvaliacaoTecnica #Laudos #Pericia #riodejaneiro #rj")
ORDEM = ["fixado-1-quem-sou","fixado-2-laudos-vistorias-pericias","fixado-3-avaliacao-tecnica"] + [k for k in POSTS if not k.startswith("fixado")]
if __name__ == "__main__":
    for slug in ORDEM:
        sl, cap = POSTS[slug]; d = os.path.join(OUT, slug)
        arte2.gerar(sl, d); open(os.path.join(d, "legenda.txt"), "w", encoding="utf-8").write(cap)
        print(slug, len(sl), len(cap))
