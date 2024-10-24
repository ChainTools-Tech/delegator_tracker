import logging

from delegator_tracker.cli import parse_args, run_cli
from delegator_tracker.config_loader import load_config
from delegator_tracker.logger import setup_logger
from delegator_tracker.web import run_web  # Example for web mode
from delegator_tracker.exporter import run_exporter  # Example for exporter mode


def main():
    args = parse_args()
    setup_logger(args.log_level)
    config = load_config(args.config)

    logging.debug(f'Command line arguments: {args}.')

    # Check mode and call the appropriate function
    if args.mode == 'cli':
        run_cli(args, config)
    elif args.mode == 'exporter':
        run_exporter(config, args.interval)
    elif args.mode == 'web':
        run_web(config)


if __name__ == "__main__":
    main()
