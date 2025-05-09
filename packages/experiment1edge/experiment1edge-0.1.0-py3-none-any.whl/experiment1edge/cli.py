# myedges/cli.py
import argparse
from .image_utils import edge_detection

def main():
    parser = argparse.ArgumentParser(description="Edge detection on an image")
    parser.add_argument("--input", required=True, help="Path to input image")
    args = parser.parse_args()

    edge_detection(args.input)
