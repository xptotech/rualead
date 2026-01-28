import base64
import json
import requests
import time

# client_id = "u8EaG2BpzcUW".strip()
# client_secret = "nZSVV3KD5Nt3".strip()

## Precos e Indices
client_id = "KLCeH85la3po".strip()
client_secret = "arnpByHFa1UI".strip()

OAUTH_URL = "https://api.anbima.com.br/oauth/access-token"
#FUNDS_URL = "https://api-sandbox.anbima.com.br/mocks/feed/fundos/v2/fundos?size=1000"

##FUNDS_URL = "https://api-sandbox.anbima.com.br/mocks/feed/fundos/v2/fundos?tipo-fundo=FIAGRO&size=1000"
FUNDS_URL = "https://api-sandbox.anbima.com.br/feed/precos-indices/v1/titulos-publicos/mercado-secundario-TPF?data=2026-01-01"

# 1) Token
b64 = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
token_resp = requests.post(
    OAUTH_URL,
    headers={"Content-Type": "application/json", "Authorization": f"Basic {b64}"},
    json={"grant_type": "client_credentials"},
    timeout=60
)
token_resp.raise_for_status()
access_token = token_resp.json()["access_token"]

print("Token gerado. (preview):", access_token)
print("Token gerado. (preview):", access_token[:6] + "...")

# 2) Tentar chamadas com headers diferentes
candidates = [
    ("A) access_token apenas", {
        "Content-Type": "application/json",
        "access_token": access_token,
    }),
    ("B) client_id + access_token", {
        "Content-Type": "application/json",
        "client_id": client_id,
        "access_token": access_token,
    }),
    ("C) Authorization: Bearer", {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }),
]



last_err = None
for label, headers in candidates:
    try:
        r = requests.get(FUNDS_URL, headers=headers, timeout=60)
        if r.status_code == 200:
            print(f"\n✅ Funcionou com: {label}")
            print(json.dumps(r.json(), indent=2, ensure_ascii=False))
            print("1111111111")
            time.sleep(5)  # pausa por 5 segundos
            break
        else:
            print(f"❌ {label} -> HTTP {r.status_code}: {r.text[:200]}")
            last_err = (r.status_code, r.text)
            print("222222222222")
            time.sleep(5)  # pausa por 5 segundos
    except Exception as e:
        print(f"❌ {label} -> erro: {e}")
        last_err = e
        print("3333333333333")
        time.sleep(5)  # pausa por 5 segundos
else:
    raise RuntimeError(f"Nenhuma variação funcionou. Último erro: {last_err}")
