# Siargo MF5200 Modbus Reader

Este projeto Python oferece uma interface de comunicação e um aplicativo gráfico simples (GUI) para ler e controlar o Sensor de Vazão da Siargo, modelo MF5200, utilizando o protocolo Modbus RTU sobre comunicação serial (RS485/USB-Serial).

### Uso Principal

O código permite:

    Conectar ao sensor Siargo MF5200 via porta serial (ex: COM9, /dev/ttyUSB0).

    Ler o Fluxo Instantâneo (m3/h) e o Fluxo Acumulado (m3) do sensor.

    Enviar o comando para Resetar o fluxo acumulado do sensor.

    Fornecer uma interface gráfica (GUI) amigável para monitoramento e controle.

Observação: As fórmulas de cálculo e os endereços de registro Modbus (como 0x003A, 0x003B, 0x003C, 0x00FF, 0x00F2) são baseados em um entendimento específico do protocolo do sensor MF5200 e devem ser validados com o manual oficial do dispositivo.

### Pré-requisitos

Para rodar o projeto, você precisará ter o Python instalado e as seguintes bibliotecas:

    minimalmodbus: Para a comunicação Modbus.

    pyserial: Para a comunicação serial.

    tkinter: Para a interface gráfica (geralmente incluída no Python padrão).

Instalação das Dependências

Use pip para instalar as bibliotecas necessárias:

    pip install minimalmodbus pyserial

##### Requisitos Físicos

Para estabelecer a comunicação entre o computador e o sensor, é necessário:

- Sensor de Vazão Siargo MF5200.

- Conversor USB para RS485: Essencial para traduzir o sinal Modbus RTU da porta serial para USB.

- **Nota de Teste**: O conversor utilizado e validado durante o desenvolvimento deste código foi o Contemp D510. Garanta que o driver do seu conversor esteja corretamente instalado no sistema operacional (Windows/Linux) para que a porta serial (COMx ou ttyUSBx) seja reconhecida.

### Como Usar

    Conecte o Sensor: Certifique-se de que o sensor Siargo MF5200 esteja conectado ao seu computador por um conversor RS485 para USB/Serial e que a porta serial correta (ex: COM9 no Windows, /dev/ttyUSBx no Linux) esteja disponível.

    Execute o Aplicativo:
    Bash

python screen.py

Configurar e Iniciar:

   - Insira a Porta serial (ex: COM9).
    
   - Insira o ID Escravo (Slave ID) do seu sensor (padrão 1).

   - Insira o Intervalo de leitura em milissegundos (padrão 400).

   - Clique no botão "Start" para iniciar a leitura.

As leituras de Fluxo Instantâneo e Fluxo Acumulado serão atualizadas no painel. Use o botão "Reset Acumulado" para zerar o totalizador do sensor.

### Como Contribuir

Contribuições são bem-vindas! Se você encontrar um bug, tiver uma sugestão de recurso ou quiser aprimorar o código, por favor:

   - Faça um Fork do projeto.

   - Crie uma nova Branch (git checkout -b feature/sua-feature).

   - Faça seus Commits (git commit -m 'Adiciona feature X').

   - Faça um Push para a Branch (git push origin feature/sua-feature).

   - Abra um Pull Request detalhando suas alterações.