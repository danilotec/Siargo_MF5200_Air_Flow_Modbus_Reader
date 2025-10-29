# Documentação da Classe Sensor (sensor.py)

A classe Sensor encapsula toda a lógica de comunicação Modbus RTU com o medidor de vazão Siargo MF5200. Ela utiliza a biblioteca minimalmodbus para gerenciar a interface serial e as requisições Modbus.

##### Definição da Classe:

    class Sensor:
        def __init__(self, port: str, address: int) -> None:
         ...
        def __read_register_value(self, register_value: int) -> int | float:
         ...
        def get_intent_flow_rate(self) -> int | float:
         ...
        def get_accumulated_flow(self) -> int | float:
         ...
        def __disable_write_protection(self) -> bool:
         ...
        def reset_accumulated_flow_rate(self) -> bool:
         ...

#### Métodos e Propriedades

##### 1. __init__(self, port: str, address: int) -> None

    Parâmetro	Tipo	Descrição
    port	str	Porta serial (ex: "COM9", "/dev/ttyUSB0").
    address	int	Endereço (Slave ID) do dispositivo Modbus (ex: 1).

Descrição: O construtor inicializa o objeto minimalmodbus.Instrument e configura os parâmetros de comunicação serial, que são padrão para Modbus RTU, com base nas especificações usuais de fábrica:

    baudrate: 9600

    bytesize: 8

    parity: serial.PARITY_NONE

    stopbits: 1

    timeout: 1 segundo

    mode: minimalmodbus.MODE_RTU

##### 2. __read_register_value(self, register_value: int) -> int | float

Parâmetro	Tipo	Descrição
register_value	int	O endereço hexadecimal do registro (ex: 0x003A).

Descrição: Método auxiliar privado (__) para ler um único Holding Register do dispositivo.

    numberOfDecimals: 2 (Assume-se que 2 casas decimais são necessárias para a escala).

    functioncode: 3 (Código de função para Read Holding Registers).

    signed: False (Assume-se que o valor não é assinado).

    Retorna o valor lido, já formatado com as casas decimais.

##### 3. get_intent_flow_rate(self) -> int | float

Endereços Lidos: 0x003A e 0x003B.

Descrição: Lê e calcula o Fluxo Instantâneo (Instantaneous Flow Rate) do sensor. O sensor usa dois registros (32 bits) para representar o valor do fluxo.

Fórmula de Cálculo:
$$\text{air\_flow} = \frac{(\text{raw\_value\_a} \times 65536) + \text{raw\_value\_b}}{10} $$A conversão final para o valor em $m^3/h$ é feita por um fator de ajuste: $$\text{air\_flow\_m3} = \text{air\_flow} \times 0.06 $$Retorna o fluxo instantâneo em $m^3/h$. 

##### 4. get_accumulated_flow(self) -> int | float 

Endereços Lidos: 0x003C, 0x003D e 0x003E.

 Descrição: Lê e calcula o Fluxo Acumulado (Accumulated Flow) do sensor, que utiliza três registros (48 bits ou formato customizado). 

Fórmula de Cálculo:
$$
\text{Accumulated Flow} = (\text{Raw}_C \times 65536) + (\text{Raw}_D \times 100) + \frac{\text{Raw}_E}{10}
$$

 
Retorna o fluxo acumulado em m3.

##### 5. __disable_write_protection(self) -> bool

Endereço Escrito: 0x00FF. Valor Escrito: 0xAA55. Function Code: 6 (Código de função para Write Single Register).

Descrição: Método privado para enviar o código mágico (0xAA55) para o registro 0x00FF, que geralmente é um passo necessário para desativar a proteção contra escrita antes de executar um comando de controle, como o reset.

##### 6. reset_accumulated_flow_rate(self) -> bool

Endereço Escrito: 0x00F2. Valor Escrito: 0x0001. Function Code: 6 (Código de função para Write Single Register).

Descrição: Chama o método __disable_write_protection() e, em seguida, envia o comando de reset (0x0001) para o registro específico (0x00F2) responsável por zerar o totalizador de fluxo acumulado do sensor. Retorna True em caso de sucesso e False em caso de erro.