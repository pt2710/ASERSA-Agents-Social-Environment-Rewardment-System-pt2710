import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QTableWidget, QTableWidgetItem, QTextEdit,
    QFileDialog, QDialog, QScrollArea, QComboBox
)
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from simulation import Simulation
import networkx as nx
import ctypes
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GUI Parameter Sliders (Initial Values)
K6 = 0.01
K7 = 0.1
COPT = 100
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASERSA Simulation Tool")
        self.simulation = Simulation(0)
        self.zoom_factor = 1.0
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        self.resize(window_width, window_height)
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.is_paused = True
        self.agent_details_windows = []
        self.zoom_factor = 1.0
        logger.info("GUI initialized.")

    def initUI(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Left panel: Controls and Statistics
        left_layout = QVBoxLayout()
        
        # Create a scroll area for the sliders
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Create a widget to hold the sliders
        slider_widget = QWidget()
        slider_layout = QVBoxLayout(slider_widget)

        slider_layout.addWidget(QLabel("Ambition Proportion"))
        self.k6_slider = QSlider(Qt.Horizontal)
        self.k6_slider.setMinimum(1)
        self.k6_slider.setMaximum(1000)
        self.k6_slider.setValue(int(K6 * 1000))
        self.k6_slider.valueChanged.connect(self.update_k6)
        slider_layout.addWidget(self.k6_slider)

        slider_layout.addWidget(QLabel("Learning Rate for Competence"))
        self.k7_slider = QSlider(Qt.Horizontal)
        self.k7_slider.setMinimum(1)
        self.k7_slider.setMaximum(1000)
        self.k7_slider.setValue(int(K7 * 1000))
        self.k7_slider.valueChanged.connect(self.update_k7)
        slider_layout.addWidget(self.k7_slider)

        slider_layout.addWidget(QLabel("Flat Tax Rate (%)"))
        self.flat_tax_slider = QSlider(Qt.Horizontal)
        self.flat_tax_slider.setMinimum(0)
        self.flat_tax_slider.setMaximum(100)
        self.flat_tax_slider.setValue(int(self.simulation.FLAT_TAX_RATE * 100))  # Convert to percentage
        self.flat_tax_slider.valueChanged.connect(self.update_flat_tax_rate)
        slider_layout.addWidget(self.flat_tax_slider)

        # Set the slider widget as the scroll area's widget
        scroll_area.setWidget(slider_widget)

        # Add the scroll area to the left layout
        left_layout.addWidget(scroll_area)

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

        # Export Data Button
        self.export_button = QPushButton("Export Data")
        self.export_button.clicked.connect(self.export_data)
        left_layout.addWidget(self.export_button)

        # Tax Policy Selection
        left_layout.addWidget(QLabel("Tax Policy"))
        self.policy_combo = QComboBox()
        self.policy_combo.addItems(['flat', 'ubi', 'progressive'])
        left_layout.addWidget(self.policy_combo)
        self.apply_policy_button = QPushButton("Apply Policy")
        self.apply_policy_button.clicked.connect(self.apply_policy_from_gui)
        left_layout.addWidget(self.apply_policy_button)

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
        self.agent_table.setColumnCount(6)
        self.agent_table.setHorizontalHeaderLabels(["ID", "Type 1 Tokens", "Type 2 Tokens", "AI", "AS", "C"])
        self.agent_table.itemSelectionChanged.connect(self.agent_selected)
        middle_layout.addWidget(self.agent_table)

        # Right panel: Graphs and Network
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Dynamic Graphs"))
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas)
        
        # Network Visualization
        right_layout.addWidget(QLabel("Network Visualization"))
        self.network_figure = Figure(figsize=(5, 3))
        self.network_canvas = FigureCanvas(self.network_figure)
        self.reset_button = QPushButton("Reset View")
        self.reset_button.clicked.connect(self.reset_view)
        right_layout.addWidget(self.reset_button)
        right_layout.addWidget(self.network_canvas)

        # Assemble layouts
        main_layout.addLayout(left_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(right_layout)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def apply_policy_from_gui(self):
        policy_name = self.policy_combo.currentText()
        # Ensure total_tax_collected is a dictionary
        if not isinstance(self.simulation.total_tax_collected, dict):
            self.simulation.total_tax_collected = {k: 0 for k in self.simulation.agents[0].tokens.keys()}
        self.simulation.apply_policy(policy_name)
        self.log(f"Applied tax policy: {policy_name}")

    def export_data(self):
        try:
            if not self.simulation.time_series:
                self.log("No data available to export. Please run the simulation for some time steps before exporting.")
                return
            export_dir = os.path.join("simulation_data", "exported_data")
            os.makedirs(export_dir, exist_ok=True)
            self.simulation.export_data()
            self.save_plots()
            self.log("Data and plots exported successfully.")
        except Exception as e:
            self.log(f"Error exporting data: {e}")

    def save_plots(self):
        export_dir = os.path.join("simulation_data", "exported_plots")
        os.makedirs(export_dir, exist_ok=True)
        dynamic_plot_path = os.path.join(export_dir, "average_wealth_over_time.png")
        self.figure.savefig(dynamic_plot_path)
        network_plot_path = os.path.join(export_dir, "network_visualization.png")
        self.network_figure.savefig(network_plot_path)
        self.log(f"Plots saved to {export_dir}.")

    def start_simulation(self):
        if self.is_paused:
            self.simulation.start()
            self.timer.start(1000)
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

    def update_k6(self):
        global K6
        K6 = self.k6_slider.value() / 100.0
        self.log(f"Ambition proportion adjusted to {K6}")

    def update_k7(self):
        global K7
        K7 = self.k7_slider.value() / 100.0
        self.log(f"Competence learning rate adjusted to {K7}")

    def update_flat_tax_rate(self, value):
        self.simulation.FLAT_TAX_RATE = value / 100.0  # Convert from percentage to decimal
        self.log(f"Flat tax rate adjusted to {self.simulation.FLAT_TAX_RATE:.2%}")

    def update_simulation(self):
        self.simulation.update()
        self.update_agent_table()
        self.update_stats()  # Make sure this is called
        self.update_graphs()
        self.update_network()

    def update_agent_table(self):
        self.agents = self.simulation.get_agents()
        self.agent_table.setRowCount(len(self.agents))
        for i, agent in enumerate(self.agents):
            self.agent_table.setItem(i, 0, QTableWidgetItem(str(agent.agent_id)))
            self.agent_table.setItem(i, 1, QTableWidgetItem(f"{agent.tokens.get('type 1', 0):.2f}"))
            self.agent_table.setItem(i, 2, QTableWidgetItem(f"{agent.tokens.get('type 2', 0):.2f}"))
            self.agent_table.setItem(i, 3, QTableWidgetItem(f"{agent.AI:.2f}"))
            self.agent_table.setItem(i, 4, QTableWidgetItem(f"{agent.AS:.2f}"))
            self.agent_table.setItem(i, 5, QTableWidgetItem(f"{agent.C:.2f}" if agent.C is not None else "-"))

    def agent_selected(self):
        selected_items = self.agent_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.agent_id = int(self.agent_table.item(row, 0).text())
            column = self.agent_table.currentColumn()
            if column == 0:
                self.show_agent_details_window(self.agent_id)
            else:
                self.show_specific_variable_plot(self.agent_id, column)

    def show_agent_details_window(self, agent_id):
        self.agent = self.simulation.get_agent_by_id(agent_id)
        if self.agent:
            time_series = self.simulation.get_time_series()
            agent_window = AgentDetailsWindow(self.agent, time_series)
            self.agent_details_windows.append(agent_window)
            agent_window.show()
        else:
            self.log(f"No agent found with ID: {agent_id}")

    
    def get_variable_data(self, variable_name):
        if variable_name == "Type 1 Tokens":
            return [tokens.get('type 1', 0) for tokens in self.agent.history['tokens']]
        elif variable_name == "Type 2 Tokens":
            return [tokens.get('type 2', 0) for tokens in self.agent.history['tokens']]
        elif variable_name in ['AI', 'AS', 'C', 'S', 'R', 'V', 'A']:
            return self.agent.history[variable_name]
        return []

    def show_specific_variable_plot(self, agent_id, column):
        self.agent = self.simulation.get_agent_by_id(agent_id)
        if self.agent:
            time_series = self.simulation.get_time_series()
            variable_name = self.agent_table.horizontalHeaderItem(column).text()
            variable_data = self.get_variable_data(variable_name)
            
            # Ensure time series and variable data have the same length
            min_length = min(len(time_series), len(variable_data))
            time_series = time_series[:min_length]
            variable_data = variable_data[:min_length]
            
            self.agent_window = AgentDetailsWindow(self.agent, time_series, variable_name, variable_data)
            self.agent_details_windows.append(self.agent_window)
            self.agent_window.show()
        else:
            self.log(f"No agent found with ID: {agent_id}")

    def update_stats(self):
        self.avg_wealth = self.simulation.get_average_wealth()
        self.gini = self.simulation.get_gini_coefficient()
        self.avg_competence = self.simulation.get_average_competence()
        self.stats_label.setText(
            f"Average Wealth: {self.avg_wealth:.2f}\n"
            f"Gini Coefficient: {self.gini:.2f}\n"
            f"Average Competence: {self.avg_competence:.2f}"
        )

    def update_graphs(self):
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
        self.network_figure.clear()
        ax = self.network_figure.add_subplot(111, projection='3d')
        G = self.simulation.get_network()
        pos = nx.spring_layout(G, dim=3)
        # Center the network
        x_coords = [p[0] for p in pos.values()]
        y_coords = [p[1] for p in pos.values()]
        z_coords = [p[2] for p in pos.values()]
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        center_z = sum(z_coords) / len(z_coords)
        # Draw edges manually in 3D
        for u, v in G.edges():
            x = [pos[u][0] - center_x, pos[v][0] - center_x]
            y = [pos[u][1] - center_y, pos[v][1] - center_y]
            z = [pos[u][2] - center_z, pos[v][2] - center_z]
            ax.plot(x, y, z, color='gray', alpha=0.5)
        # Add nodes in 3D
        for node in G.nodes():
            x, y, z = pos[node]
            ax.scatter(x - center_x, y - center_y, z - center_z, s=20)
        # Set axis limits based on zoom factor
        ax.set_xlim(-self.zoom_factor, self.zoom_factor)
        ax.set_ylim(-self.zoom_factor, self.zoom_factor)
        ax.set_zlim(-self.zoom_factor, self.zoom_factor)
        ax.set_axis_off()
        self.network_canvas.mpl_connect('scroll_event', self.zoom)
        self.network_canvas.draw()

    def zoom(self, event):
        factor = 2.0 if event.button == 'up' else 0.9
        self.zoom_factor *= factor
        ax = self.network_figure.axes[0]
        ax.set_xlim(-self.zoom_factor, self.zoom_factor)
        ax.set_ylim(-self.zoom_factor, self.zoom_factor)
        ax.set_zlim(-self.zoom_factor, self.zoom_factor)
        self.network_canvas.draw()

    def reset_view(self):
        self.zoom_factor = 1.0
        ax = self.network_figure.axes[0]
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
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
        logger.info(message)

class AgentDetailsWindow(QDialog):
    def __init__(self, agent, time_series, variable_name=None, variable_data=None):
        super().__init__()
        self.agent = agent
        self.agent_id = agent.agent_id
        self.time_series = time_series
        self.variable_name = variable_name
        self.variable_data = variable_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        if self.variable_name:
            self.plot_specific_variable()
        else:
            self.plot_agent_history()

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_specific_variable(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if self.time_series is not None and self.variable_data is not None:
            if len(self.time_series) == len(self.variable_data):
                ax.plot(self.time_series, self.variable_data)
                ax.set_title(f"Agent {self.agent_id} - {self.variable_name} Over Time")
                ax.set_xlabel("Time Step")
                ax.set_ylabel(self.variable_name)
            else:
                ax.set_title(f"Agent {self.agent_id} - {self.variable_name} Over Time")
                ax.set_xlabel("Time Step")
                ax.set_ylabel(self.variable_name)
                ax.text(0.5, 0.5, f"Data mismatch: Time series length {len(self.time_series)}, variable data length {len(self.variable_data)}",
                        ha='center', va='center', transform=ax.transAxes)
        else:
            ax.set_title(f"Agent {self.agent_id} - {self.variable_name} Over Time")
            ax.set_xlabel("Time Step")
            ax.set_ylabel(self.variable_name)
            ax.text(0.5, 0.5, "No data available for plotting",
                    ha='center', va='center', transform=ax.transAxes)
        
        self.canvas.draw()

    def plot_agent_history(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        history = self.agent.history
        time = self.time_series
        type1 = [tokens.get('type 1', 0) for tokens in history['tokens']]
        type2 = [tokens.get('type 2', 0) for tokens in history['tokens']]
        
        # Log lengths for debugging
        logger.info(f"Time length: {len(time)}, Type1 length: {len(type1)}, Type2 length: {len(type2)}")
        
        # Ensure time and data arrays have the same length
        min_length = min(len(time), len(type1), len(type2), len(history['AI']), len(history['AS']), len(history['C']))
        time = time[:min_length]
        type1 = type1[:min_length]
        type2 = type2[:min_length]
        ai = history['AI'][:min_length]
        as_ = history['AS'][:min_length]
        c = history['C'][:min_length]

        ax.plot(time, type1, label='Type 1 Tokens')
        ax.plot(time, type2, label='Type 2 Tokens')
        ax.plot(time, ai, label='AI (Agent influence)')
        ax.plot(time, as_, label='AS (Agent Status)')
        ax.plot(time, c, label='C (Competence Level)')
        ax.set_title(f"Agent {self.agent_id} Variables Over Time")
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Value")
        ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())