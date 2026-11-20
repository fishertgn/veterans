# Veterans Tarragona · publicador

Genera les imatges d'Instagram (@veteranstarragona) a partir de l'API oberta de MyGol i les envia a un bot de Telegram.
S'executa sol a GitHub Actions (`.github/workflows/publicar.yml`). Secrets necessaris: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

- `publicar.py` decideix què toca segons el dia i l'hora de Madrid i recorda què ha enviat a `estat.json`.
- `story.py` història de resultat · `proxims.py` pròxims partits · `resultats.py` · `classificacio.py` · `arrencada.py`.

## Calendari (hora de Catalunya)
- **Dijous des de les 7h**: pròxims partits a Telegram + històries i **post** a Instagram.
- **Divendres des de les 7h**: torna a mirar l'horari. Si ha canviat, nou post "HORARIS ACTUALITZATS" i històries dels dies canviats.
- **Divendres 14-24h, dissabte i diumenge 8-24h** (cada 30 min): història de cada partit acabat (Telegram + Instagram).
- **Dilluns 9h**: paquet setmanal a Telegram + **carrusel de resultats** (per competició) i **carrusel de classificacions** a Instagram.

Interruptors a `ig_auto.json`: `histories_resultats`, `histories_proxims`, `posts_proxims`, `posts_resultats` (posa `false` per aturar-ne un).
Es manté des del PC de casa (carpeta `C:\Users\luis\Claude\veterans-existent`), però s'executa sol a GitHub: no cal tenir cap ordinador encès.
