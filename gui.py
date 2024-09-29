# gui.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QTableWidget, QTableWidgetItem, QTextEdit,
    QFileDialog, QDialog
)
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from simulation import Simulation
import networkx as nx

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASERA Model Simulation")
        self.simulation = Simulation()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.is_paused = True
        self.agent_details_windows = []

    def initUI(self):
        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Left panel: Controls and Statistics
        left_layout = QVBoxLayout()
        # Simulation Controls
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_simulation)
        self.stop_button.setEnabled(False)
        self.step_button = QPushButton("Step")
        self.step_button.clicked.connect(self.step_simulation)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_simulation)
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_simulation)
        left_layout.addWidget(QLabel("Simulation Controls"))
        left_layout.addWidget(self.start_button)
        left_layout.addWidget(self.stop_button)
        left_layout.addWidget(self.step_button)
        left_layout.addWidget(self.save_button)
        left_layout.addWidget(self.load_button)
        self.export_button = QPushButton("Export Data")
        self.export_button.clicked.connect(self.export_data)
        left_layout.addWidget(self.export_button)

        # Parameter Adjustment
        self.param_slider = QSlider(Qt.Horizontal)
        self.param_slider.setMinimum(0)
        self.param_slider.setMaximum(100)
        self.param_slider.setValue(50)
        self.param_slider.valueChanged.connect(self.update_parameter)
        left_layout.addWidget(QLabel("Parameter Adjustment"))
        left_layout.addWidget(self.param_slider)

        # Statistics Panel
        left_layout.addWidget(QLabel("Statistics"))
        self.stats_label = QLabel("Average Wealth: \nGini Coefficient: \nAverage Competence: ")
        left_layout.addWidget(self.stats_label)

        # Log Panel
        left_layout.addWidget(QLabel("Log"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        left_layout.addWidget(self.log_text)

        # Middle panel: Agent Dashboard
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(QLabel("Agent Status Dashboard"))
        self.agent_table = QTableWidget()
        self.agent_table.setColumnCount(5)
        self.agent_table.setHorizontalHeaderLabels(["ID", "Wealth", "Influence", "Competence", "Self-Esteem"])
        self.agent_table.itemSelectionChanged.connect(self.agent_selected)
        middle_layout.addWidget(self.agent_table)

        # Right panel: Graphs and Network
        right_layout = QVBoxLayout()
        # Dynamic Graphs
        right_layout.addWidget(QLabel("Dynamic Graphs"))
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas)
        # Network Visualization
        right_layout.addWidget(QLabel("Network Visualization"))
        self.network_figure = Figure(figsize=(5, 3))
        self.network_canvas = FigureCanvas(self.network_figure)
        right_layout.addWidget(self.network_canvas)

        # Assemble layouts
        main_layout.addLayout(left_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(right_layout)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def export_data(self):
        filename_prefix, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "CSV Files (*.csv)")
        if filename_prefix:
            if not self.simulation.time_series:
                self.log("No data available to export. Please run the simulation for some time steps before exporting.")
                return
            # Check if agent histories have data
            empty_agents = [agent_id for agent_id, history in self.simulation.agent_histories.items() if not history['W']]
            if empty_agents:
                self.log(f"No data collected for agents: {empty_agents}. Please ensure the simulation is running correctly.")
                return
            # Remove the .csv extension if present, as the method adds it
            if filename_prefix.endswith('.csv'):
                filename_prefix = filename_prefix[:-4]
            try:
                self.simulation.export_data(filename_prefix)
                self.log(f"Data exported successfully with prefix '{filename_prefix}'.")
            except Exception as e:
                self.log(f"Error exporting data: {e}")

    def start_simulation(self):
        if self.is_paused:
            self.simulation.start()
            self.timer.start(1000)  # Update every second
            self.start_button.setText("Pause")
            self.stop_button.setEnabled(True)
            self.step_button.setEnabled(False)
            self.is_paused = False
            self.log("Simulation started.")
        else:
            self.simulation.pause()
            self.timer.stop()
            self.start_button.setText("Resume")
            self.step_button.setEnabled(True)
            self.is_paused = True
            self.log("Simulation paused.")

    def stop_simulation(self):
        self.simulation.stop()
        self.timer.stop()
        self.start_button.setText("Start")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.step_button.setEnabled(True)
        self.is_paused = True
        self.log("Simulation stopped.")

    def step_simulation(self):
        self.simulation.step()
        self.update_simulation()
        self.log("Simulation stepped.")

    def update_parameter(self, value):
        # Adjust a simulation parameter based on slider value
        self.simulation.adjust_parameter(value)
        self.log(f"Parameter adjusted to {value}.")

    def update_simulation(self):
        # Update simulation state
        self.simulation.update()
        # Update GUI elements
        self.update_agent_table()
        self.update_stats()
        self.update_graphs()
        self.update_network()

    def update_agent_table(self):
        agents = self.simulation.get_agents()
        self.agent_table.setRowCount(len(agents))
        for i, agent in enumerate(agents):
            self.agent_table.setItem(i, 0, QTableWidgetItem(str(agent.agent_id)))
            self.agent_table.setItem(i, 1, QTableWidgetItem(f"{agent.W:.2f}"))
            self.agent_table.setItem(i, 2, QTableWidgetItem(f"{agent.I:.2f}"))
            self.agent_table.setItem(i, 3, QTableWidgetItem(f"{agent.C:.2f}"))
            self.agent_table.setItem(i, 4, QTableWidgetItem(f"{agent.S:.2f}"))

    def agent_selected(self):
        selected_items = self.agent_table.selectedItems()
        if selected_items:
            agent_id = float(selected_items[0].text())
            self.show_agent_details(agent_id)

    def show_agent_details(self, agent_id):
        agent = self.simulation.get_agent_by_id(agent_id)
        if agent:
            time_series = self.simulation.get_time_series()
            agent_window = AgentDetailsWindow(agent, time_series)
            self.agent_details_windows.append(agent_window)
            agent_window.show()
        else:
            print(f"No agent found with ID: {agent_id}")

    def update_stats(self):
        avg_wealth = self.simulation.get_average_wealth()
        gini = self.simulation.get_gini_coefficient()
        avg_competence = self.simulation.get_average_competence()
        self.stats_label.setText(f"Average Wealth: {avg_wealth:.2f}\nGini Coefficient: {gini:.2f}\nAverage Competence: {avg_competence:.2f}")

    def update_graphs(self):
        # Update dynamic graphs
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        time = self.simulation.get_time_series()
        wealth = self.simulation.get_wealth_time_series()
        ax.plot(time, wealth, label='Average Wealth')
        ax.set_title("Average Wealth Over Time")
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Wealth")
        ax.legend()
        self.canvas.draw()

    def update_network(self):
        # Update network visualization
        self.network_figure.clear()
        ax = self.network_figure.add_subplot(111)
        G = self.simulation.get_network()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=ax, node_size=20, with_labels=False)
        self.network_canvas.draw()

    def save_simulation(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Simulation", "", "Simulation Files (*.sim)")
        if filename:
            self.simulation.save_simulation(filename)
            self.log(f"Simulation saved to {filename}.")

    def load_simulation(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Simulation", "", "Simulation Files (*.sim)")
        if filename:
            self.simulation = Simulation.load_simulation(filename)
            self.log(f"Simulation loaded from {filename}.")
            self.update_simulation()

    def log(self, message):
        self.log_text.append(message)

class AgentDetailsWindow(QDialog):
    def __init__(self, agent, time_series):
        super().__init__()
        self.setWindowTitle(f"Agent {agent.agent_id} Details")
        self.agent = agent
        self.time_series = time_series
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create matplotlib Figure and Canvas
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        # Plot agent's historical data
        self.plot_agent_history()

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_agent_history(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # Get agent's history
        history = self.agent.history
        time = self.time_series
        ax.plot(time, history['W'], label='Wealth')
        ax.plot(time, history['I'], label='Influence')
        ax.plot(time, history['C'], label='Competence')
        ax.plot(time, history['AS'], label='Agent Status')
        ax.set_title(f"Agent {self.agent.agent_id} Variables Over Time")
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Value")
        ax.legend()
        self.canvas.draw()
