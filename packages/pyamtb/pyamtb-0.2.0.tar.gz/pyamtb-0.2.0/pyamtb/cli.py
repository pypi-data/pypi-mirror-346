import argparse
import os
from .tight_binding_model import calculate_band_structure, create_pythtb_model
from .parameters import Parameters
from .read_datas import read_poscar, create_template_toml
from .check_distance import calculate_distances

def main():
    parser = argparse.ArgumentParser(description="""PyAMTB - Tight-binding model calculations
1. check the distance of `use_elements`
2. create a configuration file `tbparas.toml` and edit it
3. calculate the band structure
""")
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)
    
    # Model calculation command
    calc_parser = subparsers.add_parser('calculate', help='Calculate tight-binding model')
    calc_parser.add_argument('--config', '-c', type=str, help='Path to configuration file')
    calc_parser.add_argument('--poscar', '-p', type=str, help='Path to POSCAR file')
    calc_parser.add_argument('--output', '-o', type=str, help='Output filename')
    
    # Distance calculation command
    dist_parser = subparsers.add_parser('distance', help='Calculate distances between atoms')
    dist_parser.add_argument('--poscar', '-p', type=str, required=True, help='Path to POSCAR file')

    # template toml file
    template_parser = subparsers.add_parser('template', help='Create a template toml file')
    template_parser.add_argument('--filename', '-f', type=str, default="tbparas_template.toml", help='template toml file name')
    args = parser.parse_args()
    
    if args.command == 'calculate':
        # Load configuration
        if args.config:
            # Convert to absolute path if it's not already
            config_path = os.path.abspath(args.config)
            print(f"Looking for config file at: {config_path}")
            params = Parameters(config_path)
            print(params)
        else:
            print("No config file provided, using default parameters")
            params = Parameters()
            
        # Set output filename if provided
        if args.output:
            params.output_filename = args.output
            
        # Set POSCAR file if provided
        if args.poscar:
            poscar_filename = os.path.abspath(args.poscar)
        else:
            poscar_filename = os.path.join(params.savedir, params.output_filename + ".vasp")
            
        # Create and calculate model
        model = create_pythtb_model(params)
        calculate_band_structure(model, params)
        print(f"Calculation completed! Results saved to {params.output_filename}.{params.output_format}")
        
    elif args.command == 'distance':
        # Calculate distances between atoms
        distances = calculate_distances(args.poscar)
        print(f"\nFound {len(distances)} distances between atoms")

    elif args.command == 'template':
        # Create a template toml file
        create_template_toml(args.filename)
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 