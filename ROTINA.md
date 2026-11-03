# Rotina diária de Instagram — @engperitoandre

Perfil: Eng. André Victor Moreira Costa (Engenheiro de Produção e de Segurança do Trabalho, perícias/laudos, CREA-RJ 2014128139), Rio de Janeiro.
Contato do CTA: WhatsApp 21 99419-2878. Site: engperitoandrevictor.blogspot.com.
Serviços: laudos e vistorias, perícia, segurança do trabalho (PGR/GRO, NRs), predial/acessibilidade, auditorias, análise de causa-raiz.

## Passo a passo de cada execução
1. Variáveis: `IG_ACCESS_TOKEN` (obrigatória). `IG_BUSINESS_ACCOUNT_ID=17841426326269727`. Se o token faltar ou a Meta responder erro de token (code 190), NÃO tente outra forma: avise o usuário (PushNotification) e encerre.
2. Espere um atraso aleatório de 0 a 60 min (`sleep $((RANDOM % 3600))`) para variar o horário. Só nas execuções agendadas: se a execução foi disparada manualmente (mensagem de teste do usuário), pule a espera.
3. Leia `posts/historico.md` e NÃO repita tema dos últimos 30 posts.
4. Escolha 1 tema dentro do escopo do André (engenharia de produção e segurança do trabalho, perícia/laudos, predial e acessibilidade, gestão e qualidade). Fontes de tema, em ordem de preferência:
   a) **Notícia recente** de acidente de trabalho, incidente, interdição ou não conformidade (ex.: Agência Brasil, g1, gov.br/MTE, Ministério Público do Trabalho). Mostre **o que provavelmente falhou e o que poderia ter evitado** (causa-raiz, NR aplicável, medida de controle, laudo/vistoria que ajudaria). Regras: não cite nome de vítima, de empresa nem de local identificável; não acuse ninguém nem afirme culpa ou causa como fato ("segundo a imprensa", "em casos assim"); não use fotos nem reproduza o texto da notícia; tom respeitoso.
   b) Mudança de norma, portaria ou fiscalização (NR-1/PGR/riscos psicossociais, NR-35, NR-12, NR-10, NR-18, NR-17, insalubridade/periculosidade, perícia trabalhista, NBR 9050, inspeção predial, ISO 9001/45001/14001/41001, LGPD).
   c) Erro comum, mito ou dúvida frequente de clientes.
   Limite de pesquisa: no máximo **3 buscas e 3 páginas lidas** (~5 minutos). Prefira 1 fonte oficial (gov.br/MTE, ABNT, Confea, a própria norma). Ao passar do limite, use o melhor tema já confirmado.
   Prazos, datas e números: confirme quando achar rápido em fonte oficial. **Se não confirmar, publique sem esse dado**, sem inventar e sem se comprometer: use frases como "confira o prazo vigente na norma" ou "verifique a regra atual", e não prometa resultado nem garantia jurídica. Nunca invente dado, lei, prazo ou estatística. Nunca dê como certo o que não confirmou.
5. Escolha o formato: quiz/teste, mito vs verdade, checklist, "erro comum", ou caso (sem identificar pessoas). Deve prender o leitor e terminar com chamada para contato no WhatsApp. Nada de carrossel seco e informativo.
6. Crie 5–7 slides em JSON e gere com `python3 rotina/arte.py conteudo.json saida` (JPEG 1080x1350). Último slide com `"cta": true`. Confira o texto: sem erros de português, sem texto cortado (abra ao menos 2 slides com Read).
7. Legenda: gancho na 1ª linha, até ~600 caracteres, CTA para o WhatsApp, 5 hashtags. Sem promessa de resultado, sem garantia jurídica, sem depoimentos inventados.
8. Publique as imagens neste mesmo repositório (andrevictorm/blog-engenharia, público, pois a Meta precisa baixá-las). Se não estiver clonado em /home/claude/blog-engenharia, anexe com `add_repo` (access push) e clone; senão `git pull`. Copie para `posts/AAAA-MM-DD-HHMM/slide_N.jpg`, `git add`, commit e `git push origin main`. A URL será `https://raw.githubusercontent.com/andrevictorm/blog-engenharia/main/posts/AAAA-MM-DD-HHMM/slide_N.jpg`. Confira que cada URL responde 200 image/jpeg. Nunca coloque token ou dado sensível neste repositório.
9. Escreva `post.json` ({"caption":..., "image_urls":[...]}) e rode `python3 rotina/publish_carousel.py post.json` (primeiro `--dry-run`).
10. Acrescente uma linha em `posts/historico.md` (data, tema, ID da mídia), commit e push.
11. Envie ao usuário um resumo curto (PushNotification): tema + ID da mídia.

## Limites
- No máximo 2 publicações por dia (a API do Instagram limita 50 por dia).
- Nunca imprima nem grave o token em arquivo, log, commit ou mensagem.
- Não responda comentários, não mande DMs e não altere o perfil. Só publica carrosséis.
- Se algo falhar duas vezes, pare e avise em vez de insistir.
