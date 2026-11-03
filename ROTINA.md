# Rotina diária de Instagram — @engperitoandre

Perfil: Eng. André Victor Moreira Costa (Engenheiro de Produção e de Segurança do Trabalho, perícias/laudos, CREA-RJ 2014128139), Rio de Janeiro.
Contato do CTA: WhatsApp 21 99419-2878. Site: engperitoandrevictor.blogspot.com.
Serviços: laudos e vistorias, perícia, segurança do trabalho (PGR/GRO, NRs), predial/acessibilidade, auditorias, análise de causa-raiz.

## Passo a passo de cada execução
1. Variáveis: `IG_ACCESS_TOKEN` (obrigatória). `IG_BUSINESS_ACCOUNT_ID=17841426326269727`. Se o token faltar ou a Meta responder erro de token (code 190), NÃO tente outra forma: avise o usuário (PushNotification) e encerre.
2. Espere um atraso aleatório de 0 a 60 min (`sleep $((RANDOM % 3600))`) para variar o horário.
3. Leia `posts/historico.md` e NÃO repita tema dos últimos 30 posts.
4. Pesquise na web (WebSearch) 1 tema atual e relevante para empresas/trabalhadores no Brasil: NR-1/PGR/riscos psicossociais, NR-35, NR-12, NR-10, NR-18, laudos de insalubridade/periculosidade, perícia trabalhista, acessibilidade (NBR 9050), inspeção predial, acidentes de trabalho, prazos e mudanças de norma. Confirme datas e números em fonte oficial (gov.br/MTE, ABNT, Confea). Nunca invente dado, lei, prazo ou estatística.
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
