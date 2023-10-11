from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import itertools
import tkinter as tk
from tkinter import ttk, messagebox

class TravelingSalesmanApp:
    def __init__(self, master):
        self.master = master
        
        self.master.title("Traveling Salesman Problem")
        self.background_image = tk.PhotoImage(file="TSP/trans.png")

        # Create a label to hold the background image
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Predefined data sets
        self.distance_matrix = [
            [0, 4000, 6000, 8000, 5000, 9000, 3500, 16000, 9000, 1500],
            [4000, 0, 9000, 7000, 11000, 7000, 1300, 11000, 11000, 4500],
            [6000, 9000, 0, 12000, 5000, 15000, 12000, 20000, 15000, 6500],
            [8000, 7000, 12000, 0, 9000, 7000, 7100, 17000, 5000, 8600],
            [5000, 11000, 5000, 9000, 0, 13000, 11000, 17000, 13000, 5200],
            [9000, 7000, 15000, 7000, 13000, 0, 8100, 10000, 2000, 9900],
            [3500, 1300, 12000, 7100, 11000, 8100, 0, 12000, 10000, 3000],
            [16000, 11000, 20000, 17000, 17000, 10000, 12000, 0, 9000, 15000],
            [9000, 11000, 15000, 5000, 13000, 2000, 10000, 9000, 0, 7500],
            [1500, 4500, 6500, 8600, 5200, 9900, 3000, 15000, 7500, 0],
        ]

        self.famous_places = [
            "Statue of Liberty, New York",
            "Eiffel Tower, Paris",
            "Great Wall of China, Beijing",
            "Taj Mahal, Agra",
            "Machu Picchu, Peru",
            "Pyramids of Giza, Egypt",
            "Big Ben, London",
            "Sydney Opera House, Sydney",
            "Christ the Redeemer, Rio de Janeiro",
            "Colosseum, Rome",
        ]

        self.selected_indices = []

        self.create_widgets()

    def create_widgets(self):
        # Remove default window background
        self.master.configure(bg='grey')

        self.label = tk.Label(self.master, text="Select places to visit:", bg='red')
        self.label.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#BDBDBD")

        for i, place in enumerate(self.famous_places):
            btn = ttk.Button(self.master, text=place, command=lambda i=i: self.add_to_itinerary(i))
            btn.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)

        style.configure("Finish.TButton", background='red', foreground='red')
        self.finish_button = ttk.Button(self.master, text="Finish", command=self.calculate_route, style="Finish.TButton")
        self.finish_button.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)

    def add_to_itinerary(self, index):
        self.selected_indices.append(index)
        messagebox.showinfo("Added", f"{self.famous_places[index]} added to your itinerary.")

    def calculate_route(self):
        if len(self.selected_indices) >= 3:
            optimal_route, total_distance = self.find_optimal_route()
            messagebox.showinfo("Optimal Route",
                                f"Optimal Route:\n{optimal_route}\nTotal Distance: {total_distance}")
        else:
            messagebox.showwarning("Error", "Please select at least 3 places before finishing.")

    def find_optimal_route(self):
        data = self.create_data_model()
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        solution = routing.SolveWithParameters(search_parameters)
        if solution:
            index = routing.Start(0)
            route = ''
            total_distance = 0
            while not routing.IsEnd(index):
                route += f"{data['locations'][manager.IndexToNode(index)]} -> "
                total_distance += distance_callback(index, solution.Value(routing.NextVar(index)))
                index = solution.Value(routing.NextVar(index))
            route += f"{data['locations'][manager.IndexToNode(index)]}"  # Depot
            return route, total_distance
        else:
            return "No solution found!", 0

    def create_data_model(self):
        data = {}
        data['locations'] = [self.famous_places[i] for i in self.selected_indices]
        data['distance_matrix'] = [
            [self.distance_matrix[i][j] for j in self.selected_indices]
            for i in self.selected_indices
        ]
        data['num_vehicles'] = 1
        data['depot'] = 0
        return data


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelingSalesmanApp(root)
    root.mainloop()
