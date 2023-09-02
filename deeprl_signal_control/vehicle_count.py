import traci

def get_real_time_vehicle_counts(edge_id, port=8813, time_to_wait=1000):
    try:
        # Initialize TraCI connection
        traci.init(port, time_to_wait)

        while traci.simulation.getMinExpectedNumber() > 0:
            # Retrieve real-time vehicle count for the specified edge (intersection)
            vehicle_count = traci.edge.getLastStepVehicleNumber(edge_id)
            
            # Print the vehicle count
            print(f"Real-time vehicle count at {edge_id}: {vehicle_count}")
        
        # Close TraCI connection when done
        traci.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the ID of the edge (intersection) you want to monitor
    intersection_edge_id = "your_intersection_edge_id_here"
    
    # Call the function to get real-time vehicle counts
    get_real_time_vehicle_counts(intersection_edge_id)
