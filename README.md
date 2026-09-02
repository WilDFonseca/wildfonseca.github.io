# Wildney Fonseca — Consultoria de TI & IA

Landing page estática em Vue 3 (CDN), preparada para GitHub Pages.

## Antes de publicar

- Em `index.html`, procure `const calUrl='https://cal.com/wildneyfonseca'` e troque pela URL/event type real do seu Cal.com.
- Confirme o e-mail `contato@wildneyfonseca.com.br` no rodapé.
- O WhatsApp está configurado para o número usado no CV; altere `whatsappNumber` se necessário.

## Publicar no GitHub Pages

1. Crie um repositório, por exemplo `wildneyfonseca.com.br`.
2. Envie todos os arquivos desta pasta para a branch `main`.
3. Em Settings → Pages, escolha **GitHub Actions** como source.
4. O workflow `.github/workflows/pages.yml` fará o deploy.
5. O arquivo `CNAME` já aponta para `wildneyfonseca.com.br`.
6. No DNS do domínio, aponte o apex para os IPs do GitHub Pages ou use a configuração recomendada pelo GitHub. Depois, ative HTTPS.

## Observações

- A página não precisa de Node/npm para publicar: Vue e Lucide carregam por CDN.
- O formulário não precisa de backend: ele abre o WhatsApp com uma mensagem preenchida.
- O botão de agendamento abre o Cal.com dentro de um modal via iframe, com fallback para nova aba.
