import tkinter as tk
from tkinter import ttk, messagebox
import logging
import minimalmodbus
import time
from sensor import Sensor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SensorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sensor de Vazão - Modbus")
        self.geometry("380x250")
        self.resizable(False, False)

        self.port_var = tk.StringVar(value="COM9")
        self.slave_var = tk.IntVar(value=1)
        self.interval_var = tk.IntVar(value=400) 
        self.status_var = tk.StringVar(value="Parado")
        self.instant_flow_var = tk.StringVar(value="--")
        self.accumulated_flow_var = tk.StringVar(value="--")

        self.sensor = None
        self._job = None

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 8, "pady": 6}

        frame_top = ttk.Frame(self)
        frame_top.pack(fill="x", **pad) #type: ignore

        ttk.Label(frame_top, text="Porta (COM/tty):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame_top, textvariable=self.port_var, width=12).grid(row=0, column=1, sticky="w")

        ttk.Label(frame_top, text="ID Escravo:").grid(row=0, column=2, sticky="w", padx=(10,0))
        ttk.Spinbox(frame_top, from_=1, to=247, textvariable=self.slave_var, width=6).grid(row=0, column=3, sticky="w")

        ttk.Label(frame_top, text="Intervalo (ms):").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame_top, textvariable=self.interval_var, width=12).grid(row=1, column=1, sticky="w")


        frame_mid = ttk.LabelFrame(self, text="Leituras")
        frame_mid.pack(fill="x", **pad) #type: ignore

        ttk.Label(frame_mid, text="Fluxo Instantâneo (m³/h):").grid(row=0, column=0, sticky="w")
        ttk.Label(frame_mid, textvariable=self.instant_flow_var, font=("Segoe UI", 12, "bold")).grid(row=0, column=1, sticky="e")

        ttk.Label(frame_mid, text="Fluxo Acumulado (m³):").grid(row=1, column=0, sticky="w")
        ttk.Label(frame_mid, textvariable=self.accumulated_flow_var, font=("Segoe UI", 12, "bold")).grid(row=1, column=1, sticky="e")

        frame_bot = ttk.Frame(self)
        frame_bot.pack(fill="x", **pad) #type: ignore

        ttk.Label(frame_bot, text="Status:").grid(row=0, column=0, sticky="w")
        ttk.Label(frame_bot, textvariable=self.status_var).grid(row=0, column=1, sticky="w")

        btn_start = ttk.Button(frame_bot, text="Start", command=self.start)
        btn_start.grid(row=1, column=0, sticky="ew", pady=(8,0))
        btn_stop = ttk.Button(frame_bot, text="Stop", command=self.stop)
        btn_stop.grid(row=1, column=1, sticky="ew", pady=(8,0), padx=(6,0))

        btn_quit = ttk.Button(self, text="Fechar", command=self._on_close)
        btn_quit.pack(side="bottom", pady=(0,8))

    def start(self):
        if self._job:
            return
        port = self.port_var.get().strip()
        slave = int(self.slave_var.get())
        try:
            self.sensor = Sensor(port, slave)
            self.status_var.set(f"Conectando {port} (slave {slave})...")
            self.after(100, self._read_loop)
        except Exception as e:
            logging.exception("Erro ao instanciar sensor")
            messagebox.showerror("Erro", f"Não foi possível conectar ao sensor:\n{e}")
            self.status_var.set("Erro ao conectar")

    def stop(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.status_var.set("Parado")

    def _read_loop(self):
        """Loop que faz a leitura e agenda a próxima execução."""
        if not self.sensor:
            self.status_var.set("Sensor não inicializado")
            return

        try:
            instant = self.sensor.get_intent_flow_rate()
            accumulated = self.sensor.get_accumulated_flow()

            if instant is None:
                self.instant_flow_var.set("--")
            else:
                self.instant_flow_var.set(f"{instant:.2f}")

            if accumulated is None:
                self.accumulated_flow_var.set("--")
            else:
                self.accumulated_flow_var.set(f"{accumulated:.2f}")

            self.status_var.set(f"Última leitura: {time.strftime('%H:%M:%S')}")
        except minimalmodbus.NoResponseError:
            logging.warning("Sem resposta do sensor")
            self.status_var.set("Sem resposta do sensor")
        except minimalmodbus.ModbusException as e:
            logging.warning(f"Erro Modbus: {e}")
            self.status_var.set(f"Erro Modbus: {e}")
        except Exception as e:
            logging.exception("Erro inesperado ao ler sensor")
            self.status_var.set(f"Erro: {e}")

        interval = max(100, int(self.interval_var.get()))
        self._job = self.after(interval, self._read_loop)

    def _on_close(self):
        if messagebox.askokcancel("Sair", "Encerrar aplicação?"):
            self.stop()
            self.destroy()


if __name__ == "__main__":
    app = SensorApp()
    app.mainloop()
