# Documentação da Classe SensorApp (app.py)

A classe SensorApp estende tkinter.Tk e implementa a interface gráfica (GUI) para interagir com a classe Sensor, permitindo o monitoramento contínuo das leituras do sensor Siargo MF5200.

##### Definição da Classe:

    class SensorApp(tk.Tk):
    def __init__(self):
    ...
    def _build_ui(self):
    ...
    def start(self):
    ...
    def stop(self):
    ...
    def reset_accumulated(self):
    ...
    def _read_loop(self):
    ...
    def _on_close(self):
    ...

## Interface Gráfica (UI)

### A aplicação é dividida em três seções principais:

   - Configuração (Top): Controles para Porta Serial, ID Escravo e Intervalo de leitura.

   - Leituras (Mid): Exibe o Fluxo Instantâneo (m3/h) e o Fluxo Acumulado (m3) lidos.

   - Controles e Status (Bot): Exibe o Status da comunicação e os botões Start, Stop e Reset Acumulado.

## Métodos Funcionais

### 1. start(self)

Inicia a comunicação com o sensor.

   - Validação: Verifica se já existe um loop de leitura ativo (self._job).

   - Inicialização: Tenta criar uma instância da classe Sensor usando a porta e o ID fornecidos na GUI.

   - Loop de Leitura: Agenda a primeira execução do método _read_loop após 100ms.

   - Tratamento de Erros: Se a inicialização do Sensor falhar (ex: porta serial inexistente ou em uso), exibe um alerta e atualiza o status.

### 2. stop(self)

Encerra o loop de leitura periódico.

   - Cancela a próxima execução agendada do _read_loop usando self.after_cancel(self._job).

   - Define a variável de status da GUI para "Parado".

### 3. reset_accumulated(self)

Invoca a função de reset do sensor.

   - Pré-condição: Verifica se o objeto self.sensor foi inicializado.

   - Chama o método self.sensor.reset_accumulated_flow_rate().

   - Feedback: Em caso de sucesso, atualiza o status. Em caso de falha (ex: erro Modbus), exibe uma mensagem de erro na GUI e no log.

### 4. _read_loop(self)

O coração do monitoramento contínuo.

   - Leitura: Tenta ler o fluxo instantâneo e acumulado chamando self.sensor.get_intent_flow_rate() e self.sensor.get_accumulated_flow().

   - Atualização da GUI: Atualiza as variáveis instant_flow_var e accumulated_flow_var na GUI com os valores lidos, formatados para duas casas decimais.

   - Status: Atualiza o status com o horário da última leitura bem-sucedida.

   - Tratamento de Exceções: Captura exceções comuns do minimalmodbus (NoResponseError, ModbusException) e outros erros, atualizando a variável de status da GUI com a mensagem de erro apropriada para feedback ao usuário.

   - Agendamento: Agenda a próxima execução de _read_loop usando self.after(interval, self._read_loop), com o intervalo definido pelo usuário (mínimo de 100ms).

### 5. _on_close(self)

Método chamado ao tentar fechar a janela.

   - Exibe uma caixa de diálogo de confirmação.

   - Se o usuário confirmar, chama self.stop() para interromper o loop e self.destroy() para fechar a aplicação.