"""Configura uma instalação do Easy!Appointments (com white-label.patch) para um cliente.

Uso:
    EA_URL=https://agenda.cliente.com.br EA_TOKEN=<token da API> EA_DIR=/var/www/agenda \
        python3 configurar_cliente.py clientes/<cliente>/cliente.json

O token da API é definido em Configurações > Integrações > API no painel (ou na
tabela ea_settings, campo api_token). Nada aqui guarda senhas: as senhas das
profissionais são geradas aleatoriamente e elas definem a própria pelo "Esqueceu a senha?".
"""
import hashlib
import json
import os
import secrets
import sys
import urllib.request
from pathlib import Path

URL = os.environ.get("EA_URL", "http://localhost:8080").rstrip("/") + "/index.php/api/v1/"
TOKEN = os.environ["EA_TOKEN"]


def api(method, path, body=None):
    req = urllib.request.Request(URL + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def plano(h):
    dias = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    out = {}
    for d in dias:
        v = h.get(d)
        out[d] = None if not v else {"start": v[0], "end": v[1],
                                     "breaks": [{"start": b[0], "end": b[1]} for b in (v[2] if len(v) > 2 else [])]}
    return out


def main(cfg_path):
    cfg_path = Path(cfg_path)
    c = json.loads(cfg_path.read_text(encoding="utf-8"))
    wp = plano(c["horario"])

    # Logo: a API filtra "data:" (anti-XSS), então o arquivo vai para a pasta da
    # instalação (EA_DIR) e o ajuste aponta para a URL dele. Também vira favicon
    # e o logo dos e-mails.
    logo = cfg_path.parent / c["logo"]
    logo_url = ""
    ea_dir = os.environ.get("EA_DIR")
    if ea_dir:
        from PIL import Image
        img = Path(ea_dir) / "assets" / "img"
        im = Image.open(logo).convert("RGBA")
        im.save(img / "logo.png")
        im.resize((16, 16)).save(img / "logo-16x16.png")
        im.save(img / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
        versao = hashlib.md5(logo.read_bytes()).hexdigest()[:8]
        logo_url = URL.split("/index.php/")[0] + f"/assets/img/logo.png?v={versao}"
    else:
        print("Aviso: defina EA_DIR para instalar o logo; ou envie pelo painel (Configurações > Geral).")
    ajustes = {
        "company_name": c["nome"], "company_email": c["email"], "company_link": c.get("site", ""),
        "company_color": c["cor"], "company_logo": logo_url,
        "company_working_plan": json.dumps(wp), "default_language": "portuguese-br",
        "default_timezone": "America/Sao_Paulo", "date_format": "DMY", "time_format": "military",
        "first_weekday": "monday", "display_address": "0", "display_city": "0", "display_zip_code": "0",
        "require_email": "0", "display_login_button": "0", "book_advance_timeout": "60",
    }
    for k, v in ajustes.items():
        api("PUT", f"settings/{k}", {"value": v})

    # Remove os dados de exemplo que a instalação cria (Service, Jane Doe, James Doe)
    for s in api("GET", "services?length=500") or []:
        if s["name"] == "Service":
            api("DELETE", f"services/{s['id']}")
    for kind, nome in (("providers", "Jane"), ("customers", "James")):
        for u in api("GET", f"{kind}?length=500") or []:
            if u.get("firstName") == nome and u.get("lastName") == "Doe":
                api("DELETE", f"{kind}/{u['id']}")

    cats = {}
    for cat in sorted({s["categoria"] for s in c["servicos"]}):
        cats[cat] = api("POST", "service_categories", {"name": cat, "description": ""})["id"]
    ids = {}
    for s in c["servicos"]:
        ids[s["nome"]] = api("POST", "services", {
            "name": s["nome"], "duration": s["minutos"], "price": s["preco"], "currency": "R$",
            "location": c.get("endereco", ""), "description": s.get("descricao", ""), "color": s.get("cor", c["cor"]),
            "slotInterval": 15, "attendantsNumber": 1, "isPrivate": False, "serviceCategoryId": cats[s["categoria"]]})["id"]
    for p in c["profissionais"]:
        api("POST", "providers", {
            "firstName": p["nome"], "lastName": p.get("sobrenome", ""), "email": p["email"],
            "phone": p.get("telefone", ""), "timezone": "America/Sao_Paulo", "language": "portuguese-br",
            "isPrivate": False, "services": [ids[n] for n in p["servicos"]],
            "settings": {"username": p["usuario"], "password": secrets.token_urlsafe(14), "notifications": True,
                         "calendarView": "default", "googleSync": False, "syncFutureDays": 90, "syncPastDays": 30,
                         "workingPlan": plano(p.get("horario", c["horario"])), "workingPlanExceptions": {}}})
    print(f"{c['nome']}: {len(ids)} serviços, {len(c['profissionais'])} profissionais.")


if __name__ == "__main__":
    main(sys.argv[1])
