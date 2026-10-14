# HyperFrames (teste)

[HyperFrames](https://github.com/heygen-com/hyperframes), da HeyGen, licença **Apache 2.0**. Ele transforma HTML com animação GSAP em MP4, quadro a quadro, sempre igual.

Por enquanto é só um teste. Os vídeos da Synex continuam saindo do motor próprio, em `instagram/video/`.

## O que tem aqui

- `salao/index.html`: o Reel "Salão sem página?" passado do nosso motor (`render(t)`) para uma composição HyperFrames, com timeline GSAP. Usa a mesma narração, as mesmas legendas, as mesmas fontes e o mesmo visual.
- `comparacao-salao.mp4` (fica fora do git): os dois lado a lado.

## Como rodar (nuvem)

```bash
npm i hyperframes@0.8.156 gsap@3.14.2        # numa pasta qualquer
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
cp ../video/modelos/anuncio-captacao-c/audio.wav salao/narracao.wav
cp <node_modules>/gsap/dist/gsap.min.js salao/
cd salao && npx hyperframes check && npx hyperframes render --output salao-hyperframes.mp4 --fps 30
```

No PC (Windows), o `npx hyperframes browser ensure` baixa o Chrome sozinho.

## Resultado do teste (14/10/2026)

- **Visual:** os quadros saíram praticamente iguais aos do nosso motor.
- **Tempo de render:** 2 min 40 s no HyperFrames contra 2 min 14 s no nosso motor. Aqui na nuvem ele usa o modo mais lento ("screenshot" com GPU por software).
- **O que o `hyperframes check` pegou sozinho:** texto escondido atrás de outro elemento, contraste abaixo de 4,5:1 num rótulo e a duração do áudio diferente da composição.
- **O que ele não pegou:** um círculo de toque que aparecia antes da hora (efeito do `fromTo` do GSAP). Achei olhando os quadros.

## Créditos e licença

O HyperFrames é Apache 2.0. Pode usar e modificar, inclusive em trabalho comercial, desde que se mantenham o aviso de licença e os créditos quando o código dele for redistribuído. Aqui ele é usado como ferramenta instalada pelo npm; não copiamos código dele para o repositório. A composição `salao/index.html` é nossa. GSAP: licença "Standard" da GreenSock (Webflow), uso gratuito.
