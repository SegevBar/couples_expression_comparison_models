import os
import csv
import argparse
from datetime import datetime

from Expression_Representation_Generators.DECA.deca_expressions_represantation_generator import DecaExpGenerator
from Expression_Representation_Generators.EMOCA.emoca_expressions_represantation_generator import EmocaExpGenerator
from Expression_Representation_Generators.SPECTRE.spectre_expressions_represantation_generator import \
    SpectreExpGenerator

GENERATORS = {
    "EMOCA" : EmocaExpGenerator,
    "SPECTRE" : SpectreExpGenerator,
    "DECA" : DecaExpGenerator
}


def get_absolute_path(dir_type):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, dir_type)


def main(args):
    data_dir = get_absolute_path("Data")
    results_dir = get_absolute_path("Results")

    curr_result_name = f"results_{datetime.now().strftime('%Y-%m-%d_%H-%M')}_{args.typegenerator}"
    curr_result_path = os.path.join(results_dir, curr_result_name)
    os.makedirs(curr_result_path, exist_ok=True)

    for foldername in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, foldername)

        if os.path.isdir(folder_path):
            all_expressions_representations = []

            for filename in os.listdir(folder_path):
                if filename.endswith('.mp4'):
                    video_path = os.path.join(folder_path, filename)
                    generator = GENERATORS[args.typegenerator](video_path)
                    curr_expressions_representations = generator.generate_expressions_representation()
                    all_expressions_representations = all_expressions_representations + curr_expressions_representations

            # Save outputs to CSV
            csv_filename = os.path.join(curr_result_path, foldername + ".csv")
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(all_expressions_representations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='expressions represantation generator')
    parser.add_argument('-t', '--typegenerator', default='SPECTRE', type=str,
                        help='type of expression representation generator')
    main(parser.parse_args())
