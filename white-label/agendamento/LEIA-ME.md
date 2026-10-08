# Agenda online white label (salão, barbearia, clínica)

Este piloto é a agenda online do **Studio Carla**, um salão fictício de Peruíbe, feita com a marca do cliente e o selo "Agenda online por Synex Local". As telas estão em `clientes/studio-carla/telas-cliente.png` e `telas-painel.png`.

## Base

- **Sistema:** [Easy!Appointments](https://github.com/alextselegidis/easyappointments) **1.6.0**, em PHP + MySQL.
- **Licença:** GPL-3.0. Pode modificar, trocar a marca e cobrar pela hospedagem e pelo serviço.
- **O que a GPL pede:**
  - Hospedar o sistema para o cliente não é "distribuir", então não obriga a entregar o código.
  - Se um dia **entregarem os arquivos** do sistema a alguém, as modificações vão junto, também sob GPL.
  - Mantemos o aviso legal (copyright do autor e link da GPL) no rodapé do painel e na página "Sobre".
- **Marca:** o nome "Easy!Appointments" não aparece para o cliente final. Só fica o aviso legal, no painel.

**O cliente final ganha:**
- página de agendamento com serviços, preços, profissionais e horários livres;
- painel com agenda por profissional, clientes e serviços;
- e-mails de confirmação.

## O que o `white-label.patch` muda

1. Marca do cliente em tudo: logo, nome, cor (Configurações > Geral), título da aba e favicon.
2. Rodapés trocados por "Agenda online por Synex Local", na página do cliente final, na confirmação, no login, no painel e nos e-mails. O item "Premium" do menu sai.
3. Visual próprio: `assets/css/white-label.scss` para a página de agendamento e `white-label-backend.scss` para o painel.
   - Fontes DM Serif Display e Manrope (licença OFL), servidas localmente.
   - Botões arredondados na cor da marca.
4. Português revisado:
   - "profissional" em vez de "atendente";
   - "Continuar" em vez de "Seguinte";
   - "Nome" e "Sobrenome";
   - "Painel do salão";
   - correção de erros de digitação.
5. Preço no formato brasileiro: "R$ 80,00".
6. Simplificações para o público local: sem seletor de idioma e sem fuso horário.

## Instalar para um cliente novo

```bash
git clone --depth 1 --branch 1.6.0 https://github.com/alextselegidis/easyappointments.git agenda
cd agenda && git apply ../white-label.patch
composer install --no-dev && npm install && npx gulp compile
cp config-sample.php config.php    # BASE_URL, LANGUAGE=portuguese-br, dados do MySQL
# abra BASE_URL/index.php/installation e crie o admin (o dono do comércio)
# no painel: Configurações > Integrações > API > defina um token
EA_URL=<BASE_URL> EA_TOKEN=<token> EA_DIR=$(pwd) python3 ../configurar_cliente.py ../clientes/<cliente>/cliente.json
```

O `cliente.json` reúne nome, cor, logo, endereço, horário de funcionamento, serviços (duração, preço, categoria) e profissionais. Use `clientes/studio-carla/cliente.json` como modelo. As profissionais recebem senha aleatória e criam a delas pelo "Esqueceu a senha?". Para isso, o envio de e-mail (SMTP) precisa estar configurado em `application/config/email.php`.

## Antes de vender (pendências)

- **Hospedagem:** uma instalação por cliente (subdomínio, por exemplo `agenda.cliente.com.br`) em uma VPS com PHP e MySQL. Ou uma instalação por cliente na mesma VPS, separada por pasta e banco.
- **Rotina:** backup diário do banco, atualização de segurança e SMTP para os e-mails.
- **WhatsApp:** dá para ligar o lembrete por WhatsApp pelos webhooks do sistema (Configurações > Webhooks) ao n8n e à Evolution API que vocês já usam.
- **LGPD:** a página precisa de política de privacidade (o sistema já tem os campos para isso).
