"""Command-line options for the Hexa launcher."""
import argparse


def build_parser():
    parser = argparse.ArgumentParser(description="Play Hexa.")
    parser.add_argument("--mode", choices=("campaign", "conquest", "colony"), help="skip the menu and start this mode")
    parser.add_argument("--nation", help="campaign: play this country straight away (e.g. POR, ENG, VEN)")
    parser.add_argument("--map", choices=("europe", "random"), default="europe",
                        help="campaign: the real 1480 map or a random world")
    parser.add_argument("--start", choices=("sea", "land"), default="sea", help="colonisation: how to start")
    parser.add_argument("--goal", choices=("survive", "independence", "endless"), default="survive",
                        help="colonisation: how to win")
    parser.add_argument("--seed", type=int, help="map number, to replay the same map")
    return parser


def parse(argv=None):
    """Return the settings, whether to skip the menu, the nation and the seed."""
    args = build_parser().parse_args(argv)
    settings = {"mode": args.mode or "campaign", "start": args.start, "goal": args.goal, "map": args.map}
    skip_menu = args.mode is not None
    return settings, skip_menu, args.nation, args.seed
