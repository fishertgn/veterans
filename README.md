# Veterans Tarragona · publicador

Genera les imatges d'Instagram (@veteranstarragona) a partir de l'API oberta de MyGol i les envia a un bot de Telegram.
S'executa sol a GitHub Actions (`.github/workflows/publicar.yml`). Secrets necessaris: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

- `publicar.py` decideix què toca segons el dia i l'hora de Madrid i recorda què ha enviat a `estat.json`.
- `story.py` història de resultat · `proxims.py` pròxims partits · `resultats.py` · `classificacio.py` · `arrencada.py`.
