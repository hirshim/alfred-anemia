import sys
from anemia_flow import AnemiaWorkflow

def main():
    # Alfred passes arguments as strings.
    # If a previous step passes an arg, it comes in sys.argv[1].
    # If it's the first run, sys.argv might be empty or contain the empty string depending on configuration.
    
    node_id = "root"
    
    # Check if an argument is provided and is not empty
    if len(sys.argv) > 1 and sys.argv[1].strip():
        node_id = sys.argv[1].strip()
        
    wf = AnemiaWorkflow()
    output = wf.generate_json_output(node_id)
    print(output)

if __name__ == "__main__":
    main()
